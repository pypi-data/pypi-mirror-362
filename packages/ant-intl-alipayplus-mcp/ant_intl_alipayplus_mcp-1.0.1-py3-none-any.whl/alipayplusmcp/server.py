import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator, List

from mcp.server import FastMCP

from alipayplusmcp.sdk.default_alipay_client import DefaultAlipayClient
from alipayplusmcp.sdk.exception.exception import AlipayApiException
from alipayplusmcp.sdk.model.address import Address
from alipayplusmcp.sdk.model.amount import Amount
from alipayplusmcp.sdk.model.attachment import Attachment
from alipayplusmcp.sdk.model.buyer import Buyer
from alipayplusmcp.sdk.model.customs_info import CustomsInfo
from alipayplusmcp.sdk.model.env import Env
from alipayplusmcp.sdk.model.merchant import Merchant
from alipayplusmcp.sdk.model.merchant_customs_info import MerchantCustomsInfo
from alipayplusmcp.sdk.model.order import Order
from alipayplusmcp.sdk.model.payment_factor import PaymentFactor
from alipayplusmcp.sdk.model.payment_method import PaymentMethod
from alipayplusmcp.sdk.model.settlement_strategy import SettlementStrategy
from alipayplusmcp.sdk.request.customs.alipay_customs_declare_request import AlipayCustomsDeclareRequest
from alipayplusmcp.sdk.request.customs.alipay_customs_inquire_request import AlipayCustomsInquireRequest
from alipayplusmcp.sdk.request.dispute.alipay_response_escalation_request import AlipayResponseEscalationRequest
from alipayplusmcp.sdk.request.dispute.alipay_response_retrieval_request import AlipayResponseRetrievalRequest
from alipayplusmcp.sdk.request.pay.alipay_cancel_payment_request import AlipayCancelPaymentRequest
from alipayplusmcp.sdk.request.pay.alipay_inquiry_payment_request import AlipayInquiryPaymentRequest
from alipayplusmcp.sdk.request.pay.alipay_pay_request import AlipayPayRequest
from alipayplusmcp.sdk.request.pay.alipay_refund_request import AlipayRefundRequest


class Account:
    def __init__(self):
        self.gateway_url = ''
        self.client_id = ''
        self.merchant_private_key = ''
        self.alipay_public_key = ''
        self.payment_redirect_url = ''
        self.payment_notify_url = ''
        self.settlement_currency = ''
        self.merchant_name = ''
        self.merchant_id = ''
        self.merchant_mcc = ''
        self.merchant_region = ''


def serve(account: Account) -> None:


    alipay_client = DefaultAlipayClient(gateway_url=account.gateway_url,
                                        client_id=account.client_id,
                                        merchant_private_key=account.merchant_private_key,
                                        alipay_public_key=account.alipay_public_key)


    @asynccontextmanager
    async def alipay_lifespan(server: FastMCP) -> AsyncIterator[dict]:
        """Lifespan context manager for the mcp server."""
        yield {"client": alipay_client}


    server = FastMCP("alipayplus-mcp", lifespan=alipay_lifespan)


    @server.tool()
    def create_payment(payment_request_id: str,
                       order_amount_currency: str,
                       order_amount_value: int,
                       order_description: str) -> str:
        """ The tool is used by the Acquiring Service Provider (ACQP) to send a request to Alipay+ to place orders.

        Args:
            payment_request_id: TThe unique ID assigned by a merchant to identify a payment request. Maximum length: 64 characters
            order_amount_currency: The transaction currency that is specified in the contract. A 3-letter currency code that follows the ISO 4217 standard.Maximum length: 3 characters
            order_amount_value: The amount to charge as a positive integer in the smallest currency unit. (That is, 100 cents to charge $1.00, or 100 to charge JPY 100, a 0-decimal currency).Value range: 1 - unlimited
            order_description: Summary description of the order, which is used for user consumption records display or other further actions.Maximum length: 256 characters
        """
        try:
            context = server.get_context()
            client = context.request_context.lifespan_context["client"]

            order = Order()
            merchant = Merchant()
            merchant.merchant_display_name = account.merchant_name
            merchant.merchant_name = account.merchant_name
            merchant.merchant_mcc = account.merchant_mcc
            merchant.reference_merchant_id = account.merchant_id

            address = Address()
            address.region = account.merchant_region
            merchant.merchant_address = address

            buyer = Buyer()
            buyer.reference_buyer_id = str(uuid.uuid4())

            order.merchant = merchant
            order.buyer = buyer
            order.reference_order_id = payment_request_id

            env = Env()
            env.terminal_type = "WAP"
            env.os_type = "IOS"

            order.env = env
            order.order_description = order_description
            order.order_amount = Amount(order_amount_currency, order_amount_value)

            alipay_pay_request = AlipayPayRequest()
            alipay_pay_request.payment_request_id = payment_request_id
            alipay_pay_request.payment_amount = Amount(order_amount_currency, order_amount_value)
            alipay_pay_request.order = order

            payment_factor = PaymentFactor()
            payment_factor.is_in_store_payment = False
            payment_factor.is_cashier_payment = True
            payment_factor.presentment_mode = "UNIFIED"
            alipay_pay_request.payment_factor = payment_factor
            alipay_pay_request.payment_redirect_url = account.payment_redirect_url or "/"
            alipay_pay_request.payment_notify_url = account.payment_notify_url
            settlement_strategy = SettlementStrategy()
            settlement_strategy.settlement_currency = account.settlement_currency
            alipay_pay_request.settlement_strategy = settlement_strategy

            method = PaymentMethod()
            method.payment_method_type = "CONNECT_WALLET"
            alipay_pay_request.payment_method = method
            return client.execute(alipay_pay_request)
        except AlipayApiException as aex:
            return str(aex)
        except Exception as e:
            return str(e)

    @server.tool()
    def query_payment(payment_request_id: str) -> str:
        """ The tool is used by the Acquiring Service Provider (ACQP) to query the payment result if no payment result is received after a certain period of time.

        Args:
            payment_request_id: The unique ID that is assigned by a merchant to identify a payment request.Maximum length: 64 characters
        """
        try:
            context = server.get_context()
            client = context.request_context.lifespan_context["client"]

            alipay_inquiry_payment_request = AlipayInquiryPaymentRequest()
            alipay_inquiry_payment_request.payment_request_id = payment_request_id
            return client.execute(alipay_inquiry_payment_request)
        except AlipayApiException as aex:
            return str(aex)
        except Exception as e:
            return str(e)

    @server.tool()
    def cancel_payment(payment_request_id: str) -> str:
        """ The tool is used by the Acquiring Service Provider (ACQP) to proactively cancel a payment when no payment result is received after the payment expires, or when the ACQP closes the payment before receiving the payment result.

        Args:
            payment_request_id: The request ID of the payment to be canceled, assigned by the ACQP to identify the original payment order.Maximum length: 64 characters
        """
        try:
            context = server.get_context()
            client = context.request_context.lifespan_context["client"]

            alipay_cancel_payment_request = AlipayCancelPaymentRequest()
            alipay_cancel_payment_request.payment_request_id = payment_request_id
            return client.execute(alipay_cancel_payment_request)
        except AlipayApiException as aex:
            return str(aex)
        except Exception as e:
            return str(e)

    @server.tool()
    def create_refund(payment_request_id: str,
                      refund_request_id: str,
                      refund_amount_value: int,
                      refund_currency: str) -> str:
        """ The tool is used by the Acquiring Service Provider (ACQP) to initiate a refund of a successful payment.The refund can be full or partial. A transaction can have multiple refunds as long as the total refund amount is less than or equal to the original transaction amount.

        Args:
            payment_request_id: The request ID of the payment to be refunded, assigned by the ACQP to identify the original payment order.Maximum length: 64 characters
            refund_request_id: The unique ID that is assigned by the ACQP to identify a refund request. Maximum length: 64 characters.
            refund_amount_value: The amount to charge as a positive integer in the smallest currency unit. (That is, 100 cents to charge $1.00, or 100 to charge JPY 100, a 0-decimal currency).Value range: 1 - unlimited
            refund_currency: The currency code of the amount. The value of this parameter must be an alphabetic code that follows the ISO 4217 standard, for example, "EUR" for Euros.
        """
        try:
            context = server.get_context()
            client = context.request_context.lifespan_context["client"]

            alipay_refund_request = AlipayRefundRequest()
            alipay_refund_request.payment_request_id = payment_request_id
            alipay_refund_request.refund_amount = Amount(refund_currency, refund_amount_value)
            alipay_refund_request.refund_request_id = refund_request_id
            return client.execute(alipay_refund_request)
        except AlipayApiException as aex:
            return str(aex)
        except Exception as e:
            return str(e)

    @server.tool()
    def customs_declare(payment_request_id: str,
                         customs_declaration_request_id: str,
                         declaration_amount_value: int,
                         customs_code: str,
                         merchant_customs_code: str,
                         merchant_customs_name: str,
                         is_split: bool,
                         reference_order_id: str
                         ) -> str:
        """ The tool is used by the Acquiring Service Provider (ACQP) to declare a payment to customs or update an existing declaration.

        Args:
            payment_request_id: The unique ID that is assigned by the ACQP to identify a payment request for the order.Maximum length: 64 characters
            customs_declaration_request_id: The unique ID that is assigned by the merchant to identify a customs declaration request. This parameter is not provided for the customs. Maximum length: 64 characters
            declaration_amount_value: The customs declaration amount as a natural number.Value range: 1 - unlimited
            customs_code: The customs code (in either uppercase or lowercase). Maximum length: 128 characters
            merchant_customs_code: The merchant code that is registered in the customs system. Maximum length: 128 characters
            merchant_customs_name: The merchant name that is registered in the customs system. Maximum length: 256 characters
            is_split: This parameter indicates whether the payment order needs to be split for declaration. Valid values are:
                true: indicates that order splitting is needed.
                false: indicates that order splitting is not needed.
            reference_order_id: The unique ID that is assigned by the merchant to identify an order that needs to be declared to the customs. Maximum length: 64 characters
        """
        try:
            context = server.get_context()
            client = context.request_context.lifespan_context["client"]

            alipay_customs_declare_request = AlipayCustomsDeclareRequest()
            alipay_customs_declare_request.payment_request_id = payment_request_id
            alipay_customs_declare_request.customs_declaration_request_id = customs_declaration_request_id
            alipay_customs_declare_request.declaration_amount = Amount("CNY", declaration_amount_value)

            customs = CustomsInfo()
            customs.customs_code = customs_code
            customs.region = "CN"
            alipay_customs_declare_request.customs = customs

            merchant_customs_info = MerchantCustomsInfo()
            merchant_customs_info.merchant_customs_code = merchant_customs_code
            merchant_customs_info.merchant_customs_name = merchant_customs_name
            alipay_customs_declare_request.merchant_customs_info = merchant_customs_info

            alipay_customs_declare_request.is_split = is_split
            alipay_customs_declare_request.reference_order_id = reference_order_id

            return client.execute(alipay_customs_declare_request)
        except AlipayApiException as aex:
            return str(aex)
        except Exception as e:
            return str(e)

    @server.tool()
    def query_customs_declare(declaration_request_ids: List[str]) -> str:
        """ The tool is used by the Acquiring Service Provider (ACQP) to inquire about the status of declared payments.

        Args:
            declaration_request_ids: The unique declaration request IDs that are assigned by the merchant to identify declaration requests. Up to 10 declaration request IDs are supported at a time. Maximum length: 64 characters. Maximum size: 10 elements
        """
        try:
            context = server.get_context()
            client = context.request_context.lifespan_context["client"]

            alipay_customs_inquire_request = AlipayCustomsInquireRequest()
            alipay_customs_inquire_request.declaration_request_ids = declaration_request_ids
            return client.execute(alipay_customs_inquire_request)
        except AlipayApiException as aex:
            return str(aex)
        except Exception as e:
            return str(e)

    server.run('stdio')
