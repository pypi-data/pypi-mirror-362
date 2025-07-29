from typing import Optional

import logging
import threading
from datetime import datetime
import traceback

from nornir.core.task import AggregatedResult, Task, MultiResult
from nornir.core.inventory import Host

from .logging import LOG_FORMAT, ThreadLogFilter
from ..utils import send_email


logger = logging.getLogger(__name__)


class ProcessorBase:
    """
    convenience parent class so we don't have to define unused
    methods in child classes
    """

    def task_started(self, task: Task) -> None:
        pass

    def task_completed(self, task: Task, result: AggregatedResult) -> None:
        pass

    def task_instance_started(self, task: Task, host: Host) -> None:
        pass

    def task_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        pass

    def subtask_instance_started(self, task: Task, host: Host) -> None:
        pass

    def subtask_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        pass


class AgadorProcessor(ProcessorBase):
    """
    Agador processor. Designed to write to a specified logfile and optionally to stdout.
    If 'email_to' is not none, will send an email summarizing the results at the end.
    """

    def __init__(
        self,
        cmd_map: dict,
        total_hosts: int,
        logfile: str,
        email_from: str,
        email_to: Optional[str] = None,
        cli_output: Optional[bool] = False,
    ):
        self.cmd_map = cmd_map
        self.total_hosts = total_hosts
        self.email_from = email_from
        self.email_to = email_to
        self.logfile = logfile
        self.cli_output = cli_output
        self.start_time = datetime.now()

    def _log_output(self, output_str: str):
        with open(self.logfile, "a", encoding="utf-8") as fh:
            fh.write(output_str)

        if self.cli_output:
            print(output_str)

    def task_started(self, task: Task) -> None:
        msg = f"\n******* {task.name} Started at {self.start_time} *******\n"
        self._log_output(msg)

    def task_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        msg = f"** {host.name} "
        if result.failed:
            msg += f"failed at {datetime.now()}"
            for r in result:
                if r.exception:
                    msg += f" and raised an exception {r.exception}"
                if r.result:
                    msg += f" with traceback:\n\n{r.result}\n\n"

            msg += "**"
        else:
            msg += f"completed successfully at {datetime.now()}"

        msg += "**\n"
        self._log_output(msg)

    def task_completed(self, task: Task, result: AggregatedResult) -> None:
        """
        going to log, optionally print, and email the final results
        """

        # first step is to run any post-processing from the mappers in the command map
        for cmd, data in self.cmd_map.items():
            if data.get("save_to_file"):
                mapper = data["save_to_file"]["mapper"]
            elif data.get("save_to_db"):
                mapper = data["save_to_db"]

            try:
                if hasattr(mapper, "post_processing"):
                    getattr(mapper, "post_processing")()
            except Exception as e:
                logger.error(f"Error running post_procesing for {mapper} - {e}")
                logger.error(traceback.format_exc())

        # calculating how long the run took
        now = datetime.now()
        elapsed = (now - self.start_time).seconds
        m, s = divmod(elapsed, 60)
        h, m = divmod(m, 60)
        duration = f"{h} hours, {m} minutes, {s}, seconds"

        # generating outpupt message
        num_failed = len([r for r in result.values() if r.failed])
        num_passed = self.total_hosts - num_failed
        num_skipped = len(
            [r for r in result.values() if r.result == "No commands to execute"]
        )

        result_str = f"Completed run against {self.total_hosts} devices at {now}\n\n"
        result_str = f"Commands run: {', '.join(self.cmd_map)}\n"
        result_str += f"Elapsed time: {duration}\nTotal passed: {num_passed}\nTotal skipped: {num_skipped}\nTotal failed {num_failed}\n"

        if num_failed:
            result_str += "\nThe following devices failed:\n"
            for device, multi_results in result.items():
                # skip tasks that passed
                if not multi_results.failed:
                    continue

                errors = [str(r.exception) for r in multi_results if r.failed]
                result_str += f"\t{device}: {','.join(errors)}\n"

        self._log_output(result_str)

        if self.email_to:
            send_email(
                email_from=self.email_from,
                email_to=self.email_to,
                subject=f"Run result at {now}",
                message=result_str,
            )


class TraceFile(ProcessorBase):
    """
    Class that sets up and tears down logging to a host-based tracefile
    """

    def __init__(self, trace_dir: str):
        self.trace_dir = trace_dir

    def task_instance_started(self, task: Task, host: Host) -> None:
        """
        Sets up tracefile and log handler filtering for the host's thread name
        """
        thread_name = threading.current_thread().name
        timestamp = datetime.now().strftime("%Y%d%m_%H%M%S")

        log_file = f"{self.trace_dir}/{host.name}_{timestamp}.trace"
        log_handler = logging.FileHandler(log_file)
        log_handler.addFilter(ThreadLogFilter(thread_name))
        log_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        log_handler.name = host.name

        logger = logging.getLogger()
        logger.addHandler(log_handler)
        logger.setLevel(logging.DEBUG)

    def task_instance_completed(
        self, task: Task, host: Host, result: MultiResult
    ) -> None:
        """
        Tears down host log filter so that hosts using the same thread
        in the future don't get logged to this file
        """
        logger = logging.getLogger()

        # should only be one with this name
        [logger.removeHandler(h) for h in logger.handlers if h.name == task.host.name]
