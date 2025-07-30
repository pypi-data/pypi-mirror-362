# coding: utf-8

from __future__ import absolute_import

from datatransfer.source.common.configuration import get_object
from datatransfer.source.configs import DESTINATION_SYSTEM_CODE


rules_name = {
    "KTELABS_CONT": "kte_extractor_mapping_rules",
    "BARS_CONT": "dt_extractor_mapping_rules"
}

try:
    rules = get_object(rules_name[DESTINATION_SYSTEM_CODE])
except KeyError:
    raise ValueError("Unknown DESTINATION_SYSTEM_CODE")
