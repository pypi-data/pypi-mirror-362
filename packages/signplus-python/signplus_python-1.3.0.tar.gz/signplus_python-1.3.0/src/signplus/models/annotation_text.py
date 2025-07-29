from __future__ import annotations
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .annotation_font import AnnotationFont


@JsonMap({})
class AnnotationText(BaseModel):
    """Text annotation (null if annotation is not a text)

    :param size: Font size of the text in pt, defaults to None
    :type size: float, optional
    :param color: Text color in 32bit representation, defaults to None
    :type color: float, optional
    :param value: Text content of the annotation, defaults to None
    :type value: str, optional
    :param tooltip: Tooltip of the annotation, defaults to None
    :type tooltip: str, optional
    :param dynamic_field_name: Name of the dynamic field, defaults to None
    :type dynamic_field_name: str, optional
    :param font: font, defaults to None
    :type font: AnnotationFont, optional
    """

    def __init__(
        self,
        size: float = SENTINEL,
        color: float = SENTINEL,
        value: str = SENTINEL,
        tooltip: str = SENTINEL,
        dynamic_field_name: str = SENTINEL,
        font: AnnotationFont = SENTINEL,
        **kwargs,
    ):
        """Text annotation (null if annotation is not a text)

        :param size: Font size of the text in pt, defaults to None
        :type size: float, optional
        :param color: Text color in 32bit representation, defaults to None
        :type color: float, optional
        :param value: Text content of the annotation, defaults to None
        :type value: str, optional
        :param tooltip: Tooltip of the annotation, defaults to None
        :type tooltip: str, optional
        :param dynamic_field_name: Name of the dynamic field, defaults to None
        :type dynamic_field_name: str, optional
        :param font: font, defaults to None
        :type font: AnnotationFont, optional
        """
        if size is not SENTINEL:
            self.size = size
        if color is not SENTINEL:
            self.color = color
        if value is not SENTINEL:
            self.value = value
        if tooltip is not SENTINEL:
            self.tooltip = tooltip
        if dynamic_field_name is not SENTINEL:
            self.dynamic_field_name = dynamic_field_name
        if font is not SENTINEL:
            self.font = self._define_object(font, AnnotationFont)
        self._kwargs = kwargs
