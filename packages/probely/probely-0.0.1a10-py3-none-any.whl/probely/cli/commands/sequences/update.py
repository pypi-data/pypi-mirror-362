import json
import logging
from typing import Dict, List

from ....exceptions import ProbelyCLIValidation, ProbelyObjectsNotFound
from ....sdk.managers import TargetSequenceManager
from ....sdk.models import Sequence
from ...commands.sequences.schemas import SequenceApiFiltersSchema
from ...common import prepare_filters_for_api, validate_and_retrieve_yaml_content
from ...renderers import render_output
from ...tables.sequences_table import SequenceTable

logger = logging.getLogger(__name__)


def _update_and_render(args, target_id, sequence_ids, payload):
    updated_sequences: List[Sequence] = [
        TargetSequenceManager().update(
            {"target_id": target_id, "id": sequence_id}, payload
        )
        for sequence_id in sequence_ids
    ]

    render_output(records=updated_sequences, table_cls=SequenceTable, args=args)


def sequences_update_command_handler(args):
    """
    Update sequences based on the provided filters or sequence IDs.
    """
    yaml_file_path = args.yaml_file_path
    payload = validate_and_retrieve_yaml_content(yaml_file_path)

    filters = prepare_filters_for_api(SequenceApiFiltersSchema, args)
    target_id = args.target_id
    sequence_ids = args.sequence_ids

    if not filters and not sequence_ids:
        raise ProbelyCLIValidation("either filters or Sequence IDs must be provided.")

    if filters and sequence_ids:
        raise ProbelyCLIValidation("filters and Sequence IDs are mutually exclusive.")

    logger.debug("Provided content for sequence update: %s", payload)

    sequence_steps_file_path = payload.pop("content", None)

    if sequence_steps_file_path:
        with open(sequence_steps_file_path, "r") as f:
            try:
                sequence_steps: List[Dict] = json.load(f)
            except json.decoder.JSONDecodeError:
                raise ProbelyCLIValidation("Provided file has invalid JSON content")

        payload["content"] = json.dumps(sequence_steps)

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

    _update_and_render(args, target_id, sequence_ids, payload)
