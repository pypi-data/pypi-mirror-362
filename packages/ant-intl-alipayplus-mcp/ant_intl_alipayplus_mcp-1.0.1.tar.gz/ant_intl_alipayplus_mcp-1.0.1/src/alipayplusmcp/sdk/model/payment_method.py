#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


class PaymentMethod(object):
    def __init__(self):
        self.__payment_method_id = None
        self.__payment_method_type = None
        self.__payment_method_meta_data = None #type: map

    @property
    def payment_method_type(self):
        return self.__payment_method_type

    @payment_method_type.setter
    def payment_method_type(self, value):
        self.__payment_method_type = value

    @property
    def payment_method_id(self):
        return self.__payment_method_id

    @payment_method_id.setter
    def payment_method_id(self, value):
        self.__payment_method_id = value

    @property
    def payment_method_meta_data(self):
        return self.__payment_method_meta_data

    @payment_method_meta_data.setter
    def payment_method_meta_data(self, value):
        self.__payment_method_meta_data = value

    def to_aps_dict(self):
        params = dict()
        if hasattr(self, "payment_method_type") and self.payment_method_type:
            params['paymentMethodType'] = self.payment_method_type

        if hasattr(self, "payment_method_meta_data") and self.payment_method_meta_data:
            params['paymentMethodMetaData'] = self.payment_method_meta_data

        if hasattr(self, "customer_id") and self.customer_id:
            params['customerId'] = self.customer_id

        return params

    def parse_rsp_body(self, response_body):
        if type(response_body) == str:
            response_body = json.loads(response_body)

        if 'paymentMethodType' in response_body:
            self.payment_method_type = response_body['paymentMethodType']
        if hasattr(self, "payment_method_meta_data") and self.payment_method_meta_data:
            self.payment_method_meta_data = response_body['paymentMethodMetaData']
        if 'paymentMethodId' in response_body:
            self.payment_method_id = response_body['paymentMethodId']