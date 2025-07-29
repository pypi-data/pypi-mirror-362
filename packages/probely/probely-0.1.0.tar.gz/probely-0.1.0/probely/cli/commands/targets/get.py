from typing import Generator

from probely.cli.commands.targets.schemas import TargetApiFiltersSchema
from probely.cli.common import prepare_filters_for_api
from probely.cli.renderers import render_output
from probely.cli.tables.targets_table import TargetTable
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.managers import TargetManager
from probely.sdk.models import Target


def targets_get_command_handler(args):
    """
    Lists all accessible targets of client
    """
    filters = prepare_filters_for_api(TargetApiFiltersSchema, args)
    targets_ids = args.target_ids

    if filters and targets_ids:
        raise ProbelyCLIValidation("filters and Target IDs are mutually exclusive.")

    if targets_ids:
        targets: Generator[Target] = TargetManager().retrieve_multiple(targets_ids)
    else:
        targets: Generator[Target] = TargetManager().list(filters=filters)

    render_output(records=targets, table_cls=TargetTable, args=args)
