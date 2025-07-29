import argparse
from itertools import chain
from typing import Generator, Iterable

from probely import TargetExtraHost
from probely.cli.commands.target_extra_hosts.schemas import (
    TargetExtraHostsApiFiltersSchema,
)
from probely.cli.common import prepare_filters_for_api
from probely.exceptions import ProbelyCLIValidation, ProbelyCLIFiltersNoResultsException
from probely.sdk.managers import TargetExtraHostManager


def target_extra_hosts_delete_command_handler(args: argparse.Namespace):
    filters = prepare_filters_for_api(TargetExtraHostsApiFiltersSchema, args)
    target_extra_hosts_ids = args.extra_hosts_ids

    if not filters and not target_extra_hosts_ids:
        raise ProbelyCLIValidation(
            "either filters or Target Extra Hosts IDs must be provided."
        )

    if filters and target_extra_hosts_ids:
        raise ProbelyCLIValidation(
            "filters and Target Extra Hosts IDs are mutually exclusive."
        )

    target_extra_hosts: Iterable = []

    if filters:
        filtered_target_extra_hosts: Generator[TargetExtraHost] = (
            TargetExtraHostManager().list(filters=filters)
        )
        first_extra_host = next(filtered_target_extra_hosts, None)

        if not first_extra_host:
            raise ProbelyCLIFiltersNoResultsException()

        target_extra_hosts: Iterable = chain(
            [first_extra_host],
            filtered_target_extra_hosts,
        )
    else:
        target_extra_hosts: Generator[TargetExtraHost] = (
            TargetExtraHostManager().retrieve_multiple(target_extra_hosts_ids)
        )

    for target_extra_host in target_extra_hosts:
        TargetExtraHostManager().delete(
            parent_id=target_extra_host.target.id, entity_id=target_extra_host.id
        )
        args.console.print(target_extra_host.id)
