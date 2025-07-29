from __future__ import annotations
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .recipient_verification_type import RecipientVerificationType


@JsonMap({"type_": "type"})
class RecipientVerification(BaseModel):
    """RecipientVerification

    :param type_: Type of verification the recipient must complete before accessing the envelope. - `PASSCODE`: requires a code to be entered.   - `SMS`: sends a code via SMS.   - `ID_VERIFICATION`: prompts the recipient to complete an automated ID and selfie check., defaults to None
    :type type_: RecipientVerificationType, optional
    :param value: Required for `PASSCODE` and `SMS` verification. - `PASSCODE`: code required by the recipient to sign the document. - `SMS`: recipient's phone number. - `ID_VERIFICATION`: leave empty., defaults to None
    :type value: str, optional
    """

    def __init__(
        self,
        type_: RecipientVerificationType = SENTINEL,
        value: str = SENTINEL,
        **kwargs,
    ):
        """RecipientVerification

        :param type_: Type of verification the recipient must complete before accessing the envelope. - `PASSCODE`: requires a code to be entered.   - `SMS`: sends a code via SMS.   - `ID_VERIFICATION`: prompts the recipient to complete an automated ID and selfie check., defaults to None
        :type type_: RecipientVerificationType, optional
        :param value: Required for `PASSCODE` and `SMS` verification. - `PASSCODE`: code required by the recipient to sign the document. - `SMS`: recipient's phone number. - `ID_VERIFICATION`: leave empty., defaults to None
        :type value: str, optional
        """
        if type_ is not SENTINEL:
            self.type_ = self._enum_matching(
                type_, RecipientVerificationType.list(), "type_"
            )
        if value is not SENTINEL:
            self.value = value
        self._kwargs = kwargs
