from enum import Enum


class AlipayPlusPathConstants(Enum):

    PAYMENT_PATH = "/aps/api/v1/payments/pay"

    INQUIRY_PAYMENT_PATH = "/aps/api/v1/payments/inquiryPayment"

    CANCEL_PAYMENT_PATH = "/aps/api/v1/payments/cancelPayment"

    REFUND_PATH = "/aps/api/v1/payments/refund"

    RESPONSE_RETRIEVAL_PATH = "/aps/api/v1/disputes/responseRetrieval"

    RESPONSE_ESCALATION_PATH = "/aps/api/v1/disputes/responseEscalation"

    CUSTOMS_DECLARE_PATH = "/aps/api/v1/customs/declare"

    INQUIRE_DECLARE_PATH = "/aps/api/v1/customs/inquireDeclarationRequests"
