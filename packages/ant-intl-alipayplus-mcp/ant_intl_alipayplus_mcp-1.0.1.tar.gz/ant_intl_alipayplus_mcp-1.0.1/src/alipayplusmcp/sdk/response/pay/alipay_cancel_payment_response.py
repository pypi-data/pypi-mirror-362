#!/usr/bin/env python
# -*- coding: utf-8 -*-

from alipayplusmcp.sdk.response.alipay_response import AlipayResponse


class AlipayCancelPaymentResponse(AlipayResponse):

    def __init__(self, rsp_body):
        super(AlipayCancelPaymentResponse, self).__init__()
        self.__acquirer_id = None
        self.__psp_id = None
        self.__parse_rsp_body(rsp_body)

    @property
    def acquirer_id(self):
        return self.__acquirer_id

    @property
    def psp_id(self):
        return self.__psp_id


    def __parse_rsp_body(self, rsp_body):
        response = super(AlipayCancelPaymentResponse, self).parse_rsp_body(rsp_body)
        if 'acquirerId' in response:
            self.__acquirer_id = response['acquirerId']
        if 'pspId' in response:
            self.__psp_id = response['pspId']
