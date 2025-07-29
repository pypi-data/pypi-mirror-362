"""Main module."""

import logging
import shutil
import sys
import tempfile
import typing as t
import zipfile

from fw_file.dicom.config import get_config
from fw_file.dicom.series import DICOMCollection
from fw_utils.files import fileglob

from . import rules, utils, validation

log = logging.getLogger(__name__)


default_rules = [
    "check_series_consistency",
    "check_instance_number_uniqueness",
    "check_embedded_localizer",
    "check_bed_moving",
    "check_slice_consistency",
    "check_dicom_validator",
]


def eval_rules(
    dcms: DICOMCollection, rule_dict: t.Dict[str, bool]
) -> t.List[rules.RuleReport]:
    """Evaluate qc rules on the given file.

    Args:
        file_path (AnyPath): Path to file
        rule_dict (t.Dict[str, bool]): Dictionary of rules and whether or not
            to run them.

    Returns:
        t.List[rules.RuleReport]: Results of evalution of each rule.
    """
    # Evaluate all rules and keep list of reports.
    reports: t.List[rules.RuleReport] = []
    rules_list = [rule for rule, val in rule_dict.items() if val]
    for rule in rules_list:
        rule_fn = getattr(rules, rule)
        result = rule_fn(dcms)
        reports.append(result)

    return reports


def run(dicom: t.Dict, schema: t.Dict, rule_dict: t.Dict, standard: str):
    """Run dicom-qc entrypoint."""
    log.info("Checking format of provided schema")
    if not validation.validate_schema(schema):
        # Exit immediately if schema not valid
        raise ValueError("Schema is not valid")
    log.info("Validating file.info.header")
    validation_results = validation.validate_header(
        dicom.get("object", {}).get("info", {}).get("header", {}), schema
    )
    log.info(f"Setting DICOM standard version: {standard}")
    get_config().standard_rev = standard

    log.info("Determining rules to run.")
    log.info("Evaluating qc rules.")
    dicom_path = dicom.get("location").get("path")
    temp_dir = tempfile.mkdtemp()
    if zipfile.is_zipfile(dicom_path):
        with zipfile.ZipFile(dicom.get("location").get("path")) as zipf:
            zipf.extractall(temp_dir)
        check_0_report = rules.check_0_byte(fileglob(temp_dir, recurse=True))
        dcms = DICOMCollection.from_dir(temp_dir, stop_when=None, force=True)
    else:
        check_0_report = rules.check_0_byte([dicom_path])
        if check_0_report.state != "PASS":
            log.error("Single dicom file 0-byte")
            sys.exit(1)
        dcms = DICOMCollection(dicom_path, stop_when=None, force=True)
    log.info(f"Found {len(dcms)} slices in archive")
    skip = rule_dict.pop("skip_when_4D", True)
    if utils.check_for_4d(dcms) and skip:
        for rule in ["check_bed_moving", "check_slice_consistency"]:
            if rule_dict.get(rule):
                log.warning(
                    f"Input DICOM identified as 4D. {rule} will be skipped, "
                    "as this check does not support 4D DICOM files. "
                    "To configure this gear to not skip this test, "
                    "set `skip_when_4D` config option to False."
                )
                rule_dict[rule] = False
    rule_results = eval_rules(dcms, rule_dict)
    rule_results.append(check_0_report)
    shutil.rmtree(temp_dir)
    validation_results = [result.__dict__ for result in validation_results]
    formatted_results = {}
    for result in rule_results:
        val = result.__dict__
        rule = val.pop("rule")
        formatted_results[rule] = val

    return validation_results, formatted_results
