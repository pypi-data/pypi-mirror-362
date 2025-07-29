from enum import Enum


class EnvelopeLegalityLevel(Enum):
    """An enumeration representing different categories.

    :cvar SES: "SES"
    :vartype SES: str
    :cvar QESEIDAS: "QES_EIDAS"
    :vartype QESEIDAS: str
    :cvar QESZERTES: "QES_ZERTES"
    :vartype QESZERTES: str
    """

    SES = "SES"
    QESEIDAS = "QES_EIDAS"
    QESZERTES = "QES_ZERTES"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, EnvelopeLegalityLevel._member_map_.values()))
