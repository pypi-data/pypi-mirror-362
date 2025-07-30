import json


class CustomsInfo(object):

    def __init__(self):
        self.__customs_code = None
        self.__region = None

    @property
    def customs_code(self):
        return self.__customs_code

    @customs_code.setter
    def customs_code(self, value):
        self.__customs_code = value

    @property
    def region(self):
        return self.__region

    @region.setter
    def region(self, value):
        self.__region = value

    def to_aps_dict(self):
        params = dict()
        if hasattr(self, "customs_code") and self.customs_code:
            params['customsCode'] = self.customs_code

        if hasattr(self, "region") and self.region:
            params['region'] = self.region

        return params

    def parse_rsp_body(self, body_data):
        if type(body_data) == str:
            body_data = json.loads(body_data)

        if 'customsCode' in body_data:
            self.customs_code = body_data['customsCode']

        if 'region' in body_data:
            self.region = body_data['region']

