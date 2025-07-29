from __future__ import annotations
from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL
from .annotation_type import AnnotationType
from .annotation_signature import AnnotationSignature
from .annotation_initials import AnnotationInitials
from .annotation_text import AnnotationText
from .annotation_date_time import AnnotationDateTime
from .annotation_checkbox import AnnotationCheckbox


@JsonMap({"type_": "type", "datetime_": "datetime"})
class AddAnnotationRequest(BaseModel):
    """AddAnnotationRequest

    :param recipient_id: ID of the recipient, defaults to None
    :type recipient_id: str, optional
    :param document_id: ID of the document
    :type document_id: str
    :param page: Page number where the annotation is placed
    :type page: int
    :param x: X coordinate of the annotation (in % of the page width from 0 to 100) from the top left corner
    :type x: float
    :param y: Y coordinate of the annotation (in % of the page height from 0 to 100) from the top left corner
    :type y: float
    :param width: Width of the annotation (in % of the page width from 0 to 100)
    :type width: float
    :param height: Height of the annotation (in % of the page height from 0 to 100)
    :type height: float
    :param required: required, defaults to None
    :type required: bool, optional
    :param type_: Type of the annotation
    :type type_: AnnotationType
    :param signature: Signature annotation (null if annotation is not a signature), defaults to None
    :type signature: AnnotationSignature, optional
    :param initials: Initials annotation (null if annotation is not initials), defaults to None
    :type initials: AnnotationInitials, optional
    :param text: Text annotation (null if annotation is not a text), defaults to None
    :type text: AnnotationText, optional
    :param datetime_: Date annotation (null if annotation is not a date), defaults to None
    :type datetime_: AnnotationDateTime, optional
    :param checkbox: Checkbox annotation (null if annotation is not a checkbox), defaults to None
    :type checkbox: AnnotationCheckbox, optional
    """

    def __init__(
        self,
        document_id: str,
        page: int,
        x: float,
        y: float,
        width: float,
        height: float,
        type_: AnnotationType,
        recipient_id: str = SENTINEL,
        required: bool = SENTINEL,
        signature: AnnotationSignature = SENTINEL,
        initials: AnnotationInitials = SENTINEL,
        text: AnnotationText = SENTINEL,
        datetime_: AnnotationDateTime = SENTINEL,
        checkbox: AnnotationCheckbox = SENTINEL,
        **kwargs,
    ):
        """AddAnnotationRequest

        :param recipient_id: ID of the recipient, defaults to None
        :type recipient_id: str, optional
        :param document_id: ID of the document
        :type document_id: str
        :param page: Page number where the annotation is placed
        :type page: int
        :param x: X coordinate of the annotation (in % of the page width from 0 to 100) from the top left corner
        :type x: float
        :param y: Y coordinate of the annotation (in % of the page height from 0 to 100) from the top left corner
        :type y: float
        :param width: Width of the annotation (in % of the page width from 0 to 100)
        :type width: float
        :param height: Height of the annotation (in % of the page height from 0 to 100)
        :type height: float
        :param required: required, defaults to None
        :type required: bool, optional
        :param type_: Type of the annotation
        :type type_: AnnotationType
        :param signature: Signature annotation (null if annotation is not a signature), defaults to None
        :type signature: AnnotationSignature, optional
        :param initials: Initials annotation (null if annotation is not initials), defaults to None
        :type initials: AnnotationInitials, optional
        :param text: Text annotation (null if annotation is not a text), defaults to None
        :type text: AnnotationText, optional
        :param datetime_: Date annotation (null if annotation is not a date), defaults to None
        :type datetime_: AnnotationDateTime, optional
        :param checkbox: Checkbox annotation (null if annotation is not a checkbox), defaults to None
        :type checkbox: AnnotationCheckbox, optional
        """
        if recipient_id is not SENTINEL:
            self.recipient_id = recipient_id
        self.document_id = document_id
        self.page = page
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if required is not SENTINEL:
            self.required = required
        self.type_ = self._enum_matching(type_, AnnotationType.list(), "type_")
        if signature is not SENTINEL:
            self.signature = self._define_object(signature, AnnotationSignature)
        if initials is not SENTINEL:
            self.initials = self._define_object(initials, AnnotationInitials)
        if text is not SENTINEL:
            self.text = self._define_object(text, AnnotationText)
        if datetime_ is not SENTINEL:
            self.datetime_ = self._define_object(datetime_, AnnotationDateTime)
        if checkbox is not SENTINEL:
            self.checkbox = self._define_object(checkbox, AnnotationCheckbox)
        self._kwargs = kwargs
