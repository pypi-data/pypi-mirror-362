import argparse
import sys
import textwrap
from datetime import datetime
from typing import Iterable, List, Optional, Type, Union

import yaml
from dateutil import parser
from rich.console import Console

from probely.cli.enums import OutputEnum
from probely.cli.tables.base_table import BaseOutputTable
from probely.constants import (
    TARGET_NEVER_SCANNED_OUTPUT,
    UNKNOWN_VALUE_OUTPUT,
    FALSE_VALUE_OUTPUT,
    TRUE_VALUE_OUTPUT,
    UNKNOWN_LABELS_OUTPUT,
)
from probely.sdk.enums import ProbelyCLIEnum
from probely.sdk.models import SDKModel, Target
from probely.sdk.schemas import FindingLabelDataModel, TargetLabelDataModel
from probely.settings import CLI_DEFAULT_OUTPUT_FORMAT


class OutputRenderer:
    """
    Class responsible for rendering output in various formats (JSON, YAML, TABLE, IDS).
    """

    def __init__(
        self,
        records: Iterable[SDKModel],
        output_type: Optional[OutputEnum],
        console: Console,
        table_cls: Type[BaseOutputTable],
    ):
        self.records = records
        self.table_cls = table_cls
        self.console = console
        self.output_type = output_type

    def render(self) -> None:
        if self.output_type == OutputEnum.JSON:
            self._render_json()
        elif self.output_type == OutputEnum.YAML:
            self._render_yaml()
        elif self.output_type == OutputEnum.IDS_ONLY:
            self._render_ids_only()
        else:
            self._render_table()

    def _render_ids_only(self) -> None:
        for record in self.records:
            self.console.print(record.id)

    def _render_json(self) -> None:
        self.console.print("[")
        first = True
        for record in self.records:
            if not first:
                self.console.print(",")
            self.console.print(record.to_json(indent=2))
            first = False
        self.console.print("]")

    def _render_yaml(self) -> None:
        for record in self.records:
            record_dict = record.to_dict(mode="json")
            self.console.print(yaml.dump([record_dict], indent=2, width=sys.maxsize))

    def _render_table(self) -> None:
        records_iterator = iter(self.records)
        first_record_table = self.table_cls.create_table(show_header=True)

        try:
            first_record = next(records_iterator)
            self.table_cls.add_row(first_record_table, first_record)
        except StopIteration:
            pass

        self.console.print(first_record_table)

        for record in records_iterator:
            table = self.table_cls.create_table(show_header=False)
            self.table_cls.add_row(table, record)
            self.console.print(table)


def render_output(
    records: Iterable[SDKModel],
    args: argparse.Namespace,
    table_cls: Type[BaseOutputTable],
) -> None:
    """
    Helper function to render output without repeating common parameters.
    """
    console = args.console

    default_output_format = OutputEnum[CLI_DEFAULT_OUTPUT_FORMAT]
    output_type = (
        OutputEnum[args.output_format] if args.output_format else default_output_format
    )

    renderer = OutputRenderer(
        records=records,
        output_type=output_type,
        console=console,
        table_cls=table_cls,
    )
    renderer.render()


def get_printable_enum_value(enum: Type[ProbelyCLIEnum], api_enum_value: str) -> str:
    try:
        value_name: str = enum.get_by_api_response_value(api_enum_value).name
        return value_name
    except ValueError:
        return UNKNOWN_VALUE_OUTPUT  # TODO: scenario that risk enum updated but CLI is forgotten


def get_printable_labels(
    labels: List[Union[TargetLabelDataModel, FindingLabelDataModel]] = None,
) -> str:
    if labels is None:
        return UNKNOWN_LABELS_OUTPUT

    labels_names = []
    try:
        for label in labels:
            truncated_label = textwrap.shorten(label.name, width=16, placeholder="...")
            labels_names.append(truncated_label)
    except Exception:
        return UNKNOWN_LABELS_OUTPUT

    printable_labels = ", ".join(labels_names)

    return printable_labels


def get_printable_date(
    date_input: Union[str, datetime, None],
    default_string: Union[str, None] = None,
) -> str:
    if isinstance(date_input, str):
        date_obj = parser.isoparse(date_input)
    elif isinstance(date_input, datetime):
        date_obj = date_input
    else:
        date_obj = None

    if date_obj:
        return date_obj.strftime("%Y-%m-%d %H:%M")

    if default_string:
        return default_string

    return ""


def get_printable_last_scan_date(target: Target) -> str:
    if not target.last_scan:
        return TARGET_NEVER_SCANNED_OUTPUT

    return get_printable_date(target.last_scan.started, TARGET_NEVER_SCANNED_OUTPUT)


def get_printable_boolean(bool_var: bool):
    if bool_var is True:
        return TRUE_VALUE_OUTPUT
    elif bool_var is False:
        return FALSE_VALUE_OUTPUT
    else:
        return UNKNOWN_VALUE_OUTPUT
