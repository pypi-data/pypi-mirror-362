"""Utilities module for fw_gear_dicom_qc."""

import logging
from collections import Counter

from flywheel_gear_toolkit import GearToolkitContext
from fw_file.dicom import DICOMCollection

log = logging.getLogger(__name__)


def update_metadata(
    context: GearToolkitContext, rule_results: dict, validation_results: list
):
    """Update qc metadata given results."""
    input_ = context.get_input("dicom")
    for name, res in rule_results.items():
        context.metadata.add_qc_result(
            input_, name, state=res.get("state", "FAIL"), data=res.get("data")
        )
    context.metadata.add_qc_result(
        input_,
        "jsonschema-validation",
        state=("PASS" if not len(validation_results) else "FAIL"),
        data=validation_results,
    )


def check_for_4d(dcms: DICOMCollection) -> bool:
    """Checks a few DICOM tags that indicate multiple temporal positions (4D DICOM).

    Args:
        dcms: DICOMCollection to be checked

    Returns:
        bool: Whether the DICOM is determined to be 4D
    """
    res = False
    log.info("Checking for whether input DICOM is 4D...")
    # Because one or more tags could indicate that the DICOM series contains
    # multiple temporal series, the following checks each possibly-existing tag
    # independently for maximum information instead of returning as soon as it
    # finds one tag that indicates temporal spacing.

    # ImagePositionPatient: if ALL IPP values are duplicated one or more times,
    # log that DICOM appears to be 4D due to duplicate sets of IPP values and
    # handle as 4D
    ipp_count = Counter([str(ipp) for ipp in dcms.bulk_get("ImagePositionPatient")])
    ipp_nums = set([n for ipp, n in ipp_count.items()])
    if len(ipp_nums) == 1 and ipp_nums.pop() > 1:
        # All IPP values appear the same number of times and appear more than once
        res = True
        log.info(
            "In checking ImagePositionPatient, all IPP values are duplicated equally "
            "throughout the DICOM. This may indicate that the DICOM is 4D."
        )

    potential_tags = [
        # Public Tags
        "AcquisitionNumber",  # Optional
        "EchoTime",  # MR Required, empty if unknown
        "EchoNumbers",  # Optional
        "InversionTime",  # Conditionally Required, empty if unknown
        "RepetitionTime",  # Conditionally required, empty if unknown
        "TriggerTime",  # Conditionally required, empty if unknown
        "DiffusionBValue",  # Conditionally required
        "DiffusionGradientOrientation",  # Conditionally required
        "DimensionIndexValues",  # Conditionally required, paired with DimensionIndexSequence
        # Private Tags
        0x0021105E,  # GE: RTIA Timer 0021 105E
        0x0043102C,  # GE: Effective Echo Spacing 0043 102C
        0x0065102C,  # UIH: RepetitionIndex 0065 102C
        0x20051412,  # Philips: B-value Index 2005 1412
        0x20051413,  # Philips: Gradient Direction Number 2005 1413
        0x20051595,  # Philips: DIFFUSION2_KDTI 2005 1595
        0x20051599,  # Philips: NR_OF_DIFFUSION_ORDER 2005 1599
        0x20051596,  # Philips: DIFFUSION_ORDER 2005, 1596
    ]

    for tag in potential_tags:
        bulk = dcms.bulk_get(tag)
        if isinstance(bulk[0], list):
            bulk = [tuple(x) for x in bulk]
        vals = set(bulk)
        if len(vals) > 1:
            res = True
            log.info(
                f"In checking {tag}, {len(vals)} unique values identified. "
                f"This may indicate that the DICOM series could be split on {tag}."
            )

    if dcms.get("NumberOfTemporalPositions"):
        # NumberOfTemporalPositions is optional, as is TemporalPositionIdentifier.
        temporal_pos = dcms.get("NumberOfTemporalPositions")
        if temporal_pos > 1:
            res = True
            # Check if splitting by temporal position could be available
            temporal_pos_nums = set(dcms.bulk_get("TemporalPositionIdentifier"))
            if temporal_pos == len(temporal_pos_nums):
                log.info(
                    "In checking NumberOfTemporalPositions and TemporalPositionIdentifier,"
                    f"{temporal_pos} temporal positions identified. This may indicate that"
                    "the DICOM series could be split on TemporalPositionIdentifier."
                )

    return res
