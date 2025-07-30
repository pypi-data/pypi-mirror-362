#!/usr/bin/env python
# -*- coding: utf-8 -*-
from alipayplusmcp.sdk.model.amount import Amount
from alipayplusmcp.sdk.model.quote import Quote
from alipayplusmcp.sdk.model.transaction import Transaction
from alipayplusmcp.sdk.response.alipay_response import AlipayResponse
from alipayplusmcp.sdk.response.result import Result


class AlipayInquiryPaymentResponse(AlipayResponse):

    def __init__(self, rsp_body):
        super(AlipayInquiryPaymentResponse, self).__init__()
        self.__payment_result = None  # type: Result
        self.__acquirer_id = None
        self.__psp_id = None
        self.__payment_request_id = None
        self.__payment_id = None
        self.__payment_amount = None  # type: Amount
        self.__payment_time = None
        self.__customer_id = None
        self.__wallet_brand_name = None
        self.__transactions = None  # type: list[Transaction]
        self.__settlement_amount = None #type: Amount
        self.__settlement_quote = None  # type: Quote
        self.__customs_declaration_amount = None  # type: Amount
        self.__mpp_payment_id = None
        self.__parse_rsp_body(rsp_body)

    @property
    def payment_result(self):
        return self.__payment_result

    @property
    def acquirer_id(self):
        return self.__acquirer_id

    @property
    def psp_id(self):
        return self.__psp_id

    @property
    def payment_request_id(self):
        return self.__payment_request_id

    @property
    def payment_id(self):
        return self.__payment_id

    @property
    def payment_amount(self):
        return self.__payment_amount

    @property
    def payment_time(self):
        return self.__payment_time

    @property
    def customer_id(self):
        return self.__customer_id

    @property
    def wallet_brand_name(self):
        return self.__wallet_brand_name

    @property
    def transactions(self):
        return self.__transactions

    @property
    def settlement_amount(self):
        return self.__settlement_amount

    @property
    def settlement_quote(self):
        return self.__settlement_quote

    @property
    def customs_declaration_amount(self):
        return self.__customs_declaration_amount

    @property
    def mpp_payment_id(self):
        return self.__mpp_payment_id

    def __parse_rsp_body(self, rsp_body):
        response = super(AlipayInquiryPaymentResponse, self).parse_rsp_body(rsp_body)

        if 'paymentResult' in response:
            result = Result()
            result.parse_rsp_body(response['paymentResult'])
            self.__payment_result = result

        if 'acquirerId' in response:
            self.__acquirer_id = response['acquirerId']

        if 'pspId' in response:
            self.__psp_id = response['pspId']

        if 'paymentRequestId' in response:
            self.__payment_request_id = response['paymentRequestId']

        if 'paymentId' in response:
            self.__payment_id = response['paymentId']

        if 'paymentAmount' in response:
            payment_amount = Amount()
            payment_amount.parse_rsp_body(response['paymentAmount'])
            self.__payment_amount = payment_amount

        if 'paymentTime' in response:
            self.__payment_time = response['paymentTime']

        if 'customerId' in response:
            self.__customer_id = response['customerId']

        if 'walletBrandName' in response:
            self.__wallet_brand_name = response['walletBrandName']

        if 'transactions' in response:
            transactions = []
            for transaction_body in response['transactions']:
                transaction = Transaction()
                transaction.parse_rsp_body(transaction_body)
                transactions.append(transaction)
            self.__transactions = transactions

        if 'settlementAmount' in response:
            settlement_amount = Amount()
            settlement_amount.parse_rsp_body(response['settlementAmount'])
            self.__settlement_amount = settlement_amount

        if 'settlementQuote' in response:
            settlement_quote = Quote()
            settlement_quote.parse_rsp_body(response['settlementQuote'])
            self.__settlement_quote = settlement_quote

        if 'customsDeclarationAmount' in response:
            customs_declaration_amount = Amount()
            customs_declaration_amount.parse_rsp_body(response['customsDeclarationAmount'])
            self.__customs_declaration_amount = customs_declaration_amount

        if 'mppPaymentId' in response:
            self.__mpp_payment_id = response['mppPaymentId']
