#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from alipayplusmcp.sdk.model.AlipayPlusPathConstant import AlipayPlusPathConstants
from alipayplusmcp.sdk.model.amount import Amount
from alipayplusmcp.sdk.request.alipay_request import AlipayRequest

# https://docs.alipayplus.com/alipayplus/alipayplus/api_acq/refund?role=ACQP&product=Payment1&version=1.4.6
class AlipayRefundRequest(AlipayRequest):

    def __init__(self):
        super(AlipayRefundRequest, self).__init__(AlipayPlusPathConstants.REFUND_PATH)
        self.__payment_request_id = None
        self.__payment_id = None
        self.__refund_request_id = None
        self.__refund_amount = None  # type: Amount
        self.__refund_reason = None

    @property
    def payment_request_id(self):
        return self.__payment_request_id

    @payment_request_id.setter
    def payment_request_id(self, value):
        self.__payment_request_id = value

    @property
    def payment_id(self):
        return self.__payment_id

    @payment_id.setter
    def payment_id(self, value):
        self.__payment_id = value

    @property
    def refund_request_id(self):
        return self.__refund_request_id

    @refund_request_id.setter
    def refund_request_id(self, value):
        self.__refund_request_id = value

    @property
    def refund_amount(self):
        return self.__refund_amount

    @refund_amount.setter
    def refund_amount(self, value):
        self.__refund_amount = value

    @property
    def refund_reason(self):
        return self.__refund_reason

    @refund_reason.setter
    def refund_reason(self, value):
        self.__refund_reason = value


    def to_aps_json(self):
        json_str = json.dumps(obj=self.__to_aps_dict(), default=lambda o: o.to_aps_dict(), indent=3)
        return json_str

    def __to_aps_dict(self):
        params = dict()

        if hasattr(self, "payment_request_id") and self.payment_request_id:
            params['paymentRequestId'] = self.payment_request_id

        if hasattr(self, "payment_id") and self.payment_id:
            params['paymentId'] = self.payment_id

        if hasattr(self, "refund_request_id") and self.refund_request_id:
            params['refundRequestId'] = self.refund_request_id

        if hasattr(self, "refund_amount") and self.refund_amount:
            params['refundAmount'] = self.refund_amount

        if hasattr(self, "refund_reason") and self.refund_reason:
            params['refundReason'] = self.refund_reason

        return params
