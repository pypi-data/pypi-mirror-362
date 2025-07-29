import copy
import logging
import traceback
from typing import Any, Dict, List, Optional

from nornir.core.task import Result, Task
from umnet_napalm import get_network_driver

from .connections import CONNECTION_NAME

GetterOptionsDict = Optional[Dict[str, Dict[str, Any]]]


logger = logging.getLogger(__name__)


def umnet_napalm_get(
    task: Task,
    getters: List[str],
    getters_options: GetterOptionsDict = None,
    **kwargs: Any,
) -> Result:
    """
    Gather information from network devices using napalm

    Arguments:
        getters: getters to use
        getters_options (dict of dicts): When passing multiple getters you
            pass a dictionary where the outer key is the getter name
            and the included dictionary represents the options to pass
            to the getter
        **kwargs: will be passed as they are to the getters

    Returns:
        Result object with the following attributes set:
          * result (``dict``): dictionary with the result of the getter
    """
    try:
        device = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
        getters_options = getters_options or {}

        if isinstance(getters, str):
            getters = [getters]

        result = {}
        for g in getters:
            options = copy.deepcopy(kwargs)
            options.update(getters_options.get(g, {}))
            getter = g if g.startswith("get_") else "get_{}".format(g)
            method = getattr(device, getter)
            result[g] = method(**options)

    except Exception as e:
        tb = traceback.format_exc()
        logger.error(
            "Host %r getters failed with traceback:\n%s",
            task.host.name,
            tb,
        )
        return Result(host=task.host, result=tb, exception=str(e), failed=True)
    return Result(host=task.host, result=result)


def umnet_napalm_get_in_context(
    task: Task,
    getters: Dict[str, GetterOptionsDict],
):
    """
    This task runs the list of getters in a napalm context manager -
    opening a connection, running the getters, then closing the connection.

    Find that this is more resilient, particularly in a multiprocess scenario.
    """
    parameters = {
        "hostname": task.host.hostname,
        "username": task.host.username,
        "password": task.host.password,
        "optional_args": {},
    }
    parameters.update(task.host.connection_options["umnet_napalm"].extras)

    network_driver = get_network_driver(task.host.platform)

    result = {}
    try:
        with network_driver(**parameters) as device:
            for getter, options in getters.items():
                method = getattr(device, getter)
                result[getter] = method(**options)

        return Result(host=task.host, result=result)
    except Exception:
        return Result(host=task.host, result="Connection error")
