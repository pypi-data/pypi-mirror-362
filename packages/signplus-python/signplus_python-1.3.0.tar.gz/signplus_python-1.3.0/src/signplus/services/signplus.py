from typing import List
from .utils.validator import Validator
from .utils.base_service import BaseService
from ..net.transport.serializer import Serializer
from ..net.environment.environment import Environment
from ..models.utils.sentinel import SENTINEL
from ..models.utils.cast_models import cast_models
from ..models import (
    AddAnnotationRequest,
    AddEnvelopeDocumentRequest,
    AddEnvelopeSigningStepsRequest,
    AddTemplateDocumentRequest,
    AddTemplateSigningStepsRequest,
    Annotation,
    CreateEnvelopeFromTemplateRequest,
    CreateEnvelopeRequest,
    CreateTemplateRequest,
    CreateWebhookRequest,
    Document,
    Envelope,
    EnvelopeNotification,
    ListEnvelopeDocumentAnnotationsResponse,
    ListEnvelopeDocumentsResponse,
    ListEnvelopesRequest,
    ListEnvelopesResponse,
    ListTemplateAnnotationsResponse,
    ListTemplateDocumentAnnotationsResponse,
    ListTemplateDocumentsResponse,
    ListTemplatesRequest,
    ListTemplatesResponse,
    ListWebhooksRequest,
    ListWebhooksResponse,
    RenameEnvelopeRequest,
    RenameTemplateRequest,
    SetEnvelopeCommentRequest,
    SetEnvelopeDynamicFieldsRequest,
    SetEnvelopeExpirationRequest,
    SetEnvelopeLegalityLevelRequest,
    SetTemplateCommentRequest,
    Template,
    Webhook,
)


class SignplusService(BaseService):

    @cast_models
    def create_envelope(self, request_body: CreateEnvelopeRequest) -> Envelope:
        """Create new envelope

        :param request_body: The request body.
        :type request_body: CreateEnvelopeRequest
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Envelope
        """

        Validator(CreateEnvelopeRequest).validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope",
                [self.get_access_token()],
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def create_envelope_from_template(
        self, request_body: CreateEnvelopeFromTemplateRequest, template_id: str
    ) -> Envelope:
        """Create new envelope from template

        :param request_body: The request body.
        :type request_body: CreateEnvelopeFromTemplateRequest
        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Envelope
        """

        Validator(CreateEnvelopeFromTemplateRequest).validate(request_body)
        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/from_template/{{template_id}}",
                [self.get_access_token()],
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def list_envelopes(
        self, request_body: ListEnvelopesRequest = None
    ) -> ListEnvelopesResponse:
        """List envelopes

        :param request_body: The request body., defaults to None
        :type request_body: ListEnvelopesRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: ListEnvelopesResponse
        """

        Validator(ListEnvelopesRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelopes",
                [self.get_access_token()],
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return ListEnvelopesResponse._unmap(response)

    @cast_models
    def get_envelope(self, envelope_id: str) -> Envelope:
        """Get envelope

        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Envelope
        """

        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def delete_envelope(self, envelope_id: str) -> None:
        """Delete envelope

        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("DELETE")
        )

        self.send_request(serialized_request)

    @cast_models
    def download_envelope_signed_documents(
        self, envelope_id: str, certificate_of_completion: bool = SENTINEL
    ) -> any:
        """Download signed documents for an envelope

        :param envelope_id: ID of the envelope
        :type envelope_id: str
        :param certificate_of_completion: Whether to include the certificate of completion in the downloaded file, defaults to None
        :type certificate_of_completion: bool, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: any
        """

        Validator(str).validate(envelope_id)
        Validator(bool).is_optional().validate(certificate_of_completion)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/signed_documents",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .add_query("certificate_of_completion", certificate_of_completion)
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return response

    @cast_models
    def download_envelope_certificate(self, envelope_id: str) -> any:
        """Download certificate of completion for an envelope

        :param envelope_id: ID of the envelope
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: any
        """

        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/certificate",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return response

    @cast_models
    def get_envelope_document(self, envelope_id: str, document_id: str) -> Document:
        """Get envelope document

        :param envelope_id: envelope_id
        :type envelope_id: str
        :param document_id: document_id
        :type document_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Document
        """

        Validator(str).validate(envelope_id)
        Validator(str).validate(document_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/document/{{document_id}}",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .add_path("document_id", document_id)
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return Document._unmap(response)

    @cast_models
    def get_envelope_documents(self, envelope_id: str) -> ListEnvelopeDocumentsResponse:
        """Get envelope documents

        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: ListEnvelopeDocumentsResponse
        """

        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/documents",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return ListEnvelopeDocumentsResponse._unmap(response)

    @cast_models
    def add_envelope_document(
        self, request_body: AddEnvelopeDocumentRequest, envelope_id: str
    ) -> Document:
        """Add envelope document

        :param request_body: The request body.
        :type request_body: AddEnvelopeDocumentRequest
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Document
        """

        Validator(AddEnvelopeDocumentRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/document",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body, "multipart/form-data")
        )

        response, _, _ = self.send_request(serialized_request)
        return Document._unmap(response)

    @cast_models
    def set_envelope_dynamic_fields(
        self, request_body: SetEnvelopeDynamicFieldsRequest, envelope_id: str
    ) -> Envelope:
        """Set envelope dynamic fields

        :param request_body: The request body.
        :type request_body: SetEnvelopeDynamicFieldsRequest
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Envelope
        """

        Validator(SetEnvelopeDynamicFieldsRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/dynamic_fields",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def add_envelope_signing_steps(
        self, request_body: AddEnvelopeSigningStepsRequest, envelope_id: str
    ) -> Envelope:
        """Add envelope signing steps

        :param request_body: The request body.
        :type request_body: AddEnvelopeSigningStepsRequest
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Envelope
        """

        Validator(AddEnvelopeSigningStepsRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/signing_steps",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def send_envelope(self, envelope_id: str) -> Envelope:
        """Send envelope for signature

        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Envelope
        """

        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/send",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("POST")
        )

        response, _, _ = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def duplicate_envelope(self, envelope_id: str) -> Envelope:
        """Duplicate envelope

        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Envelope
        """

        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/duplicate",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("POST")
        )

        response, _, _ = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def void_envelope(self, envelope_id: str) -> Envelope:
        """Void envelope

        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Envelope
        """

        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/void",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("PUT")
        )

        response, _, _ = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def rename_envelope(
        self, request_body: RenameEnvelopeRequest, envelope_id: str
    ) -> Envelope:
        """Rename envelope

        :param request_body: The request body.
        :type request_body: RenameEnvelopeRequest
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Envelope
        """

        Validator(RenameEnvelopeRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/rename",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def set_envelope_comment(
        self, request_body: SetEnvelopeCommentRequest, envelope_id: str
    ) -> Envelope:
        """Set envelope comment

        :param request_body: The request body.
        :type request_body: SetEnvelopeCommentRequest
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Envelope
        """

        Validator(SetEnvelopeCommentRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/set_comment",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def set_envelope_notification(
        self, request_body: EnvelopeNotification, envelope_id: str
    ) -> Envelope:
        """Set envelope notification

        :param request_body: The request body.
        :type request_body: EnvelopeNotification
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Envelope
        """

        Validator(EnvelopeNotification).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/set_notification",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def set_envelope_expiration_date(
        self, request_body: SetEnvelopeExpirationRequest, envelope_id: str
    ) -> Envelope:
        """Set envelope expiration date

        :param request_body: The request body.
        :type request_body: SetEnvelopeExpirationRequest
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Envelope
        """

        Validator(SetEnvelopeExpirationRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/set_expiration_date",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def set_envelope_legality_level(
        self, request_body: SetEnvelopeLegalityLevelRequest, envelope_id: str
    ) -> Envelope:
        """Set envelope legality level

        :param request_body: The request body.
        :type request_body: SetEnvelopeLegalityLevelRequest
        :param envelope_id: envelope_id
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Envelope
        """

        Validator(SetEnvelopeLegalityLevelRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/set_legality_level",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Envelope._unmap(response)

    @cast_models
    def get_envelope_annotations(self, envelope_id: str) -> List[Annotation]:
        """Get envelope annotations

        :param envelope_id: ID of the envelope
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: List[Annotation]
        """

        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/annotations",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return [Annotation._unmap(item) for item in response]

    @cast_models
    def get_envelope_document_annotations(
        self, envelope_id: str, document_id: str
    ) -> ListEnvelopeDocumentAnnotationsResponse:
        """Get envelope document annotations

        :param envelope_id: ID of the envelope
        :type envelope_id: str
        :param document_id: ID of document
        :type document_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: ListEnvelopeDocumentAnnotationsResponse
        """

        Validator(str).validate(envelope_id)
        Validator(str).validate(document_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/annotations/{{document_id}}",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .add_path("document_id", document_id)
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return ListEnvelopeDocumentAnnotationsResponse._unmap(response)

    @cast_models
    def add_envelope_annotation(
        self, request_body: AddAnnotationRequest, envelope_id: str
    ) -> Annotation:
        """Add envelope annotation

        :param request_body: The request body.
        :type request_body: AddAnnotationRequest
        :param envelope_id: ID of the envelope
        :type envelope_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Annotation
        """

        Validator(AddAnnotationRequest).validate(request_body)
        Validator(str).validate(envelope_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/annotation",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Annotation._unmap(response)

    @cast_models
    def delete_envelope_annotation(self, envelope_id: str, annotation_id: str) -> None:
        """Delete envelope annotation

        :param envelope_id: ID of the envelope
        :type envelope_id: str
        :param annotation_id: ID of the annotation to delete
        :type annotation_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(envelope_id)
        Validator(str).validate(annotation_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/envelope/{{envelope_id}}/annotation/{{annotation_id}}",
                [self.get_access_token()],
            )
            .add_path("envelope_id", envelope_id)
            .add_path("annotation_id", annotation_id)
            .serialize()
            .set_method("DELETE")
        )

        self.send_request(serialized_request)

    @cast_models
    def create_template(self, request_body: CreateTemplateRequest) -> Template:
        """Create new template

        :param request_body: The request body.
        :type request_body: CreateTemplateRequest
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Template
        """

        Validator(CreateTemplateRequest).validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/template",
                [self.get_access_token()],
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Template._unmap(response)

    @cast_models
    def list_templates(
        self, request_body: ListTemplatesRequest = None
    ) -> ListTemplatesResponse:
        """List templates

        :param request_body: The request body., defaults to None
        :type request_body: ListTemplatesRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: ListTemplatesResponse
        """

        Validator(ListTemplatesRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/templates",
                [self.get_access_token()],
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return ListTemplatesResponse._unmap(response)

    @cast_models
    def get_template(self, template_id: str) -> Template:
        """Get template

        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Template
        """

        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/template/{{template_id}}",
                [self.get_access_token()],
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return Template._unmap(response)

    @cast_models
    def delete_template(self, template_id: str) -> None:
        """Delete template

        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/template/{{template_id}}",
                [self.get_access_token()],
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("DELETE")
        )

        self.send_request(serialized_request)

    @cast_models
    def duplicate_template(self, template_id: str) -> Template:
        """Duplicate template

        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Template
        """

        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/template/{{template_id}}/duplicate",
                [self.get_access_token()],
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("POST")
        )

        response, _, _ = self.send_request(serialized_request)
        return Template._unmap(response)

    @cast_models
    def add_template_document(
        self, request_body: AddTemplateDocumentRequest, template_id: str
    ) -> Document:
        """Add template document

        :param request_body: The request body.
        :type request_body: AddTemplateDocumentRequest
        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Document
        """

        Validator(AddTemplateDocumentRequest).validate(request_body)
        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/template/{{template_id}}/document",
                [self.get_access_token()],
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body, "multipart/form-data")
        )

        response, _, _ = self.send_request(serialized_request)
        return Document._unmap(response)

    @cast_models
    def get_template_document(self, template_id: str, document_id: str) -> Document:
        """Get template document

        :param template_id: template_id
        :type template_id: str
        :param document_id: document_id
        :type document_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Document
        """

        Validator(str).validate(template_id)
        Validator(str).validate(document_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/template/{{template_id}}/document/{{document_id}}",
                [self.get_access_token()],
            )
            .add_path("template_id", template_id)
            .add_path("document_id", document_id)
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return Document._unmap(response)

    @cast_models
    def get_template_documents(self, template_id: str) -> ListTemplateDocumentsResponse:
        """Get template documents

        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: ListTemplateDocumentsResponse
        """

        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/template/{{template_id}}/documents",
                [self.get_access_token()],
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return ListTemplateDocumentsResponse._unmap(response)

    @cast_models
    def add_template_signing_steps(
        self, request_body: AddTemplateSigningStepsRequest, template_id: str
    ) -> Template:
        """Add template signing steps

        :param request_body: The request body.
        :type request_body: AddTemplateSigningStepsRequest
        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Template
        """

        Validator(AddTemplateSigningStepsRequest).validate(request_body)
        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/template/{{template_id}}/signing_steps",
                [self.get_access_token()],
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Template._unmap(response)

    @cast_models
    def rename_template(
        self, request_body: RenameTemplateRequest, template_id: str
    ) -> Template:
        """Rename template

        :param request_body: The request body.
        :type request_body: RenameTemplateRequest
        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Template
        """

        Validator(RenameTemplateRequest).validate(request_body)
        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/template/{{template_id}}/rename",
                [self.get_access_token()],
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Template._unmap(response)

    @cast_models
    def set_template_comment(
        self, request_body: SetTemplateCommentRequest, template_id: str
    ) -> Template:
        """Set template comment

        :param request_body: The request body.
        :type request_body: SetTemplateCommentRequest
        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Template
        """

        Validator(SetTemplateCommentRequest).validate(request_body)
        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/template/{{template_id}}/set_comment",
                [self.get_access_token()],
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Template._unmap(response)

    @cast_models
    def set_template_notification(
        self, request_body: EnvelopeNotification, template_id: str
    ) -> Template:
        """Set template notification

        :param request_body: The request body.
        :type request_body: EnvelopeNotification
        :param template_id: template_id
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Template
        """

        Validator(EnvelopeNotification).validate(request_body)
        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/template/{{template_id}}/set_notification",
                [self.get_access_token()],
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("PUT")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Template._unmap(response)

    @cast_models
    def get_template_annotations(
        self, template_id: str
    ) -> ListTemplateAnnotationsResponse:
        """Get template annotations

        :param template_id: ID of the template
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: ListTemplateAnnotationsResponse
        """

        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/template/{{template_id}}/annotations",
                [self.get_access_token()],
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return ListTemplateAnnotationsResponse._unmap(response)

    @cast_models
    def get_document_template_annotations(
        self, template_id: str, document_id: str
    ) -> ListTemplateDocumentAnnotationsResponse:
        """Get document template annotations

        :param template_id: ID of the template
        :type template_id: str
        :param document_id: ID of document
        :type document_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: ListTemplateDocumentAnnotationsResponse
        """

        Validator(str).validate(template_id)
        Validator(str).validate(document_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/template/{{template_id}}/annotations/{{document_id}}",
                [self.get_access_token()],
            )
            .add_path("template_id", template_id)
            .add_path("document_id", document_id)
            .serialize()
            .set_method("GET")
        )

        response, _, _ = self.send_request(serialized_request)
        return ListTemplateDocumentAnnotationsResponse._unmap(response)

    @cast_models
    def add_template_annotation(
        self, request_body: AddAnnotationRequest, template_id: str
    ) -> Annotation:
        """Add template annotation

        :param request_body: The request body.
        :type request_body: AddAnnotationRequest
        :param template_id: ID of the template
        :type template_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Annotation
        """

        Validator(AddAnnotationRequest).validate(request_body)
        Validator(str).validate(template_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/template/{{template_id}}/annotation",
                [self.get_access_token()],
            )
            .add_path("template_id", template_id)
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Annotation._unmap(response)

    @cast_models
    def delete_template_annotation(self, template_id: str, annotation_id: str) -> None:
        """Delete template annotation

        :param template_id: ID of the template
        :type template_id: str
        :param annotation_id: ID of the annotation to delete
        :type annotation_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(template_id)
        Validator(str).validate(annotation_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/template/{{template_id}}/annotation/{{annotation_id}}",
                [self.get_access_token()],
            )
            .add_path("template_id", template_id)
            .add_path("annotation_id", annotation_id)
            .serialize()
            .set_method("DELETE")
        )

        self.send_request(serialized_request)

    @cast_models
    def create_webhook(self, request_body: CreateWebhookRequest) -> Webhook:
        """Create webhook

        :param request_body: The request body.
        :type request_body: CreateWebhookRequest
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: Webhook
        """

        Validator(CreateWebhookRequest).validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/webhook",
                [self.get_access_token()],
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return Webhook._unmap(response)

    @cast_models
    def list_webhooks(
        self, request_body: ListWebhooksRequest = None
    ) -> ListWebhooksResponse:
        """List webhooks

        :param request_body: The request body., defaults to None
        :type request_body: ListWebhooksRequest, optional
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        :return: The parsed response data.
        :rtype: ListWebhooksResponse
        """

        Validator(ListWebhooksRequest).is_optional().validate(request_body)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/webhooks",
                [self.get_access_token()],
            )
            .serialize()
            .set_method("POST")
            .set_body(request_body)
        )

        response, _, _ = self.send_request(serialized_request)
        return ListWebhooksResponse._unmap(response)

    @cast_models
    def delete_webhook(self, webhook_id: str) -> None:
        """Delete webhook

        :param webhook_id: webhook_id
        :type webhook_id: str
        ...
        :raises RequestError: Raised when a request fails, with optional HTTP status code and details.
        ...
        """

        Validator(str).validate(webhook_id)

        serialized_request = (
            Serializer(
                f"{self.base_url or Environment.DEFAULT.url}/webhook/{{webhook_id}}",
                [self.get_access_token()],
            )
            .add_path("webhook_id", webhook_id)
            .serialize()
            .set_method("DELETE")
        )

        self.send_request(serialized_request)
