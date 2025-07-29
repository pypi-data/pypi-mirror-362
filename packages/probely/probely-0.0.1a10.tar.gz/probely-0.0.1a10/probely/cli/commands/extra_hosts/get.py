import argparse
from typing import Generator, List

from probely.cli.renderers import render_output
from probely.cli.tables.extra_hosts_table import ExtraHostTable
from probely.sdk.managers import TargetExtraHostManager
from probely.sdk.models import ExtraHost


def extra_hosts_get_command_handler(args: argparse.Namespace):
    """
    List Extra Hosts for a specified Target.
    """
    target_id = args.target_id
    extra_hosts_ids = args.extra_hosts_ids

    if extra_hosts_ids:
        compound_ids = [
            {"target_id": target_id, "id": extra_host_id}
            for extra_host_id in extra_hosts_ids
        ]
        extra_hosts: List[ExtraHost] = (
            TargetExtraHostManager().unoptimized_get_multiple(compound_ids)
        )
    else:
        extra_hosts: Generator[ExtraHost] = TargetExtraHostManager().list(
            parent_id={"target_id": target_id}
        )

    render_output(records=extra_hosts, table_cls=ExtraHostTable, args=args)
