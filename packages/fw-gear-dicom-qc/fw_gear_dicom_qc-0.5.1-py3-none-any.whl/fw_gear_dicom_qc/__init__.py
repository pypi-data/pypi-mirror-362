"""The fw_gear_dicom_qc package."""

from importlib import metadata

pkg_name = __package__
try:  # noqa
    __version__ = metadata.version(__package__)
except:  # noqa
    try:
        __version__ = metadata.version(__package__.replace("_", "-"))
    except:  # noqa
        __version__ = "0.1.0"
