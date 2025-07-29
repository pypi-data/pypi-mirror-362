from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .template_recipient import TemplateRecipient


@JsonMap({})
class TemplateSigningStep(BaseModel):
    """TemplateSigningStep

    :param recipients: List of recipients, defaults to None
    :type recipients: List[TemplateRecipient], optional
    """

    def __init__(self, recipients: List[TemplateRecipient] = SENTINEL, **kwargs):
        """TemplateSigningStep

        :param recipients: List of recipients, defaults to None
        :type recipients: List[TemplateRecipient], optional
        """
        if recipients is not SENTINEL:
            self.recipients = self._define_list(recipients, TemplateRecipient)
        self._kwargs = kwargs
