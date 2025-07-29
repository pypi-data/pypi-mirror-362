import argparse
import logging
from typing import Dict

from probely.cli.common import validate_and_retrieve_yaml_content
from probely.cli.renderers import render_output
from probely.cli.tables.target_extra_hosts_table import TargetExtraHostTable
from probely.sdk.managers import TargetExtraHostManager
from probely.sdk.models import TargetExtraHost

logger = logging.getLogger(__name__)


def generate_payload_from_args(args: argparse.Namespace) -> Dict:
    """
    Generate payload for creating an Extra Host by prioritizing command line arguments
    and using file input as a fallback.
    """
    yaml_file_path = args.yaml_file_path
    file_content = validate_and_retrieve_yaml_content(yaml_file_path)

    command_arguments = {
        "target_id": args.target_id,
        "host": args.host or file_content.get("host"),
        "include": args.include or file_content.get("include"),
        "name": args.name or file_content.get("name"),
        "description": args.description or file_content.get("desc"),
        "file_input": file_content,
    }

    return command_arguments


def extra_hosts_add_command_handler(args: argparse.Namespace):
    payload = generate_payload_from_args(args)

    logger.debug("extra-host `add` extra_payload: {}".format(payload["file_input"]))

    extra_host: TargetExtraHost = TargetExtraHostManager().create(
        target_id=payload["target_id"],
        host=payload["host"],
        include=payload["include"],
        name=payload["name"],
        description=payload["description"],
        skip_reachability_check=args.skip_reachability_check,
        extra_payload=payload["file_input"],
    )

    render_output(records=[extra_host], table_cls=TargetExtraHostTable, args=args)
