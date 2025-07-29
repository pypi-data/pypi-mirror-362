import logging
import argparse
import sys
import subprocess
from os import getenv

from datetime import datetime
import time

from .loaders import apply_config_settings
from .nornir.logging import LOG_FORMAT
from .utils import send_email, agador_cfg

logger = logging.getLogger("agador")

LOOP_INTERVAL = 10


def main():
    parser = argparse.ArgumentParser(description="Run agador")
    parser.add_argument(
        "--cfg-file",
        help="Configuration file.",
    )
    parser.add_argument(
        "-l", "--log-level", default="INFO", help="Set log level for agador only"
    )
    parser.add_argument("--echo", action="store_true", help="echo logfile to stdout")
    args = parser.parse_args()

    cfg_file = args.cfg_file if args.cfg_file else getenv("AGADOR_CFG")
    if not cfg_file:
        raise ValueError(
            "No config file provided as argument or env variable AGADOR_CFG"
        )

    apply_config_settings(cfg_file)

    cmd_map = agador_cfg("CMD_MAP")

    base_run_cmd = ["agador-run", "-l", args.log_level.upper(), "--cfg-file", cfg_file]

    # setting up logging
    file_handler = logging.handlers.RotatingFileHandler(
        agador_cfg("LOG_DIR") + "/agador.log", maxBytes=1024 * 1024 * 10, backupCount=20
    )
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(file_handler)
    logger.setLevel(args.log_level)
    if args.echo:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(stdout_handler)
        base_run_cmd.append("--echo")

    email_to = agador_cfg("EMAIL_RECIPIENTS")
    if email_to:
        base_run_cmd.extend(["--email-result", email_to])

    current_run = None

    last_check = datetime.now()
    while True:
        # If there's a previous run and it has finished, check to make sure there
        # were no errors. If there were errors and we're configured to send emails,
        # send an email indicating what the error was.
        if current_run and current_run.poll():
            _, errs = current_run.communicate()
            if errs:
                error_msg = f"Agador run (PID {current_run.pid}) ended unexpectedly.\n\n{errs.decode('utf-8')}"
                logger.error(error_msg)
                if email_to:
                    send_email(
                        email_from=agador_cfg("EMAIL_ADDRESS"),
                        email_to=email_to,
                        subject="Unexpected error",
                        message=error_msg,
                    )

            current_run = None

        # waiting a bit, then checking the time
        time.sleep(LOOP_INTERVAL)
        now = datetime.now()

        # if any commands are scheduled to run between now and the last time
        # we checked the time, put them on a list of commands to run
        cmds_to_run = []
        for cmd, data in cmd_map.items():
            run_time = data["frequency"].schedule(now).prev()
            if run_time >= last_check:
                cmds_to_run.append(cmd)

        # If we have commands to run, first check to see if the previous run has completed.
        # if it has, run our new commands
        if cmds_to_run:
            if current_run and current_run.poll() is None:
                logger.error(
                    f"Agador wants to run cmds {','.join(cmds_to_run)} but previous run (PID {current_run.pid}) has not completed!"
                )
            else:
                cmd_args = base_run_cmd.copy()
                cmd_args.append("--cmds")
                cmd_args.extend(cmds_to_run)
                current_run = subprocess.Popen(cmd_args, stderr=subprocess.PIPE)
                logger.info(f"Starting agador run (PID {current_run.pid}): {cmd_args}")

        last_check = now


if __name__ == "__main__":
    main()
