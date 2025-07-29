from __future__ import annotations
from typing import List
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .template_signing_step import TemplateSigningStep


@JsonMap({})
class AddTemplateSigningStepsRequest(BaseModel):
    """AddTemplateSigningStepsRequest

    :param signing_steps: List of signing steps
    :type signing_steps: List[TemplateSigningStep]
    """

    def __init__(self, signing_steps: List[TemplateSigningStep], **kwargs):
        """AddTemplateSigningStepsRequest

        :param signing_steps: List of signing steps
        :type signing_steps: List[TemplateSigningStep]
        """
        self.signing_steps = self._define_list(signing_steps, TemplateSigningStep)
        self._kwargs = kwargs
