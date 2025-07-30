import time
import uuid
from datetime import datetime
from statistics import mean
from typing import List

import requests
from cached_property import cached_property
from dallinger import db
from sqlalchemy import Column, Integer

from .db import transaction
from .participant import Participant
from .timeline import Page
from .utils import NoArgumentProvided, get_logger, log_time_taken, wait_until

logger = get_logger()


class Bot(Participant):
    page_count = Column(Integer, default=1)

    def __init__(
        self,
        recruiter_id="bot_recruiter",
        worker_id=None,
        assignment_id=None,
        unique_id=None,
        hit_id="",
        mode="debug",
    ):
        self.wait_until_experiment_launch_is_complete()

        if worker_id is None:
            worker_id = str(uuid.uuid4())

        if assignment_id is None:
            assignment_id = str(uuid.uuid4())

        logger.info("Initializing bot with worker ID %s.", worker_id)

        super().__init__(
            self.experiment,
            recruiter_id=recruiter_id,
            worker_id=worker_id,
            assignment_id=assignment_id,
            hit_id=hit_id,
            mode=mode,
        )

        db.session.add(self)
        db.session.commit()

    def initialize(self, experiment):
        self.experiment.initialize_bot(bot=self)
        super().initialize(experiment)

    def wait_until_experiment_launch_is_complete(self):
        from .experiment import is_experiment_launched

        def f():
            logger.info("Waiting for experiment launch to complete....")
            return is_experiment_launched()

        wait_until(
            f, max_wait=60, error_message="Experiment launch didn't finish in time"
        )

    @cached_property
    def experiment(self):
        from .experiment import get_experiment

        return get_experiment()

    @cached_property
    def timeline(self):
        return self.experiment.timeline

    def get_current_page(self):
        return self.experiment.get_current_page(self.experiment, self)

    @log_time_taken
    def take_experiment(self, time_factor=0, render_pages: bool = False):
        """
        Parameters
        ----------

        time_factor :
            Determines how long the bot spends on each page.
            If 0, the bot spends no time on each page.
            If 1, the bot spends ``time_estimate`` time on each page.

        render_page :
            Whether to run page rendering code (default: False).
            This is generally only useful for testing.
        """
        logger.info(f"Bot {self.id} is starting the experiment.")
        self.run_to_completion(time_factor, render_pages)

    def run_to_completion(self, time_factor=0, render_pages: bool = False):
        # We tried the following code to simulate the Flask server and thereby
        # run Page.render() functions directly. However the approach fails
        # when we try to run multiple tests in succession, because Flask
        # doesn't let us deregister the old apps.
        #
        # from gunicorn import util
        # from .utils import working_directory
        # with working_directory(self.experiment.var.server_working_directory):
        # app = util.import_app("dallinger.experiment_server.sockets:app")
        # with app.app_context(), app.test_request_context():
        n_pages = 0

        page_processing_times = []
        page_total_times = []

        while True:
            page_time_started = time.monotonic()

            # This commit is necessary because get_current_page can make changes to the participant
            # (e.g. advancing them to the next page in the timeline). We need to commit so that the
            # server (as accessed via the HTTP request) has access to this information too.

            sleep_time = self.take_page(
                time_factor=time_factor, render_page=render_pages
            )["sleep_time"]

            page_time_finished = time.monotonic()
            page_total_time = page_time_finished - page_time_started

            page_total_times.append(page_total_time)

            page_processing_time = page_total_time - sleep_time
            page_processing_times.append(page_processing_time)

            n_pages += 1

            if not self.status == "working":
                break

        if n_pages > 0:
            mean_page_processing_time = mean(page_processing_times)
        else:
            mean_page_processing_time = None

        total_experiment_time = (datetime.now() - self.creation_time).total_seconds()

        # Todo - migrate these metrics to generic Participants (not just bots) so that we can report them
        # everywhere
        stats = {
            "page_count": self.page_count,
            "progress": self.progress,
            "mean_page_processing_time": mean_page_processing_time,
            "total_wait_page_time": self.total_wait_page_time,
            "total_experiment_time": total_experiment_time,
        }

        logger.info(
            f"Bot {self.id} has finished the experiment (took {stats['page_count']} page(s), "
            f"progress = {100 * stats['progress']:.0f}%, "
            f"mean processing time per page = {stats['mean_page_processing_time']:.3f} seconds, "
            f"total WaitPage time = {stats['total_wait_page_time']:.3f} seconds, "
            f"total experiment time = {stats['total_experiment_time']:.3f} seconds)."
        )

        return stats

    # In a real launched experiment, taking a page involves a single HTTP request that is wrapped in a transaction.
    # We therefore do the same here, to ensure that the bot's behavior is as close as possible to that of a real
    # participant.
    def take_page(
        self, page=None, time_factor=0, response=NoArgumentProvided, render_page=False
    ):
        from .page import WaitPage

        if render_page:
            db.session.commit()  # Make sure that any local changes to the participant are visible to the server
            req = requests.get(
                f"http://localhost:5000/timeline?unique_id={self.unique_id}"
            )
            assert req.status_code == 200
            db.session.commit()  # Make sure any server-side changes are visible to us

        with transaction():
            # Locks the present participant row
            self = (
                self.__class__.query.with_for_update(of=self.__class__)
                .populate_existing()
                .get(self.id)
            )

            start_time = time.monotonic()

            if page is None:
                page = self.get_current_page()

            bot = self
            experiment = self.experiment
            assert isinstance(page, Page)

            sleep_time = page.time_estimate * time_factor

            if sleep_time == 0 and isinstance(page, WaitPage):
                sleep_time = 0.5

            if sleep_time > 0:
                time.sleep(sleep_time)

            response = page.call__bot_response(experiment, bot, response)

            if "time_taken" not in response.metadata:
                response.metadata["time_taken"] = sleep_time

            try:
                experiment.process_response(
                    participant_id=self.id,
                    raw_answer=response.raw_answer,
                    blobs=response.blobs,
                    metadata=response.metadata,
                    page_uuid=self.page_uuid,
                    client_ip_address=response.client_ip_address,
                    answer=response.answer,
                )
            except RuntimeError as err:
                if "Working outside of request context" in str(err):
                    err.args = (
                        err.args[0]
                        + "\n\nNote: The 'working outside of request context' error can usually be ignored "
                        "during testing as it typically comes from Flask trying to construct an "
                        "error page without a valid request context. The real error probably "
                        "happened earlier though.",
                    )
                raise

        self.page_count += 1

        end_time = time.monotonic()
        processing_time = end_time - start_time - sleep_time

        return {
            "sleep_time": sleep_time,
            "processing_time": processing_time,
        }

    def submit_response(self, response=NoArgumentProvided):
        page = self.get_current_page()
        self.take_page(page, response=response)

    def run_until(self, condition, render_pages=False):
        while True:
            current_page = self.get_current_page()
            if condition(current_page):
                break
            self.take_page(current_page, render_page=render_pages)
            if not self.status == "working":
                raise RuntimeError(
                    "Bot finished the experiment before condition was met."
                )


class BotResponse:
    """
    Defines a bot's response to a given page.

    Parameters
    ----------
        raw_answer :
            The raw_answer returned from the page.

        answer :
            The (formatted) answer, as would ordinarily be computed by ``format_answer``.

        metadata :
            A dictionary of metadata.

        blobs :
            A dictionary of blobs returned from the front-end.

        client_ip_address :
            The client's IP address.
    """

    def __init__(
        self,
        *,
        raw_answer=NoArgumentProvided,
        answer=NoArgumentProvided,
        metadata=NoArgumentProvided,
        blobs=NoArgumentProvided,
        client_ip_address=NoArgumentProvided,
    ):
        if raw_answer != NoArgumentProvided and answer != NoArgumentProvided:
            raise ValueError(
                "raw_answer and answer cannot both be provided; you should probably just provide raw_answer."
            )

        if raw_answer == NoArgumentProvided and answer == NoArgumentProvided:
            raise ValueError("At least one of raw_answer and answer must be provided.")

        if blobs == NoArgumentProvided:
            blobs = {}

        if metadata == NoArgumentProvided:
            metadata = {}

        if client_ip_address == NoArgumentProvided:
            client_ip_address = None

        self.raw_answer = raw_answer
        self.answer = answer
        self.metadata = metadata
        self.blobs = blobs
        self.client_ip_address = client_ip_address


def advance_past_wait_pages(bots: List[Bot], max_iterations=10):
    from .page import WaitPage

    iteration = 0
    while True:
        iteration += 1
        any_waiting = False
        for bot in bots:
            current_page = bot.get_current_page()
            if isinstance(current_page, WaitPage):
                any_waiting = True
                bot.take_page(current_page)
        if not any_waiting:
            break
        if iteration >= max_iterations:
            raise RuntimeError("Not all bots finished waiting in time.")
