from enum import Enum


class AnnotationType(Enum):
    """An enumeration representing different categories.

    :cvar TEXT: "TEXT"
    :vartype TEXT: str
    :cvar SIGNATURE: "SIGNATURE"
    :vartype SIGNATURE: str
    :cvar INITIALS: "INITIALS"
    :vartype INITIALS: str
    :cvar CHECKBOX: "CHECKBOX"
    :vartype CHECKBOX: str
    :cvar DATE: "DATE"
    :vartype DATE: str
    """

    TEXT = "TEXT"
    SIGNATURE = "SIGNATURE"
    INITIALS = "INITIALS"
    CHECKBOX = "CHECKBOX"
    DATE = "DATE"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, AnnotationType._member_map_.values()))
