import argparse

from probely.cli.commands.targets.add import targets_add_command_handler
from probely.cli.commands.targets.delete import targets_delete_command_handler
from probely.cli.commands.targets.get import targets_get_command_handler
from probely.cli.commands.targets.start_scan import targets_start_scan_command_handler
from probely.cli.commands.targets.update import targets_update_command_handler
from probely.cli.parsers.common import (
    ProbelyArgumentParser,
    build_configs_parser,
    build_file_parser,
    build_output_parser,
    show_help,
)
from probely.cli.parsers.help_texts import (
    FILTERS_GROUP_TITLE,
    SUB_COMMAND_AVAILABLE_ACTIONS_TITLE,
    TARGET_COMMAND_DESCRIPTION_TEXT,
    TARGETS_ADD_COMMAND_DESCRIPTION_TEXT,
    TARGETS_DELETE_COMMAND_DESCRIPTION_TEXT,
    TARGETS_F_SEARCH_TEXT,
    TARGETS_GET_COMMAND_DESCRIPTION_TEXT,
    TARGETS_START_SCAN_COMMAND_DESCRIPTION_TEXT,
    TARGETS_UPDATE_COMMAND_DESCRIPTION_TEXT,
)
from probely.sdk.enums import (
    LogicalOperatorTypeEnum,
    TargetAPISchemaTypeEnum,
    TargetRiskEnum,
    TargetTypeEnum,
)
from probely.settings import FALSY_VALUES, TRUTHY_VALUES


def build_targets_filters_parser() -> argparse.ArgumentParser:
    target_filters_parser = argparse.ArgumentParser(
        description="Filters usable in Targets commands",
        add_help=False,
    )

    target_filters_group = target_filters_parser.add_argument_group(
        title=FILTERS_GROUP_TITLE,
    )

    target_filters_group.add_argument(
        "--f-has-unlimited-scans",
        type=str.upper,
        choices=TRUTHY_VALUES + FALSY_VALUES,
        help="Filter if target has unlimited scans",
        action="store",
    )
    target_filters_group.add_argument(
        "--f-is-url-verified",
        type=str.upper,
        choices=TRUTHY_VALUES + FALSY_VALUES,
        help="Filter targets by verified (true) or not verified (false) domain",
        action="store",
    )
    target_filters_group.add_argument(
        "--f-risk",
        type=str.upper,
        choices=TargetRiskEnum.cli_input_choices(),
        help="Filter targets by risk",
        nargs=argparse.ONE_OR_MORE,
        action="store",
    )
    target_filters_group.add_argument(
        "--f-type",
        type=str.upper,
        choices=TargetTypeEnum.cli_input_choices(),
        help="Filter targets by type",
        nargs=argparse.ONE_OR_MORE,
        action="store",
    )
    target_filters_group.add_argument(
        "--f-search",
        metavar="SEARCH_TERM",
        help=TARGETS_F_SEARCH_TEXT,
        action="store",
    )
    target_filters_group.add_argument(
        "--f-label",
        type=str,
        help="Filter Targets by Targets Label IDs",
        nargs=argparse.ONE_OR_MORE,
        action="store",
    )
    target_filters_group.add_argument(
        "--f-label-logical-operator",
        choices=LogicalOperatorTypeEnum.cli_input_choices(),
        type=str.upper,
        help="Logical operator to apply when filtering labels",
        action="store",
    )

    return target_filters_parser


def build_targets_parser():
    target_filters_parser = build_targets_filters_parser()
    configs_parser = build_configs_parser()
    file_parser = build_file_parser()
    output_parser = build_output_parser()

    targets_parser = ProbelyArgumentParser(
        prog="probely targets",
        add_help=False,
        description=TARGET_COMMAND_DESCRIPTION_TEXT,
    )
    targets_parser.set_defaults(
        command_handler=show_help,
        is_no_action_parser=True,
        parser=targets_parser,
    )

    targets_command_parser = targets_parser.add_subparsers(
        title=SUB_COMMAND_AVAILABLE_ACTIONS_TITLE,
    )

    targets_get_parser = targets_command_parser.add_parser(
        "get",
        help=TARGETS_GET_COMMAND_DESCRIPTION_TEXT,
        parents=[configs_parser, target_filters_parser, output_parser],
    )
    targets_get_parser.add_argument(
        "target_ids",
        metavar="TARGET_ID",
        nargs=argparse.ZERO_OR_MORE,
        help="Identifiers of the targets to list",
        default=None,
    )
    targets_get_parser.set_defaults(
        command_handler=targets_get_command_handler,
        parser=targets_get_parser,
    )

    targets_add_parser = targets_command_parser.add_parser(
        "add",
        help=TARGETS_ADD_COMMAND_DESCRIPTION_TEXT,
        parents=[configs_parser, file_parser, output_parser],
    )
    targets_add_parser.add_argument(
        "target_url",
        metavar="TARGET_URL",
        nargs=argparse.OPTIONAL,
        help="Url of target",
    )
    targets_add_parser.add_argument(
        "--target-name",
        help="Display name of target",
    )
    targets_add_parser.add_argument(
        "--target-type",
        type=str.upper,
        choices=TargetTypeEnum.cli_input_choices(),
        help="Set type of target being add",
    )
    targets_add_parser.add_argument(
        "--api-schema-type",
        type=str.upper,
        choices=TargetAPISchemaTypeEnum.cli_input_choices(),
        help="Type of schema for API Targets",
    )
    targets_add_parser.add_argument(
        "--api-schema-file-url",
        help="URL to download the target's API schema",
    )

    targets_add_parser.add_argument(
        "--api-schema-file",
        metavar="FILE_PATH",
        dest="api_schema_file_path",
        help="File System Path of target's API schema",
    )

    targets_add_parser.set_defaults(
        command_handler=targets_add_command_handler,
        parser=targets_add_parser,
    )

    targets_update_parser = targets_command_parser.add_parser(
        "update",
        help=TARGETS_UPDATE_COMMAND_DESCRIPTION_TEXT,
        parents=[configs_parser, target_filters_parser, file_parser, output_parser],
    )
    targets_update_parser.add_argument(
        "target_ids",
        metavar="TARGET_ID",
        nargs=argparse.ZERO_OR_MORE,
        help="Identifiers of the targets to update",
        default=None,
    )
    targets_update_parser.set_defaults(
        command_handler=targets_update_command_handler,
        parser=targets_update_parser,
    )

    start_scan_parser = targets_command_parser.add_parser(
        "start-scan",
        help=TARGETS_START_SCAN_COMMAND_DESCRIPTION_TEXT,
        parents=[configs_parser, target_filters_parser, file_parser, output_parser],
    )
    start_scan_parser.add_argument(
        "target_ids",
        metavar="TARGET_ID",
        nargs=argparse.ZERO_OR_MORE,
        help="Identifiers of the targets to scan",
        default=None,
    )
    start_scan_parser.set_defaults(
        command_handler=targets_start_scan_command_handler,
        parser=start_scan_parser,
    )

    targets_delete_parser = targets_command_parser.add_parser(
        "delete",
        help=TARGETS_DELETE_COMMAND_DESCRIPTION_TEXT,
        parents=[configs_parser, target_filters_parser],
    )
    targets_delete_parser.add_argument(
        "target_ids",
        metavar="TARGET_ID",
        nargs=argparse.ZERO_OR_MORE,
        help="Identifiers of the targets to delete",
        default=None,
    )
    targets_delete_parser.set_defaults(
        command_handler=targets_delete_command_handler,
        parser=targets_delete_parser,
    )

    return targets_parser
