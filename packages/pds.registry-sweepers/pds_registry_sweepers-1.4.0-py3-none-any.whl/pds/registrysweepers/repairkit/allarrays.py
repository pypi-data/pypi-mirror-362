"""change single strings to array of strings"""
import json
import logging
from typing import Dict

log = logging.getLogger(__name__)

# exclude the following properties from array conversion even if targeted - they are expected to be string-typed
EXCLUDED_PROPERTIES = {
    "lid",
    "vid",
    "lidvid",
    "title",
    "product_class",
    "_package_id",
    "ops:Tracking_Meta/ops:archive_status",
}


def repair(document: Dict, fieldname: str) -> Dict:
    # don't touch the enumerated exclusions, or any registry-sweepers metadata property
    if fieldname in EXCLUDED_PROPERTIES or fieldname.startswith("ops:Provenance"):
        return {}

    if isinstance(document[fieldname], str):
        log.debug(f"found string in doc {document.get('_id')} for field {fieldname} where it should be an array")
        return {fieldname: [document[fieldname]]}
    return {}
