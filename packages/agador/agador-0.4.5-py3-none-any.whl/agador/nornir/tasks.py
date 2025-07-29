import logging
import traceback
from nornir.core.task import Result, Task
from nornir.core.exceptions import NornirSubTaskError
from sqlalchemy.engine import Engine

from umnet_napalm import get_network_driver

from ..utils import get_device_cmd_list
from ..mappers.save_to_file import SaveResult
from ..mappers.save_to_db import ResultsToDb

from sqlalchemy import create_engine

logger = logging.getLogger(__name__)


def process_device(
    task: Task,
    cmd_map: dict,
    db_url: str,
) -> Result:
    """
    Run a set of commands against a specific device based on the
    command mapper and an optional restricted list of commands.
    If no list is provided all commands in the mapper will be run
    """
    db_engine = create_engine(db_url)

    # first figure out which commands to run against this host
    cmd_list = get_device_cmd_list(cmd_map, task.host)

    logger.debug(f"Running getters on {task.host.name}: {cmd_list}")
    if not cmd_list:
        logger.debug(f"No commands to execute for {task.host.name}")
        return Result(
            host=task.host,
            result="No commands to execute",
            exception="No commands to execute",
        )

    # finding that for multiprocessing it's cleaner to use the context
    # manager - by this we mean 'with network_driver as device' - because
    # connection failures that raise exceptions aren't otherwise well tolerated.
    network_driver = get_network_driver(task.host.platform)
    parameters = {
        "hostname": task.host.hostname,
        "username": task.host.username,
        "password": task.host.password,
        "optional_args": {},
    }
    parameters.update(task.host.connection_options["umnet_napalm"].extras)

    getter_results = {}
    try:
        with network_driver(**parameters) as device:
            for cmd, getter in cmd_list.items():
                method = getattr(device, getter)
                getter_results[cmd] = method()

    except Exception as e:
        tb = traceback.format_exc()
        logger.error(
            "Host %r getters failed with traceback:\n%s",
            task.host.name,
            tb,
        )
        return Result(host=task.host, result=tb, exception=str(e), failed=True)

    # for each command save data using the appropriate methods based
    # on the command map
    for cmd, result in getter_results.items():
        if "save_to_db" in cmd_map[cmd]:
            try:
                task.run(
                    name=f"{cmd}_save_to_db",
                    task=update_table,
                    result=result,
                    engine=db_engine,
                    mapper=cmd_map[cmd]["save_to_db"],
                )
            except NornirSubTaskError as e:
                logger.error(f"{task.host.name} save_to_db error: {e}")

        if "save_to_file" in cmd_map[cmd]:
            try:
                task.run(
                    name=f"{cmd}_save_to_file",
                    task=save_to_file,
                    result=result,
                    mapper=cmd_map[cmd]["save_to_file"]["mapper"],
                )
            except NornirSubTaskError as e:
                logger.error(f"{task.host.name} save_to_file error: {e}")

    return Result(host=task.host, result="Completed")


def update_table(
    task: Task,
    result: Result,
    engine: Engine,
    mapper: ResultsToDb,
) -> Result:
    """
    Generic task for taking the results from a previous "napalm_get"
    task and saving it to the database
    """
    mapper(task.host.name, task.host.hostname, result, engine)

    return Result(host=task.host)


def save_to_file(
    task: Task,
    result: dict,
    mapper: SaveResult,
) -> Result:
    """
    Task for saving to a file
    """
    mapper.write_to_file(task.host, result)

    return Result(host=task.host)
