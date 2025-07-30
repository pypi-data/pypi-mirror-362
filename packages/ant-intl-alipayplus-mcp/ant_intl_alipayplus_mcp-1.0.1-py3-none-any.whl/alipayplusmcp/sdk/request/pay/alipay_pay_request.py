import json

from alipayplusmcp.sdk.model.AlipayPlusPathConstant import AlipayPlusPathConstants
from alipayplusmcp.sdk.model.amount import Amount
from alipayplusmcp.sdk.model.order import Order
from alipayplusmcp.sdk.model.payment_factor import PaymentFactor
from alipayplusmcp.sdk.model.payment_method import PaymentMethod
from alipayplusmcp.sdk.model.settlement_strategy import SettlementStrategy
from alipayplusmcp.sdk.request.alipay_request import AlipayRequest

# https://docs.alipayplus.com/alipayplus/alipayplus/api_acq/pay_cashier?role=ACQP&product=Payment1&version=1.4.6
class AlipayPayRequest(AlipayRequest):

    def __init__(self):
        super(AlipayPayRequest, self).__init__(AlipayPlusPathConstants.PAYMENT_PATH)
        self.__order = None  # type: Order
        self.__payment_request_id = None
        self.__payment_amount = None  # type: Amount
        self.__payment_method = None  # type: PaymentMethod
        self.__payment_factor = None  # type: PaymentFactor
        self.__payment_expiry_time = None
        self.__payment_notify_url = None
        self.__payment_redirect_url = None
        self.__settlement_strategy = None  # type: SettlementStrategy
        self.__user_region = None
        self.__split_settlement_id = None

    @property
    def payment_request_id(self):
        return self.__payment_request_id

    @payment_request_id.setter
    def payment_request_id(self, value):
        self.__payment_request_id = value

    @property
    def order(self):
        return self.__order

    @order.setter
    def order(self, value):
        self.__order = value

    @property
    def payment_amount(self):
        return self.__payment_amount

    @payment_amount.setter
    def payment_amount(self, value):
        self.__payment_amount = value

    @property
    def payment_method(self):
        return self.__payment_method

    @payment_method.setter
    def payment_method(self, value):
        self.__payment_method = value

    @property
    def payment_factor(self):
        return self.__payment_factor

    @payment_factor.setter
    def payment_factor(self, value):
        self.__payment_factor = value

    @property
    def payment_expiry_time(self):
        return self.__payment_expiry_time

    @payment_expiry_time.setter
    def payment_expiry_time(self, value):
        self.__payment_expiry_time = value

    @property
    def payment_redirect_url(self):
        return self.__payment_redirect_url

    @payment_redirect_url.setter
    def payment_redirect_url(self, value):
        self.__payment_redirect_url = value

    @property
    def payment_notify_url(self):
        return self.__payment_notify_url

    @payment_notify_url.setter
    def payment_notify_url(self, value):
        self.__payment_notify_url = value

    @property
    def settlement_strategy(self):
        return self.__settlement_strategy

    @settlement_strategy.setter
    def settlement_strategy(self, value):
        self.__settlement_strategy = value

    @property
    def user_region(self):
        return self.__user_region

    @user_region.setter
    def user_region(self, value):
        self.__user_region = value


    @property
    def split_settlement_id(self):
        return self.__split_settlement_id

    @split_settlement_id.setter
    def split_settlement_id(self, value):
        self.__split_settlement_id = value

    def to_aps_json(self):
        json_str = json.dumps(obj=self.__to_aps_dict(), default=lambda o: o.to_aps_dict(), indent=3)
        return json_str

    def __to_aps_dict(self):
        params = dict()

        if hasattr(self, "payment_request_id") and self.payment_request_id:
            params['paymentRequestId'] = self.payment_request_id

        if hasattr(self, "order") and self.order:
            params['order'] = self.order

        if hasattr(self, "payment_amount") and self.payment_amount:
            params['paymentAmount'] = self.payment_amount

        if hasattr(self, "payment_method") and self.payment_method:
            params['paymentMethod'] = self.payment_method

        if hasattr(self, "payment_expiry_time") and self.payment_expiry_time:
            params['paymentExpiryTime'] = self.payment_expiry_time

        if hasattr(self, "payment_redirect_url") and self.payment_redirect_url:
            params['paymentRedirectUrl'] = self.payment_redirect_url

        if hasattr(self, "payment_notify_url") and self.payment_notify_url:
            params['paymentNotifyUrl'] = self.payment_notify_url

        if hasattr(self, "payment_factor") and self.payment_factor:
            params['paymentFactor'] = self.payment_factor

        if hasattr(self, "settlement_strategy") and self.settlement_strategy:
            params['settlementStrategy'] = self.settlement_strategy

        if hasattr(self, "user_region") and self.user_region:
            params['userRegion'] = self.user_region

        return params

