from __future__ import annotations
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .recipient_role import RecipientRole
from .recipient_verification import RecipientVerification


@JsonMap({"id_": "id"})
class Recipient(BaseModel):
    """Recipient

    :param id_: Unique identifier of the recipient, defaults to None
    :type id_: str, optional
    :param uid: Unique identifier of the user associated with the recipient, defaults to None
    :type uid: str, optional
    :param name: Name of the recipient
    :type name: str
    :param email: Email of the recipient
    :type email: str
    :param role: Role of the recipient (SIGNER signs the document, RECEIVES_COPY receives a copy of the document, IN_PERSON_SIGNER signs the document in person, SENDER sends the document)
    :type role: RecipientRole
    :param verification: verification, defaults to None
    :type verification: RecipientVerification, optional
    """

    def __init__(
        self,
        name: str,
        email: str,
        role: RecipientRole,
        id_: str = SENTINEL,
        uid: str = SENTINEL,
        verification: RecipientVerification = SENTINEL,
        **kwargs,
    ):
        """Recipient

        :param id_: Unique identifier of the recipient, defaults to None
        :type id_: str, optional
        :param uid: Unique identifier of the user associated with the recipient, defaults to None
        :type uid: str, optional
        :param name: Name of the recipient
        :type name: str
        :param email: Email of the recipient
        :type email: str
        :param role: Role of the recipient (SIGNER signs the document, RECEIVES_COPY receives a copy of the document, IN_PERSON_SIGNER signs the document in person, SENDER sends the document)
        :type role: RecipientRole
        :param verification: verification, defaults to None
        :type verification: RecipientVerification, optional
        """
        if id_ is not SENTINEL:
            self.id_ = id_
        if uid is not SENTINEL:
            self.uid = uid
        self.name = name
        self.email = email
        self.role = self._enum_matching(role, RecipientRole.list(), "role")
        if verification is not SENTINEL:
            self.verification = self._define_object(verification, RecipientVerification)
        self._kwargs = kwargs
