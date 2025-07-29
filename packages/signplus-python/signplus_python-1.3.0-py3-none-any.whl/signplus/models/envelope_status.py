from enum import Enum


class EnvelopeStatus(Enum):
    """An enumeration representing different categories.

    :cvar DRAFT: "DRAFT"
    :vartype DRAFT: str
    :cvar INPROGRESS: "IN_PROGRESS"
    :vartype INPROGRESS: str
    :cvar COMPLETED: "COMPLETED"
    :vartype COMPLETED: str
    :cvar EXPIRED: "EXPIRED"
    :vartype EXPIRED: str
    :cvar DECLINED: "DECLINED"
    :vartype DECLINED: str
    :cvar VOIDED: "VOIDED"
    :vartype VOIDED: str
    :cvar PENDING: "PENDING"
    :vartype PENDING: str
    """

    DRAFT = "DRAFT"
    INPROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    EXPIRED = "EXPIRED"
    DECLINED = "DECLINED"
    VOIDED = "VOIDED"
    PENDING = "PENDING"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, EnvelopeStatus._member_map_.values()))
