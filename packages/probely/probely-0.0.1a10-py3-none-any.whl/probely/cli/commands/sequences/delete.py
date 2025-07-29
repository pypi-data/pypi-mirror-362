from typing import List

from probely.cli.commands.sequences.schemas import SequenceApiFiltersSchema
from probely.cli.common import prepare_filters_for_api
from probely.exceptions import ProbelyCLIValidation, ProbelyObjectsNotFound
from probely.sdk.managers import TargetSequenceManager
from probely.sdk.models import Sequence


def sequences_delete_command_handler(args):
    filters = prepare_filters_for_api(SequenceApiFiltersSchema, args)
    target_id = args.target_id
    sequence_ids = args.sequence_ids

    if not filters and not sequence_ids:
        raise ProbelyCLIValidation("either filters or Sequence IDs must be provided.")

    if filters and sequence_ids:
        raise ProbelyCLIValidation("Filters and Sequence IDs are mutually exclusive.")

    if sequence_ids:
        invalid_sequence_ids = []
        for sequence_id in sequence_ids:
            try:
                TargetSequenceManager().retrieve(
                    {"target_id": target_id, "id": sequence_id}
                )
            except ProbelyObjectsNotFound:
                invalid_sequence_ids.append(sequence_id)

        if invalid_sequence_ids:
            raise ProbelyCLIValidation(f"Invalid Sequence IDs: {invalid_sequence_ids}.")
    else:
        sequences: List[Sequence] = list(
            TargetSequenceManager().list({"target_id": target_id}, filters=filters)
        )
        sequence_ids = [sequence.id for sequence in sequences]

        if len(sequence_ids) == 0:
            raise ProbelyCLIValidation("Selected filters returned no results")

    for sequence_id in sequence_ids:
        TargetSequenceManager().delete({"target_id": target_id, "id": sequence_id})

    for sequence_id in sequence_ids:
        args.console.print(sequence_id)
