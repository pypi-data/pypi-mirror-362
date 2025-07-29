from enum import Enum


class EnvelopeOrderField(Enum):
    """An enumeration representing different categories.

    :cvar CREATIONDATE: "CREATION_DATE"
    :vartype CREATIONDATE: str
    :cvar MODIFICATIONDATE: "MODIFICATION_DATE"
    :vartype MODIFICATIONDATE: str
    :cvar NAME: "NAME"
    :vartype NAME: str
    :cvar STATUS: "STATUS"
    :vartype STATUS: str
    :cvar LASTDOCUMENTCHANGE: "LAST_DOCUMENT_CHANGE"
    :vartype LASTDOCUMENTCHANGE: str
    """

    CREATIONDATE = "CREATION_DATE"
    MODIFICATIONDATE = "MODIFICATION_DATE"
    NAME = "NAME"
    STATUS = "STATUS"
    LASTDOCUMENTCHANGE = "LAST_DOCUMENT_CHANGE"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, EnvelopeOrderField._member_map_.values()))
