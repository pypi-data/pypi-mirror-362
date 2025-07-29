import logging
from typing import Generator, List


from ....exceptions import ProbelyCLIValidation
from ....sdk.managers import TargetManager
from ....sdk.models import Target
from ...commands.targets.schemas import TargetApiFiltersSchema
from ...common import prepare_filters_for_api, validate_and_retrieve_yaml_content
from ...renderers import render_output
from ...tables.targets_table import TargetTable

logger = logging.getLogger(__name__)


def _update_and_render(args, targets_ids, payload):
    if len(targets_ids) == 1:
        updated_targets: List[Target] = [
            TargetManager().update({"id": targets_ids[0]}, payload)
        ]
    else:
        updated_targets: Generator[Target] = TargetManager().bulk_update(
            targets=targets_ids, payload=payload
        )

    render_output(records=updated_targets, table_cls=TargetTable, args=args)


def targets_update_command_handler(args):
    """
    Update targets based on the provided filters or target IDs.
    """
    yaml_file_path = args.yaml_file_path
    if not yaml_file_path:
        raise ProbelyCLIValidation(
            "Path to the YAML file that contains the payload is required."
        )
    payload = validate_and_retrieve_yaml_content(yaml_file_path)

    filters = prepare_filters_for_api(TargetApiFiltersSchema, args)
    targets_ids = args.target_ids

    if not filters and not targets_ids:
        raise ProbelyCLIValidation("either filters or Target IDs must be provided.")

    if filters and targets_ids:
        raise ProbelyCLIValidation("filters and Target IDs are mutually exclusive.")

    logger.debug("Provided content for target update: %s", payload)

    if targets_ids:
        _update_and_render(args, targets_ids, payload)
        return

    # Fetch all Targets that match the filters and update them
    targets_generator: Generator[Target] = TargetManager().list(filters=filters)
    first_target = next(targets_generator, None)

    if not first_target:
        raise ProbelyCLIValidation("Selected Filters returned no results")

    targets_ids = [first_target.id, *[target.id for target in targets_generator]]

    _update_and_render(args, targets_ids, payload)
