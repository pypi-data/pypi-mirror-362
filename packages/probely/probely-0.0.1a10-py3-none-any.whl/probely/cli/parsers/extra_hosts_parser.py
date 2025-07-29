import argparse

from probely.cli.commands.extra_hosts.add import extra_hosts_add_command_handler
from probely.cli.commands.extra_hosts.delete import extra_hosts_delete_command_handler
from probely.cli.commands.extra_hosts.get import extra_hosts_get_command_handler
from probely.cli.commands.extra_hosts.update import extra_hosts_update_command_handler
from probely.cli.parsers.common import (
    ProbelyArgumentParser,
    build_configs_parser,
    build_file_parser,
    build_output_parser,
    show_help,
)
from probely.cli.parsers.help_texts import (
    EXTRA_HOSTS_ADD_COMMAND_DESCRIPTION_TEXT,
    EXTRA_HOSTS_COMMAND_DESCRIPTION_TEXT,
    EXTRA_HOSTS_DELETE_COMMAND_DESCRIPTION_TEXT,
    EXTRA_HOSTS_GET_COMMAND_DESCRIPTION_TEXT,
    EXTRA_HOSTS_UPDATE_COMMAND_DESCRIPTION_TEXT,
    SUB_COMMAND_AVAILABLE_ACTIONS_TITLE,
)
from probely.settings import FALSY_VALUES, TRUTHY_VALUES


def build_target_extra_hosts_parser():
    # NOTE: filters for Extra Hosts are not implemented on API side
    configs_parser = build_configs_parser()
    file_parser = build_file_parser()
    output_parser = build_output_parser()

    extra_hosts_parser = ProbelyArgumentParser(
        prog="probely target-extra-hosts",
        add_help=False,
        description=EXTRA_HOSTS_COMMAND_DESCRIPTION_TEXT,
    )
    extra_hosts_parser.set_defaults(
        command_handler=show_help,
        is_no_action_parser=True,
        parser=extra_hosts_parser,
    )

    extra_hosts_command_parser = extra_hosts_parser.add_subparsers(
        title=SUB_COMMAND_AVAILABLE_ACTIONS_TITLE,
    )

    extra_hosts_get_parser = extra_hosts_command_parser.add_parser(
        "get",
        help=EXTRA_HOSTS_GET_COMMAND_DESCRIPTION_TEXT,
        parents=[configs_parser, output_parser],
    )
    extra_hosts_get_parser.add_argument(
        "target_id",
        metavar="TARGET_ID",
        help="Identifier of the Target",
    )
    extra_hosts_get_parser.add_argument(
        "extra_hosts_ids",
        metavar="EXTRA_HOST_ID",
        nargs=argparse.ZERO_OR_MORE,
        help="Identifier of the Extra Host",
        default=None,
    )
    extra_hosts_get_parser.set_defaults(
        command_handler=extra_hosts_get_command_handler,
        parser=extra_hosts_get_parser,
    )

    extra_hosts_add_parser = extra_hosts_command_parser.add_parser(
        "add",
        help=EXTRA_HOSTS_ADD_COMMAND_DESCRIPTION_TEXT,
        parents=[configs_parser, file_parser, output_parser],
    )
    extra_hosts_add_parser.add_argument(
        "target_id",
        metavar="TARGET_ID",
        help="Identifier of the Target",
    )
    extra_hosts_add_parser.add_argument(
        "--host",
        help="Extra host to be added",
    )
    extra_hosts_add_parser.add_argument(
        "--include",
        type=str.upper,
        choices=TRUTHY_VALUES + FALSY_VALUES,
        help="Include the extra host in the scope of the scan",
    )
    extra_hosts_add_parser.add_argument(
        "--name",
        help="Display name of the extra host",
    )
    extra_hosts_add_parser.add_argument(
        "--desc",
        help="Description of the extra host",
    )
    extra_hosts_add_parser.set_defaults(
        command_handler=extra_hosts_add_command_handler,
        parser=extra_hosts_add_parser,
    )

    extra_hosts_update_parser = extra_hosts_command_parser.add_parser(
        "update",
        help=EXTRA_HOSTS_UPDATE_COMMAND_DESCRIPTION_TEXT,
        parents=[configs_parser, file_parser, output_parser],
    )
    extra_hosts_update_parser.add_argument(
        "target_id",
        metavar="TARGET_ID",
        help="Identifier of the Target",
    )
    extra_hosts_update_parser.add_argument(
        "extra_hosts_ids",
        metavar="EXTRA_HOST_ID",
        nargs=argparse.ONE_OR_MORE,
        help="Identifiers of the Extra Hosts to update",
    )
    extra_hosts_update_parser.add_argument(
        "--include",
        type=str.upper,
        choices=TRUTHY_VALUES + FALSY_VALUES,
        help="Include the extra host in the scope of the scan",
    )
    extra_hosts_update_parser.add_argument(
        "--name",
        help="Display name of the extra host",
    )
    extra_hosts_update_parser.add_argument(
        "--desc",
        help="Description of the extra host",
    )
    extra_hosts_update_parser.set_defaults(
        command_handler=extra_hosts_update_command_handler,
        parser=extra_hosts_update_parser,
    )

    extra_hosts_delete_parser = extra_hosts_command_parser.add_parser(
        "delete",
        help=EXTRA_HOSTS_DELETE_COMMAND_DESCRIPTION_TEXT,
        parents=[configs_parser],
    )
    extra_hosts_delete_parser.add_argument(
        "target_id",
        metavar="TARGET_ID",
        help="Identifier of the Target",
    )
    extra_hosts_delete_parser.add_argument(
        "extra_hosts_ids",
        metavar="EXTRA_HOST_ID",
        nargs=argparse.ONE_OR_MORE,
        help="Identifiers of the Extra Hosts to delete",
        default=None,
    )
    extra_hosts_delete_parser.set_defaults(
        command_handler=extra_hosts_delete_command_handler,
        parser=extra_hosts_delete_parser,
    )

    return extra_hosts_parser
