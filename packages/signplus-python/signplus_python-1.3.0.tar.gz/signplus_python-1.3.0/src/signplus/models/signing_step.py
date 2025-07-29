from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .recipient import Recipient


@JsonMap({})
class SigningStep(BaseModel):
    """SigningStep

    :param recipients: List of recipients, defaults to None
    :type recipients: List[Recipient], optional
    """

    def __init__(self, recipients: List[Recipient] = SENTINEL, **kwargs):
        """SigningStep

        :param recipients: List of recipients, defaults to None
        :type recipients: List[Recipient], optional
        """
        if recipients is not SENTINEL:
            self.recipients = self._define_list(recipients, Recipient)
        self._kwargs = kwargs
