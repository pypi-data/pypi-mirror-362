"""Validation module."""

import dataclasses
import logging
import typing as t

import jsonschema

log = logging.getLogger(__name__)


@dataclasses.dataclass
class ValidationErrorReport:  # pragma: no cover
    """Dataclass representing validation error.

    Arguments roughly correspond to jsonschema.exceptions.ValidationError
    See https://python-jsonschema.readthedocs.io/en/stable/errors/ for mor info.

    Args:
        error_type (str): The name of the failed validator
        error_message (str): A human readable message explaining the error.
        error_value (t.Any): The value for the failed validator in the schema.
        error_context (str): If the error was caused by errors in subschemas,
            the list of errors from the subschemas will be available on this
            property. The schema_path and path of these errors will be relative
            to the parent error.
        item (str): Dotty path to the offending element.
        revalidate (bool): Defaults to True
    """

    error_type: str
    error_message: str
    error_value: t.Any
    error_context: t.List
    item: str


def validate_schema(schema: t.Dict) -> bool:
    """Quick validator for input jsonschema.

    Args:
        schema (t.Dict): json-loaded schema

    Returns:
        bool: True or False whether schema is valid
    """
    try:
        jsonschema.Draft7Validator.check_schema(schema)
        return True
    except:  # noqa
        log.error("JSON template invalid.  Please check and try again")
        return False


def validate_header(header: t.Dict, schema: t.Dict) -> t.List[ValidationErrorReport]:
    """Validate file.info.header dictionary against a schema.

    Args:
        header (t.Dict): Contents of file.info.header
        header (t.Dict): Schema to validate against

    Returns:
        t.List[ValidationErrorReport]: List of validation error reports.
    """
    validation_errors = []
    validator = jsonschema.Draft7Validator(schema)
    to_validate = {}
    key = "file.info.header"
    # Try to validate against dicom and dicom array
    if "dicom" in schema.get("properties", "") or "dicom_array" in schema.get(
        "properties", []
    ):
        to_validate = header
    # Otherwise fall back to legacy validation of only info.header.dicom
    else:
        log.info(
            "Did not find 'dicom' or 'dicom_array' in properties, "
            + "falling back to legacy validation"
        )
        key = "file.info.header.dicom"
        to_validate = header.get("dicom", {})
    for error in sorted(validator.iter_errors(to_validate), key=str):
        err_con = ""
        err_val = ""
        if error.absolute_path:
            # Set item to be dotty notation of where error occured in header
            item = error.absolute_path.copy()
            # Absolute path is a deque
            item.appendleft(key)
            item = ".".join([str(val) for val in item])
        else:
            item = key

        if error.context:
            err_con = [con.message for con in error.context]
        if error.validator_value:
            err_val = error.validator_value

        validation_errors.append(
            ValidationErrorReport(
                error_type=error.validator,
                error_message=error.message.replace(",", ""),
                error_value=err_val,
                item=item,
                error_context=err_con,
            )
        )
    return validation_errors
