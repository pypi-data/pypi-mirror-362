from enum import Enum


class AnnotationFontFamily(Enum):
    """An enumeration representing different categories.

    :cvar UNKNOWN: "UNKNOWN"
    :vartype UNKNOWN: str
    :cvar SERIF: "SERIF"
    :vartype SERIF: str
    :cvar SANS: "SANS"
    :vartype SANS: str
    :cvar MONO: "MONO"
    :vartype MONO: str
    """

    UNKNOWN = "UNKNOWN"
    SERIF = "SERIF"
    SANS = "SANS"
    MONO = "MONO"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, AnnotationFontFamily._member_map_.values()))
