from enum import Enum


class RecipientVerificationType(Enum):
    """An enumeration representing different categories.

    :cvar SMS: "SMS"
    :vartype SMS: str
    :cvar PASSCODE: "PASSCODE"
    :vartype PASSCODE: str
    :cvar IDVERIFICATION: "ID_VERIFICATION"
    :vartype IDVERIFICATION: str
    """

    SMS = "SMS"
    PASSCODE = "PASSCODE"
    IDVERIFICATION = "ID_VERIFICATION"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(
            map(lambda x: x.value, RecipientVerificationType._member_map_.values())
        )
