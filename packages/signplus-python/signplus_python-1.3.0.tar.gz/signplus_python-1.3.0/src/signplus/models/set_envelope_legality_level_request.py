from __future__ import annotations
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .envelope_legality_level import EnvelopeLegalityLevel


@JsonMap({})
class SetEnvelopeLegalityLevelRequest(BaseModel):
    """SetEnvelopeLegalityLevelRequest

    :param legality_level: Legal level of the envelope (SES is Simple Electronic Signature, QES_EIDAS is Qualified Electronic Signature, QES_ZERTES is Qualified Electronic Signature with Zertes), defaults to None
    :type legality_level: EnvelopeLegalityLevel, optional
    """

    def __init__(self, legality_level: EnvelopeLegalityLevel = SENTINEL, **kwargs):
        """SetEnvelopeLegalityLevelRequest

        :param legality_level: Legal level of the envelope (SES is Simple Electronic Signature, QES_EIDAS is Qualified Electronic Signature, QES_ZERTES is Qualified Electronic Signature with Zertes), defaults to None
        :type legality_level: EnvelopeLegalityLevel, optional
        """
        if legality_level is not SENTINEL:
            self.legality_level = self._enum_matching(
                legality_level, EnvelopeLegalityLevel.list(), "legality_level"
            )
        self._kwargs = kwargs
