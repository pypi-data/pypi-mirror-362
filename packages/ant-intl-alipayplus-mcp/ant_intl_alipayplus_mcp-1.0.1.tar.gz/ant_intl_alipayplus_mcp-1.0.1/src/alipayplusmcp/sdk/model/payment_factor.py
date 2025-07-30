#!/usr/bin/env python
# -*- coding: utf-8 -*-
from alipayplusmcp.sdk.model.in_store_payment_scenario import InStorePaymentScenario
from alipayplusmcp.sdk.model.presentment_mode import PresentmentMode


class PaymentFactor(object):
    def __init__(self):
        self.__is_in_store_payment = None
        self.__is_cashier_payment = None
        self.__in_store_payment_scenario = None  # type: InStorePaymentScenario
        self.__presentment_mode = None  # type: PresentmentMode
        self.__is_payment_evaluation = None
        self.__is_agreement_payment = None

    @property
    def is_in_store_payment(self):
        return self.__is_in_store_payment

    @is_in_store_payment.setter
    def is_in_store_payment(self, value):
        self.__is_in_store_payment = value

    @property
    def is_cashier_payment(self):
        return self.__is_cashier_payment

    @is_cashier_payment.setter
    def is_cashier_payment(self, value):
        self.__is_cashier_payment = value

    @property
    def in_store_payment_scenario(self):
        return self.__in_store_payment_scenario

    @in_store_payment_scenario.setter
    def in_store_payment_scenario(self, value):
        self.__in_store_payment_scenario = value

    @property
    def presentment_mode(self):
        return self.__presentment_mode

    @presentment_mode.setter
    def presentment_mode(self, value):
        self.__presentment_mode = value

    @property
    def is_payment_evaluation(self):
        return self.__is_payment_evaluation

    @is_payment_evaluation.setter
    def is_payment_evaluation(self, value):
        self.__is_payment_evaluation = value

    @property
    def is_agreement_payment(self):
        return self.__is_agreement_payment

    @is_agreement_payment.setter
    def is_agreement_payment(self, value):
        self.__is_agreement_payment = value

    def to_aps_dict(self):
        params = dict()
        if hasattr(self, "is_in_store_payment") and self.__is_in_store_payment:
            params['isInStorePayment'] = self.is_in_store_payment

        if hasattr(self, "is_cashier_payment") and self.__is_cashier_payment:
            params['isCashierPayment'] = self.is_cashier_payment

        if hasattr(self, "in_store_payment_scenario") and self.__in_store_payment_scenario:
            params['inStorePaymentScenario'] = self.in_store_payment_scenario

        if hasattr(self, "presentment_mode") and self.__presentment_mode:
            params['presentmentMode'] = self.presentment_mode

        if hasattr(self, "is_payment_evaluation") and self.__is_payment_evaluation:
            params['isPaymentEvaluation'] = self.is_payment_evaluation

        if hasattr(self, "is_agreement_payment") and self.__is_agreement_payment:
            params['isAgreementPayment'] = self.is_agreement_payment

        return params
