#!/usr/bin/env python
# -*- coding: utf-8 -*-
from alipayplusmcp.sdk.model.amount import Amount
from alipayplusmcp.sdk.model.quote import Quote
from alipayplusmcp.sdk.response.alipay_response import AlipayResponse


class AlipayRefundResponse(AlipayResponse):

    def __init__(self, rsp_body):
        super(AlipayRefundResponse, self).__init__()
        self.__acquirer_id = None
        self.__psp_id = None
        self.__refund_id = None
        self.__refund_time = None
        self.__refund_amount = None  # type: Amount
        self.__settlement_amount = None  # type: Amount
        self.__settlement_quote = None  # type: Quote
        self.__parse_rsp_body(rsp_body)

    @property
    def acquirer_id(self):
        return self.__acquirer_id

    @property
    def psp_id(self):
        return self.__psp_id

    @property
    def refund_id(self):
        return self.__refund_id

    @property
    def refund_time(self):
        return self.__refund_time

    @property
    def refund_amount(self):
        return self.__refund_amount

    @property
    def settlement_amount(self):
        return self.__settlement_amount

    @property
    def settlement_quote(self):
        return self.__settlement_quote


    def __parse_rsp_body(self, rsp_body):
        response = super(AlipayRefundResponse, self).parse_rsp_body(rsp_body)
        if 'acquirerId' in response:
            self.__acquirer_id = response['acquirerId']
        if 'pspId' in response:
            self.__psp_id = response['pspId']
        if 'refundId' in response:
            self.__refund_id = response['refundId']
        if 'refundTime' in response:
            self.__refund_time = response['refundTime']
        if 'refundAmount' in response:
            refund_amount = Amount()
            refund_amount.parse_rsp_body(response['refundAmount'])
            self.__refund_amount = refund_amount

        if 'settlementAmount' in response:
            settlement_amount = Amount()
            settlement_amount.parse_rsp_body(response['settlementAmount'])
            self.__settlement_amount = settlement_amount

        if 'settlementQuote' in response:
            settlement_quote = Quote()
            settlement_quote.parse_rsp_body(response['settlementQuote'])
            self.__settlement_quote = settlement_quote
