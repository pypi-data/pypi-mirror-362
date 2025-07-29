from .utils.json_map import JsonMap
from .utils.base_model import BaseModel
from .utils.sentinel import SENTINEL


@JsonMap({"id_": "id"})
class AnnotationSignature(BaseModel):
    """Signature annotation (null if annotation is not a signature)

    :param id_: Unique identifier of the annotation signature, defaults to None
    :type id_: str, optional
    """

    def __init__(self, id_: str = SENTINEL, **kwargs):
        """Signature annotation (null if annotation is not a signature)

        :param id_: Unique identifier of the annotation signature, defaults to None
        :type id_: str, optional
        """
        if id_ is not SENTINEL:
            self.id_ = id_
        self._kwargs = kwargs
