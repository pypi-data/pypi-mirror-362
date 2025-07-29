from enum import Enum


class WebhookEvent(Enum):
    """An enumeration representing different categories.

    :cvar ENVELOPEEXPIRED: "ENVELOPE_EXPIRED"
    :vartype ENVELOPEEXPIRED: str
    :cvar ENVELOPEDECLINED: "ENVELOPE_DECLINED"
    :vartype ENVELOPEDECLINED: str
    :cvar ENVELOPEVOIDED: "ENVELOPE_VOIDED"
    :vartype ENVELOPEVOIDED: str
    :cvar ENVELOPECOMPLETED: "ENVELOPE_COMPLETED"
    :vartype ENVELOPECOMPLETED: str
    :cvar ENVELOPEAUDITTRAIL: "ENVELOPE_AUDIT_TRAIL"
    :vartype ENVELOPEAUDITTRAIL: str
    """

    ENVELOPEEXPIRED = "ENVELOPE_EXPIRED"
    ENVELOPEDECLINED = "ENVELOPE_DECLINED"
    ENVELOPEVOIDED = "ENVELOPE_VOIDED"
    ENVELOPECOMPLETED = "ENVELOPE_COMPLETED"
    ENVELOPEAUDITTRAIL = "ENVELOPE_AUDIT_TRAIL"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, WebhookEvent._member_map_.values()))
