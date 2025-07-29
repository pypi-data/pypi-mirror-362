import argparse
from pprint import pprint
from os import getenv

from umnet_napalm import get_network_driver, PLATFORM_MAP
from umnet_napalm.abstract_base import AbstractUMnetNapalm
from umnet_napalm.utils import configure_logging, LOG_LEVELS


# list of getters to test
GETTERS = [
    attr for attr in AbstractUMnetNapalm.__abstractmethods__ if attr.startswith("get")
]


def get_from_args_or_env(
    cli_arg: str, parsed_args: argparse.Namespace, required=True
) -> str:
    """
    Pull a value from parsed arparse, if it's not there look for it
    in the environment
    """
    cli_arg = cli_arg.replace("-", "_")

    if getattr(parsed_args, cli_arg, False):
        return getattr(parsed_args, cli_arg)

    env_arg = cli_arg.upper()
    if getenv(env_arg):
        return getenv(env_arg)

    if required:
        raise ValueError(
            f"ERROR: Please provide {cli_arg} as cli input or as {env_arg} environment variable"
        )
    return None


cred_args = {"napalm-username": True, "napalm-password": True, "napalm-enable": False}


def main():
    parser = argparse.ArgumentParser(
        description="""
Run a specific umnet_napalm "getter" against a device.
"""
    )
    parser.add_argument("device", help="device hostname or IP address")
    parser.add_argument(
        "umnet_napalm_platform",
        choices=PLATFORM_MAP,
        help="The platform of this device",
    )
    parser.add_argument(
        "cmd",
        choices=GETTERS,
        help="The getter command to run against this device",
    )
    log_args = parser.add_mutually_exclusive_group()
    log_args.add_argument(
        "-l", "--log-level", help="Set log level for nornir only", choices=LOG_LEVELS
    )
    log_args.add_argument(
        "-L", "--LOG-LEVEL", help="set log level for all libraries", choices=LOG_LEVELS
    )
    parser.add_argument(
        "--tracefile",
        type=str,
        help="Save logging to a file (specified by name) instead of to stdout",
    )
    parser.add_argument(
        "--pan-host",
        type=str,
        help="If this is a managed panos device, specify panorama hostname",
    )
    parser.add_argument(
        "--pan-serial",
        type=str,
        help="If this is a panorama managed device, specify the device's serial number",
    )

    for cred_arg in cred_args:
        parser.add_argument(f"--{cred_arg}", help="Specify credentials")
    args = parser.parse_args()

    log_level = args.log_level if args.log_level else args.LOG_LEVEL
    if log_level:
        configure_logging(
            log_level,
            log_globally=bool(args.LOG_LEVEL),
            log_file=args.tracefile,
            log_to_console=not (bool(args.tracefile)),
        )

    creds = {
        cred: get_from_args_or_env(cred, args, required=reqd)
        for cred, reqd in cred_args.items()
    }
    Driver = get_network_driver(args.umnet_napalm_platform)

    # setting up connection details
    optional_args = {"look_for_keys": False, "secret": creds["napalm-enable"]}

    # overriding hostname and adding s/n and API key for panorama hosts
    if args.pan_host:
        optional_args["serial"] = args.pan_serial
        optional_args["panorama"] = args.pan_host
        optional_args["api_key"] = getenv("PANORAMA_API_KEY")

    with Driver(
        args.device,
        creds["napalm-username"],
        creds["napalm-password"],
        timeout=6000,
        optional_args=optional_args,
    ) as conn:
        result = getattr(conn, args.cmd)()
        pprint(result)


if __name__ == "__main__":
    main()
