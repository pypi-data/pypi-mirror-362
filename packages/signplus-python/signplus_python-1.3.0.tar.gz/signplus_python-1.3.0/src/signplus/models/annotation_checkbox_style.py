from enum import Enum


class AnnotationCheckboxStyle(Enum):
    """An enumeration representing different categories.

    :cvar CIRCLECHECK: "CIRCLE_CHECK"
    :vartype CIRCLECHECK: str
    :cvar CIRCLEFULL: "CIRCLE_FULL"
    :vartype CIRCLEFULL: str
    :cvar SQUARECHECK: "SQUARE_CHECK"
    :vartype SQUARECHECK: str
    :cvar SQUAREFULL: "SQUARE_FULL"
    :vartype SQUAREFULL: str
    :cvar CHECKMARK: "CHECK_MARK"
    :vartype CHECKMARK: str
    :cvar TIMESSQUARE: "TIMES_SQUARE"
    :vartype TIMESSQUARE: str
    """

    CIRCLECHECK = "CIRCLE_CHECK"
    CIRCLEFULL = "CIRCLE_FULL"
    SQUARECHECK = "SQUARE_CHECK"
    SQUAREFULL = "SQUARE_FULL"
    CHECKMARK = "CHECK_MARK"
    TIMESSQUARE = "TIMES_SQUARE"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, AnnotationCheckboxStyle._member_map_.values())
        )
