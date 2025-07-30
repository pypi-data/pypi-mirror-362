import json

from alipayplusmcp.sdk.model.AlipayPlusPathConstant import AlipayPlusPathConstants
from alipayplusmcp.sdk.request.alipay_request import AlipayRequest

# https://docs.alipayplus.com/alipayplus/alipayplus/api_acq/inquiry_payment?role=ACQP&product=Payment1&version=1.4.6
class AlipayInquiryPaymentRequest(AlipayRequest):

    def __init__(self):
        super(AlipayInquiryPaymentRequest, self).__init__(AlipayPlusPathConstants.INQUIRY_PAYMENT_PATH)
        self.__payment_request_id = None
        self.__payment_id = None

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


    def to_aps_json(self):
        params = dict()
        if hasattr(self, "payment_request_id") and self.payment_request_id:
            params['paymentRequestId'] = self.payment_request_id

        if hasattr(self, "payment_id") and self.payment_id:
            params['paymentId'] = self.payment_id

        json_str = json.dumps(obj=params, indent=3)
        return json_str