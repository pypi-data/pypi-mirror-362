import argparse
from itertools import chain
from pathlib import Path
from typing import Type, Union, Generator, Iterable

import marshmallow
import yaml

import probely.settings as settings
from probely.exceptions import ProbelyCLIValidation, ProbelyCLIFiltersNoResultsException


def validate_and_retrieve_yaml_content(yaml_file_path: Union[str, None]):
    if not yaml_file_path:
        return dict()

    file_path = Path(yaml_file_path)

    if not file_path.exists():
        raise ProbelyCLIValidation("Provided path does not exist: {}".format(file_path))

    if not file_path.is_file():
        raise ProbelyCLIValidation(
            "Provided path is not a file: {}".format(file_path.absolute())
        )

    if file_path.suffix not in settings.CLI_ACCEPTED_FILE_EXTENSIONS:
        raise ProbelyCLIValidation(
            "Invalid file extension, must be one of the following: {}:".format(
                settings.CLI_ACCEPTED_FILE_EXTENSIONS
            )
        )

    with file_path.open() as yaml_file:
        try:
            # TODO: supported yaml versions?
            yaml_content = yaml.safe_load(yaml_file)
            if yaml_content is None:
                raise ProbelyCLIValidation("YAML file {} is empty.".format(file_path))
        except yaml.error.YAMLError as ex:
            raise ProbelyCLIValidation("Invalid yaml content in file: {}".format(ex))

    return yaml_content


def validate_empty_results_generator(results_generator: Generator) -> Iterable:
    first_result = next(results_generator, None)

    if first_result is None:
        raise ProbelyCLIFiltersNoResultsException()

    return chain([first_result], results_generator)


def prepare_filters_for_api(
    schema: Type[marshmallow.Schema], args: argparse.Namespace
) -> dict:
    """
    Prepares and validates filters using the provided Marshmallow schema.
    """
    filters_schema = schema()
    try:
        filters = filters_schema.load(vars(args))
        return filters
    except marshmallow.ValidationError as ex:
        raise ProbelyCLIValidation(f"Invalid filters: {ex}")
