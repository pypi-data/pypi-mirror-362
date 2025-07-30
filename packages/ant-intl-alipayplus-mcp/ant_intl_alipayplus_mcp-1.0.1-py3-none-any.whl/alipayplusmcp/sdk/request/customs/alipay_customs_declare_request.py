import json

from alipayplusmcp.sdk.model.AlipayPlusPathConstant import AlipayPlusPathConstants
from alipayplusmcp.sdk.model.amount import Amount
from alipayplusmcp.sdk.model.certificate import Certificate
from alipayplusmcp.sdk.model.customs_info import CustomsInfo
from alipayplusmcp.sdk.model.merchant_customs_info import MerchantCustomsInfo
from alipayplusmcp.sdk.request.alipay_request import AlipayRequest

# https://docs.alipayplus.com/alipayplus/alipayplus/api_acq/declare?role=ACQP&product=Payment1&version=1.4.6
class AlipayCustomsDeclareRequest(AlipayRequest):

    def __init__(self):
        super(AlipayCustomsDeclareRequest, self).__init__(AlipayPlusPathConstants.CUSTOMS_DECLARE_PATH)
        self.__payment_request_id = None
        self.__customs_declaration_request_id = None
        self.__customs = None # type: CustomsInfo
        self.__merchant_customs_info = None # type: MerchantCustomsInfo
        self.__declaration_amount = None # type: Amount
        self.__is_split = None
        self.__reference_order_id = None
        self.__buyer_certificate = None # type: Certificate

    @property
    def payment_request_id(self):
        return self.__payment_request_id

    @payment_request_id.setter
    def payment_request_id(self, value):
        self.__payment_request_id = value

    @property
    def customs_declaration_request_id(self):
        return self.__customs_declaration_request_id

    @customs_declaration_request_id.setter
    def customs_declaration_request_id(self, value):
        self.__customs_declaration_request_id = value

    @property
    def customs(self):
        return self.__customs

    @customs.setter
    def customs(self, value):
        self.__customs = value

    @property
    def merchant_customs_info(self):
        return self.__merchant_customs_info

    @merchant_customs_info.setter
    def merchant_customs_info(self, value):
        self.__merchant_customs_info = value

    @property
    def declaration_amount(self):
        return self.__declaration_amount

    @declaration_amount.setter
    def declaration_amount(self, value):
        self.__declaration_amount = value

    @property
    def is_split(self):
        return self.__is_split

    @is_split.setter
    def is_split(self, value):
        self.__is_split = value

    @property
    def reference_order_id(self):
        return self.__reference_order_id

    @reference_order_id.setter
    def reference_order_id(self, value):
        self.__reference_order_id = value

    @property
    def buyer_certificate(self):
        return self.__buyer_certificate

    @buyer_certificate.setter
    def buyer_certificate(self, value):
        self.__buyer_certificate = value

    def to_aps_json(self):
        json_str = json.dumps(obj=self.__to_aps_dict(), default=lambda o: o.to_aps_dict(), indent=3)
        return json_str

    def __to_aps_dict(self):
        params = dict()

        if hasattr(self, "payment_request_id") and self.payment_request_id:
            params['paymentRequestId'] = self.payment_request_id

        if hasattr(self, "customs_declaration_request_id") and self.customs_declaration_request_id:
            params['customsDeclarationRequestId'] = self.customs_declaration_request_id

        if hasattr(self, "customs") and self.customs:
            params['customs'] = self.customs

        if hasattr(self, "merchant_customs_info") and self.merchant_customs_info:
            params['merchantCustomsInfo'] = self.merchant_customs_info

        if hasattr(self, "declaration_amount") and self.declaration_amount:
            params['declarationAmount'] = self.declaration_amount

        if hasattr(self, "is_split") and self.is_split is not None: # Check for None explicitly for boolean
            params['isSplit'] = self.is_split

        if hasattr(self, "reference_order_id") and self.reference_order_id:
            params['referenceOrderId'] = self.reference_order_id

        if hasattr(self, "buyer_certificate") and self.buyer_certificate:
            params['buyerCertificate'] = self.buyer_certificate

        return params
