# Defines constants used for versioning updated documents with the in-use version of sweepers
# SWEEPERS_VERSION must be incremented any time sweepers is changed in a way which requires reprocessing of
# previously-processed data
from pds.registrysweepers.utils.misc import get_sweeper_version_metadata_key

SWEEPERS_REPAIRKIT_VERSION = 3
SWEEPERS_REPAIRKIT_VERSION_METADATA_KEY = get_sweeper_version_metadata_key("repairkit")
