"""Parser module to parse gear config.json."""

import json
import typing as t
from pathlib import Path

from flywheel_gear_toolkit import GearToolkitContext


def parse_config(
    gear_context: GearToolkitContext,
) -> t.Tuple[t.Dict, t.Dict, t.Dict]:
    """Parse gear config file and returns relevant inputs and config.

    Args:
        gear_context (GearToolkitContext): Context

    Returns:
        t.Tuple[t.Dict, t.Dict, t.Dict]:
            - File info dictionary
            - Loaded schema
            - Rules dictionary in the format <rule>:<bool>
            - DICOM standard string
    """
    dicom = gear_context.get_input("dicom")
    schema = dict()
    schema_path = gear_context.get_input_path("validation-schema")
    # If schema is not provided, fallback to empty json schema
    if not schema_path:
        schema_path = Path(__file__).parents[0] / "empty-json-schema.json"
    with open(schema_path, "r") as fp:
        schema = json.load(fp)

    # Rule values are copied directly from gear config, except debug option.
    rules = gear_context.config.copy()
    rules.pop("debug")
    rules.pop("tag")
    rules.pop("fail_on_critical_error")
    standard = rules.pop("dicom_standard", "current")

    return dicom, schema, rules, standard
