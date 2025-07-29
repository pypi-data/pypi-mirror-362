from enum import Enum


class AnnotationDateTimeFormat(Enum):
    """An enumeration representing different categories.

    :cvar DMYNUMERICSLASH: "DMY_NUMERIC_SLASH"
    :vartype DMYNUMERICSLASH: str
    :cvar MDYNUMERICSLASH: "MDY_NUMERIC_SLASH"
    :vartype MDYNUMERICSLASH: str
    :cvar YMDNUMERICSLASH: "YMD_NUMERIC_SLASH"
    :vartype YMDNUMERICSLASH: str
    :cvar DMYNUMERICDASHSHORT: "DMY_NUMERIC_DASH_SHORT"
    :vartype DMYNUMERICDASHSHORT: str
    :cvar DMYNUMERICDASH: "DMY_NUMERIC_DASH"
    :vartype DMYNUMERICDASH: str
    :cvar YMDNUMERICDASH: "YMD_NUMERIC_DASH"
    :vartype YMDNUMERICDASH: str
    :cvar MDYTEXTDASHSHORT: "MDY_TEXT_DASH_SHORT"
    :vartype MDYTEXTDASHSHORT: str
    :cvar MDYTEXTSPACESHORT: "MDY_TEXT_SPACE_SHORT"
    :vartype MDYTEXTSPACESHORT: str
    :cvar MDYTEXTSPACE: "MDY_TEXT_SPACE"
    :vartype MDYTEXTSPACE: str
    """

    DMYNUMERICSLASH = "DMY_NUMERIC_SLASH"
    MDYNUMERICSLASH = "MDY_NUMERIC_SLASH"
    YMDNUMERICSLASH = "YMD_NUMERIC_SLASH"
    DMYNUMERICDASHSHORT = "DMY_NUMERIC_DASH_SHORT"
    DMYNUMERICDASH = "DMY_NUMERIC_DASH"
    YMDNUMERICDASH = "YMD_NUMERIC_DASH"
    MDYTEXTDASHSHORT = "MDY_TEXT_DASH_SHORT"
    MDYTEXTSPACESHORT = "MDY_TEXT_SPACE_SHORT"
    MDYTEXTSPACE = "MDY_TEXT_SPACE"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, AnnotationDateTimeFormat._member_map_.values())
        )
