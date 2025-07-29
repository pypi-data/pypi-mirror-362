import argparse
from typing import Generator

from probely.cli.commands.target_extra_hosts.schemas import (
    TargetExtraHostsApiFiltersSchema,
)
from probely.cli.common import prepare_filters_for_api
from probely.cli.renderers import render_output
from probely.cli.tables.target_extra_hosts_table import TargetExtraHostTable
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.managers import TargetExtraHostManager
from probely.sdk.models import TargetExtraHost


def target_extra_hosts_get_command_handler(args: argparse.Namespace):
    filters = prepare_filters_for_api(TargetExtraHostsApiFiltersSchema, args)
    target_extra_hosts_ids = args.extra_hosts_ids

    if filters and target_extra_hosts_ids:
        raise ProbelyCLIValidation(
            "filters and Target Extra Hosts IDs are mutually exclusive."
        )

    if target_extra_hosts_ids:
        target_extra_hosts: Generator[TargetExtraHost] = (
            TargetExtraHostManager().retrieve_multiple(target_extra_hosts_ids)
        )
    else:
        target_extra_hosts: Generator[TargetExtraHost] = TargetExtraHostManager().list(
            filters=filters
        )

    render_output(records=target_extra_hosts, table_cls=TargetExtraHostTable, args=args)
