import argparse
import logging
from typing import Dict, List

from probely.cli.common import validate_and_retrieve_yaml_content
from probely.cli.renderers import render_output
from probely.cli.tables.extra_hosts_table import ExtraHostTable
from probely.exceptions import ProbelyCLIValidation, ProbelyObjectsNotFound
from probely.sdk.managers import TargetExtraHostManager
from probely.sdk.models import ExtraHost

logger = logging.getLogger(__name__)


def _validate_extra_hosts_ids(target_id, extra_hosts_ids):
    # NOTE: This will be removed when custom ID 404 validation
    # becomes supported for Extra Hosts on API
    invalid_extra_hosts_ids = []
    for extra_host_id in extra_hosts_ids:
        try:
            TargetExtraHostManager().retrieve(
                {"target_id": target_id, "id": extra_host_id}
            )
        except ProbelyObjectsNotFound:
            invalid_extra_hosts_ids.append(extra_host_id)

    if invalid_extra_hosts_ids:
        raise ProbelyCLIValidation(
            f"Invalid Extra Host IDs: {invalid_extra_hosts_ids}."
        )


def generate_payload_from_args(args: argparse.Namespace) -> Dict:
    """
    Generate payload for updating an Extra Host by prioritizing CL args
    and using file input as a fallback. Only include fields that are specified.
    """
    yaml_file_path = args.yaml_file_path
    file_content = validate_and_retrieve_yaml_content(yaml_file_path)

    payload = {}

    # Check each argument and add to payload if it is specified
    if args.include or "include" in file_content:
        payload["include"] = args.include or file_content.get("include")
    if args.name or "name" in file_content:
        payload["name"] = args.name or file_content.get("name")
    if args.desc or "desc" in file_content:
        payload["desc"] = args.desc or file_content.get("desc")

    # Headers and cookies could not be specified in the CL, but only in the file
    if "headers" in file_content:
        payload["headers"] = file_content["headers"]
    if "cookies" in file_content:
        payload["cookies"] = file_content["cookies"]

    return payload


def extra_hosts_update_command_handler(args: argparse.Namespace):
    target_id = args.target_id
    extra_hosts_ids = args.extra_hosts_ids
    _validate_extra_hosts_ids(target_id, extra_hosts_ids)

    payload = generate_payload_from_args(args)

    updated_extra_hosts: List[ExtraHost] = [
        TargetExtraHostManager().update(
            {"target_id": target_id, "id": extra_host_id}, payload
        )
        for extra_host_id in extra_hosts_ids
    ]

    render_output(records=updated_extra_hosts, table_cls=ExtraHostTable, args=args)
