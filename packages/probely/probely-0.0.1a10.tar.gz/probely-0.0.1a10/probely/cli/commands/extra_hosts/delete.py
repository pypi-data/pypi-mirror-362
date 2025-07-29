import argparse

from probely.cli.commands.extra_hosts.update import _validate_extra_hosts_ids
from probely.sdk.managers import TargetExtraHostManager


def extra_hosts_delete_command_handler(args: argparse.Namespace):
    target_id = args.target_id
    extra_hosts_ids = args.extra_hosts_ids

    _validate_extra_hosts_ids(target_id, extra_hosts_ids)

    for extra_host_id in extra_hosts_ids:
        TargetExtraHostManager().delete({"target_id": target_id, "id": extra_host_id})

    for extra_host_id in extra_hosts_ids:
        args.console.print(extra_host_id)
