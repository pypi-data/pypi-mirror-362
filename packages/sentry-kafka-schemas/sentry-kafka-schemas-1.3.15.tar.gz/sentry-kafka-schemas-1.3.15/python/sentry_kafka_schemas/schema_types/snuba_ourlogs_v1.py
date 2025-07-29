from typing import Union, Required, Dict, TypedDict


class OurlogEvent(TypedDict, total=False):
    """ ourlog_event. """

    organization_id: Required["_Uint"]
    """
    minimum: 0

    Required property
    """

    project_id: Required["_Uint"]
    """
    minimum: 0

    Required property
    """

    trace_id: "_Uuid"
    """
    minLength: 32
    maxLength: 36
    """

    trace_flags: "_Uint8"
    """
    minimum: 0
    maximum: 255
    """

    timestamp_nanos: Required["_Uint"]
    """
    minimum: 0

    Required property
    """

    retention_days: Required["_Uint16"]
    """
    minimum: 0
    maximum: 65535

    Required property
    """

    observed_timestamp_nanos: Required["_Uint"]
    """
    minimum: 0

    Required property
    """

    body: Required[str]
    """
    The body of the log.

    Required property
    """

    severity_text: str
    """ The name of the severity level (e.g., WARNING) """

    severity_number: "_Uint8"
    """
    minimum: 0
    maximum: 255
    """

    attributes: Dict[str, "_OurlogEventAttributesAdditionalproperties"]
    """ key-value tag pairs on this log """



class _OurlogEventAttributesAdditionalproperties(TypedDict, total=False):
    """
    minProperties: 1
    maxProperties: 1
    """

    string_value: str
    int_value: int
    double_value: Union[int, float]
    bool_value: bool


_Uint = int
""" minimum: 0 """



_Uint16 = int
"""
minimum: 0
maximum: 65535
"""



_Uint8 = int
"""
minimum: 0
maximum: 255
"""



_Uuid = str
"""
minLength: 32
maxLength: 36
"""

