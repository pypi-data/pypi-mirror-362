import sys
import re
import argparse
from datetime import datetime
import logging


from .nornir import nornir_setup
from .nornir.logging import configure_nornir_logging

from .nornir.tasks import process_device
from .nornir.processors import (
    AgadorProcessor,
    TraceFile,
)
from .utils import validate_email_list, AgadorError, agador_cfg
from .loaders import apply_config_settings


def main():
    parser = argparse.ArgumentParser(description="Run agador")

    parser.add_argument(
        "--cfg-file",
        help="Configuration file. You can also set this as AGADOR_CFG in your environennt",
    )

    filter_args = parser.add_mutually_exclusive_group()
    filter_args.add_argument(
        "--device", help="Restrict the update to a particular device"
    )
    filter_args.add_argument(
        "--role", help="Restrict the update to a specific netbox device role"
    )

    parser.add_argument(
        "--cmds",
        nargs="*",
        help="Limit update to a subset of tasks/commands",
    )
    parser.add_argument(
        "--email-result", help="Email result to a comma-separated list of addresses."
    )

    log_args = parser.add_mutually_exclusive_group()
    log_args.add_argument("-l", "--log-level", help="Set log level for agador only")
    log_args.add_argument("-L", "--LOG-LEVEL", help="set log level for all libraries")
    parser.add_argument(
        "--echo", action="store_true", help="echo logfile to stdout", default=True
    )
    parser.add_argument("--trace", action="store_true", help="Save device session logs")

    args = parser.parse_args()

    apply_config_settings(args.cfg_file)

    cmd_map = agador_cfg("CMD_MAP")

    # input validation
    if args.cmds:
        for cmd in args.cmds:
            if cmd not in cmd_map:
                print(
                    f"ERROR: {cmd} not in command map! valid commands: {','.join(cmd_map.keys())}"
                )
                sys.exit(1)

        # if we're filtering on what commands to run, remove them from the command map
        cmd_map = {k: v for k, v in cmd_map.items() if k in args.cmds}

    if args.trace and not args.device:
        sure = input(
            "Trace output is for debugging only. Are you sure you want to save session logs for ALL devices (y/n)? "
        )
        if re.match(r"[Yy]", sure):
            print(f"Fine. Logs will be saved at {agador_cfg('LOG_DIR')}")
        else:
            print("Good choice! Turning trace off.")
            args.trace = False

    if args.email_result:
        validate_email_list(args.email_result)

    # logging configuration
    if args.log_level:
        log_level = args.log_level
    elif args.LOG_LEVEL:
        log_level = args.LOG_LEVEL
    else:
        log_level = logging.INFO

    logfile = agador_cfg("LOG_DIR") + "/agador.log"
    logger = configure_nornir_logging(
        log_level,
        log_globally=bool(args.LOG_LEVEL),
        log_file=logfile,
        log_to_console=bool(args.echo),
    )

    # initialize nornir
    logger.info("initializing nornir")
    nr = nornir_setup(
        device_filter=args.device,
        role_filter=args.role,
    )

    logger.info(
        "Nornir initialization complete - inventory has %s items",
        len(nr.inventory.hosts.keys()),
    )

    if not (nr.inventory.hosts.keys()):
        logger.error("No matching hosts found in netbox inventory!")
        raise AgadorError("No matching hosts found in netbox inventory!")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_logfile = f"{agador_cfg('LOG_DIR')}/results_{timestamp}"

    # setting up processors
    processors = [
        AgadorProcessor(
            cmd_map=cmd_map,
            total_hosts=len(nr.inventory.hosts),
            email_from=agador_cfg("EMAIL_ADDRESS"),
            logfile=results_logfile,
            email_to=args.email_result,
            cli_output=args.echo,
        )
    ]

    if args.trace:
        processors.append(TraceFile(agador_cfg("LOG_DIR")))

    logger.debug("Starting run...")
    nr.with_processors(processors).run(
        task=process_device,
        cmd_map=cmd_map,
        db_url=agador_cfg("DB_URL"),
        on_failed=True,
    )


if __name__ == "__main__":
    main()
