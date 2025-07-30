#!/usr/bin/env python
# -*- coding: utf-8 -*-

from alipayplusmcp.sdk.model.amount import Amount
from alipayplusmcp.sdk.response.alipay_response import AlipayResponse


class AlipayPayResponse(AlipayResponse):

    def __init__(self, rsp_body):
        super(AlipayPayResponse, self).__init__()
        self.__acquirer_id = None
        self.__payment_id = None
        self.__normal_url = None
        self.__payment_amount = None  # type: Amount
        self.__payment_data = None
        self.__psp_id = None
        self.__guide_url = None
        self.__parse_rsp_body(rsp_body)

    @property
    def acquirer_id(self):
        return self.__acquirer_id

    @property
    def payment_id(self):
        return self.__payment_id

    @property
    def normal_url(self):
        return self.__normal_url

    @property
    def payment_amount(self):
        return self.__payment_amount

    @property
    def payment_data(self):
        return self.__payment_data

    @property
    def psp_id(self):
        return self.__psp_id

    @property
    def guide_url(self):
        return self.__guide_url


    def __parse_rsp_body(self, rsp_body):
        response = super(AlipayPayResponse, self).parse_rsp_body(rsp_body)
        if 'acquirerId' in response:
            self.__acquirer_id = response['acquirerId']
        if 'paymentId' in response:
            self.__payment_id = response['paymentId']
        if 'normalUrl' in response:
            self.__normal_url = response['normalUrl']
        if 'paymentAmount' in response:
            payment_amount = Amount()
            payment_amount.parse_rsp_body(response['paymentAmount'])
            self.__payment_amount = payment_amount
        if 'paymentData' in response:
            self.__payment_data = response['paymentData']
        if 'pspId' in response:
            self.__psp_id = response['pspId']
        if 'guideUrl' in response:
            self.__guide_url = response['guideUrl']
