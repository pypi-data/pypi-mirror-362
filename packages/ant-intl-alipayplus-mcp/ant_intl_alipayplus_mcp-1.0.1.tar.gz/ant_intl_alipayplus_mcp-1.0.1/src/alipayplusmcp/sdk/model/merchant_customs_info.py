import json


class MerchantCustomsInfo(object):

    def __init__(self):
        self.__merchant_customs_code = None
        self.__merchant_customs_name = None

    @property
    def merchant_customs_code(self):
        return self.__merchant_customs_code

    @merchant_customs_code.setter
    def merchant_customs_code(self, value):
        self.__merchant_customs_code = value

    @property
    def merchant_customs_name(self):
        return self.__merchant_customs_name

    @merchant_customs_name.setter
    def merchant_customs_name(self, value):
        self.__merchant_customs_name = value

    def to_aps_dict(self):
        params = dict()
        if hasattr(self, "merchant_customs_code") and self.merchant_customs_code:
            params['merchantCustomsCode'] = self.merchant_customs_code

        if hasattr(self, "merchant_customs_name") and self.merchant_customs_name:
            params['merchantCustomsName'] = self.merchant_customs_name

        return params

    def parse_rsp_body(self, body_data):
        if type(body_data) == str:
            body_data = json.loads(body_data)

        if 'merchantCustomsCode' in body_data:
            self.merchant_customs_code = body_data['merchantCustomsCode']

        if 'merchantCustomsName' in body_data:
            self.merchant_customs_name = body_data['merchantCustomsName']
