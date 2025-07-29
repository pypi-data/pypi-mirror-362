from typing import Generator, List

from probely.cli.commands.sequences.schemas import SequenceApiFiltersSchema
from probely.cli.common import prepare_filters_for_api
from probely.cli.renderers import render_output
from probely.cli.tables.sequences_table import SequenceTable
from probely.exceptions import ProbelyCLIValidation
from probely.sdk.managers import TargetSequenceManager
from probely.sdk.models import Sequence


def sequences_get_command_handler(args):
    """
    Lists all target's sequences.
    """
    filters = prepare_filters_for_api(SequenceApiFiltersSchema, args)
    target_id = args.target_id
    sequence_ids = args.sequence_ids

    if filters and sequence_ids:
        raise ProbelyCLIValidation("filters and Sequence IDs are mutually exclusive.")

    if sequence_ids:
        sequences: List[Sequence] = TargetSequenceManager().unoptimized_get_multiple(
            [
                {"target_id": target_id, "id": sequence_id}
                for sequence_id in sequence_ids
            ]
        )
    else:
        sequences: Generator[Sequence] = TargetSequenceManager().list(
            {"target_id": target_id}, filters=filters
        )

    render_output(records=sequences, table_cls=SequenceTable, args=args)
