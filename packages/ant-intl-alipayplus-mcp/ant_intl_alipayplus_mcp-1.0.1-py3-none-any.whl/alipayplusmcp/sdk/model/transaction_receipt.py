from alipayplusmcp.sdk.model.amount import Amount
from alipayplusmcp.sdk.model.goods import Goods


class TransactionReceipt(object):

    def __init__(self):
        self.__reference_order_id = None
        self.__order_status = None
        self.__order_amount = None  # type: Amount
        self.__goods = None  # type: list[Goods]

    @property
    def reference_order_id(self):
        return self.__reference_order_id

    @reference_order_id.setter
    def reference_order_id(self, value):
        self.__reference_order_id = value

    @property
    def order_status(self):
        return self.__order_status

    @order_status.setter
    def order_status(self, value):
        self.__order_status = value

    @property
    def order_amount(self):
        return self.__order_amount

    @order_amount.setter
    def order_amount(self, value):
        self.__order_amount = value

    @property
    def goods(self):
        return self.__goods

    @goods.setter
    def goods(self, value):
        self.__goods = value

    def to_aps_dict(self):
        params = dict()
        if hasattr(self, "reference_order_id") and self.reference_order_id:
            params['referenceOrderId'] = self.reference_order_id

        if hasattr(self, "order_status") and self.order_status:
            params['orderStatus'] = self.order_status

        if hasattr(self, "order_amount") and self.order_amount:
            params['orderAmount'] = self.order_amount

        if hasattr(self, "goods") and self.goods:
            params['goods'] = self.goods

        return params
