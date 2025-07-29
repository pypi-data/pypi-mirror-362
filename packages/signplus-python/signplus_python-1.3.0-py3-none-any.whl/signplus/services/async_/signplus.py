from typing import Awaitable, List
from .utils.to_async import to_async
from ..signplus import SignplusService
from ...models.utils.sentinel import SENTINEL
from ...models import (
    Envelope,
    CreateEnvelopeRequest,
    CreateEnvelopeFromTemplateRequest,
    ListEnvelopesResponse,
    ListEnvelopesRequest,
    Document,
    ListEnvelopeDocumentsResponse,
    AddEnvelopeDocumentRequest,
    SetEnvelopeDynamicFieldsRequest,
    AddEnvelopeSigningStepsRequest,
    RenameEnvelopeRequest,
    SetEnvelopeCommentRequest,
    EnvelopeNotification,
    SetEnvelopeExpirationRequest,
    SetEnvelopeLegalityLevelRequest,
    Annotation,
    ListEnvelopeDocumentAnnotationsResponse,
    AddAnnotationRequest,
    Template,
    CreateTemplateRequest,
    ListTemplatesResponse,
    ListTemplatesRequest,
    AddTemplateDocumentRequest,
    ListTemplateDocumentsResponse,
    AddTemplateSigningStepsRequest,
    RenameTemplateRequest,
    SetTemplateCommentRequest,
    ListTemplateAnnotationsResponse,
    ListTemplateDocumentAnnotationsResponse,
    Webhook,
    CreateWebhookRequest,
    ListWebhooksResponse,
    ListWebhooksRequest,
)


class SignplusServiceAsync(SignplusService):
    """
    Async Wrapper for SignplusServiceAsync
    """

    def create_envelope(
        self, request_body: CreateEnvelopeRequest
    ) -> Awaitable[Envelope]:
        return to_async(super().create_envelope)(request_body)

    def create_envelope_from_template(
        self, request_body: CreateEnvelopeFromTemplateRequest, template_id: str
    ) -> Awaitable[Envelope]:
        return to_async(super().create_envelope_from_template)(
            request_body, template_id
        )

    def list_envelopes(
        self, request_body: ListEnvelopesRequest = None
    ) -> Awaitable[ListEnvelopesResponse]:
        return to_async(super().list_envelopes)(request_body)

    def get_envelope(self, envelope_id: str) -> Awaitable[Envelope]:
        return to_async(super().get_envelope)(envelope_id)

    def delete_envelope(self, envelope_id: str) -> Awaitable[None]:
        return to_async(super().delete_envelope)(envelope_id)

    def download_envelope_signed_documents(
        self, envelope_id: str, certificate_of_completion: bool = SENTINEL
    ) -> Awaitable[any]:
        return to_async(super().download_envelope_signed_documents)(
            envelope_id, certificate_of_completion
        )

    def download_envelope_certificate(self, envelope_id: str) -> Awaitable[any]:
        return to_async(super().download_envelope_certificate)(envelope_id)

    def get_envelope_document(
        self, envelope_id: str, document_id: str
    ) -> Awaitable[Document]:
        return to_async(super().get_envelope_document)(envelope_id, document_id)

    def get_envelope_documents(
        self, envelope_id: str
    ) -> Awaitable[ListEnvelopeDocumentsResponse]:
        return to_async(super().get_envelope_documents)(envelope_id)

    def add_envelope_document(
        self, request_body: AddEnvelopeDocumentRequest, envelope_id: str
    ) -> Awaitable[Document]:
        return to_async(super().add_envelope_document)(request_body, envelope_id)

    def set_envelope_dynamic_fields(
        self, request_body: SetEnvelopeDynamicFieldsRequest, envelope_id: str
    ) -> Awaitable[Envelope]:
        return to_async(super().set_envelope_dynamic_fields)(request_body, envelope_id)

    def add_envelope_signing_steps(
        self, request_body: AddEnvelopeSigningStepsRequest, envelope_id: str
    ) -> Awaitable[Envelope]:
        return to_async(super().add_envelope_signing_steps)(request_body, envelope_id)

    def send_envelope(self, envelope_id: str) -> Awaitable[Envelope]:
        return to_async(super().send_envelope)(envelope_id)

    def duplicate_envelope(self, envelope_id: str) -> Awaitable[Envelope]:
        return to_async(super().duplicate_envelope)(envelope_id)

    def void_envelope(self, envelope_id: str) -> Awaitable[Envelope]:
        return to_async(super().void_envelope)(envelope_id)

    def rename_envelope(
        self, request_body: RenameEnvelopeRequest, envelope_id: str
    ) -> Awaitable[Envelope]:
        return to_async(super().rename_envelope)(request_body, envelope_id)

    def set_envelope_comment(
        self, request_body: SetEnvelopeCommentRequest, envelope_id: str
    ) -> Awaitable[Envelope]:
        return to_async(super().set_envelope_comment)(request_body, envelope_id)

    def set_envelope_notification(
        self, request_body: EnvelopeNotification, envelope_id: str
    ) -> Awaitable[Envelope]:
        return to_async(super().set_envelope_notification)(request_body, envelope_id)

    def set_envelope_expiration_date(
        self, request_body: SetEnvelopeExpirationRequest, envelope_id: str
    ) -> Awaitable[Envelope]:
        return to_async(super().set_envelope_expiration_date)(request_body, envelope_id)

    def set_envelope_legality_level(
        self, request_body: SetEnvelopeLegalityLevelRequest, envelope_id: str
    ) -> Awaitable[Envelope]:
        return to_async(super().set_envelope_legality_level)(request_body, envelope_id)

    def get_envelope_annotations(self, envelope_id: str) -> Awaitable[List[Annotation]]:
        return to_async(super().get_envelope_annotations)(envelope_id)

    def get_envelope_document_annotations(
        self, envelope_id: str, document_id: str
    ) -> Awaitable[ListEnvelopeDocumentAnnotationsResponse]:
        return to_async(super().get_envelope_document_annotations)(
            envelope_id, document_id
        )

    def add_envelope_annotation(
        self, request_body: AddAnnotationRequest, envelope_id: str
    ) -> Awaitable[Annotation]:
        return to_async(super().add_envelope_annotation)(request_body, envelope_id)

    def delete_envelope_annotation(
        self, envelope_id: str, annotation_id: str
    ) -> Awaitable[None]:
        return to_async(super().delete_envelope_annotation)(envelope_id, annotation_id)

    def create_template(
        self, request_body: CreateTemplateRequest
    ) -> Awaitable[Template]:
        return to_async(super().create_template)(request_body)

    def list_templates(
        self, request_body: ListTemplatesRequest = None
    ) -> Awaitable[ListTemplatesResponse]:
        return to_async(super().list_templates)(request_body)

    def get_template(self, template_id: str) -> Awaitable[Template]:
        return to_async(super().get_template)(template_id)

    def delete_template(self, template_id: str) -> Awaitable[None]:
        return to_async(super().delete_template)(template_id)

    def duplicate_template(self, template_id: str) -> Awaitable[Template]:
        return to_async(super().duplicate_template)(template_id)

    def add_template_document(
        self, request_body: AddTemplateDocumentRequest, template_id: str
    ) -> Awaitable[Document]:
        return to_async(super().add_template_document)(request_body, template_id)

    def get_template_document(
        self, template_id: str, document_id: str
    ) -> Awaitable[Document]:
        return to_async(super().get_template_document)(template_id, document_id)

    def get_template_documents(
        self, template_id: str
    ) -> Awaitable[ListTemplateDocumentsResponse]:
        return to_async(super().get_template_documents)(template_id)

    def add_template_signing_steps(
        self, request_body: AddTemplateSigningStepsRequest, template_id: str
    ) -> Awaitable[Template]:
        return to_async(super().add_template_signing_steps)(request_body, template_id)

    def rename_template(
        self, request_body: RenameTemplateRequest, template_id: str
    ) -> Awaitable[Template]:
        return to_async(super().rename_template)(request_body, template_id)

    def set_template_comment(
        self, request_body: SetTemplateCommentRequest, template_id: str
    ) -> Awaitable[Template]:
        return to_async(super().set_template_comment)(request_body, template_id)

    def set_template_notification(
        self, request_body: EnvelopeNotification, template_id: str
    ) -> Awaitable[Template]:
        return to_async(super().set_template_notification)(request_body, template_id)

    def get_template_annotations(
        self, template_id: str
    ) -> Awaitable[ListTemplateAnnotationsResponse]:
        return to_async(super().get_template_annotations)(template_id)

    def get_document_template_annotations(
        self, template_id: str, document_id: str
    ) -> Awaitable[ListTemplateDocumentAnnotationsResponse]:
        return to_async(super().get_document_template_annotations)(
            template_id, document_id
        )

    def add_template_annotation(
        self, request_body: AddAnnotationRequest, template_id: str
    ) -> Awaitable[Annotation]:
        return to_async(super().add_template_annotation)(request_body, template_id)

    def delete_template_annotation(
        self, template_id: str, annotation_id: str
    ) -> Awaitable[None]:
        return to_async(super().delete_template_annotation)(template_id, annotation_id)

    def create_webhook(self, request_body: CreateWebhookRequest) -> Awaitable[Webhook]:
        return to_async(super().create_webhook)(request_body)

    def list_webhooks(
        self, request_body: ListWebhooksRequest = None
    ) -> Awaitable[ListWebhooksResponse]:
        return to_async(super().list_webhooks)(request_body)

    def delete_webhook(self, webhook_id: str) -> Awaitable[None]:
        return to_async(super().delete_webhook)(webhook_id)
