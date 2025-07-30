from alipayplusmcp.sdk.model.shipping import Shipping


class ProofOfDelivery(object):

    def __init__(self):
        self.__delivery_tracking_no = None
        self.__shipping = None # type: Shipping

    @property
    def delivery_tracking_no(self):
        return self.__delivery_tracking_no

    @delivery_tracking_no.setter
    def delivery_tracking_no(self, value):
        self.__delivery_tracking_no = value

    @property
    def shipping(self):
        return self.__shipping

    @shipping.setter
    def shipping(self, value):
        self.__shipping = value

    def to_aps_dict(self):
        params = dict()
        if hasattr(self, "delivery_tracking_no") and self.delivery_tracking_no:
            params['deliveryTrackingNo'] = self.delivery_tracking_no

        if hasattr(self, "shipping") and self.shipping:
            params['shipping'] = self.shipping

        return params
