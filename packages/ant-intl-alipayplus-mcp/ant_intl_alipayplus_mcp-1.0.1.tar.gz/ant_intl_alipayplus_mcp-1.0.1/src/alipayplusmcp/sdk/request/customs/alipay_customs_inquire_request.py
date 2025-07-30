import json

from alipayplusmcp.sdk.model.AlipayPlusPathConstant import AlipayPlusPathConstants
from alipayplusmcp.sdk.request.alipay_request import AlipayRequest

# https://docs.alipayplus.com/alipayplus/alipayplus/api_acq/inquire_declaration_status?role=ACQP&product=Payment1&version=1.4.6

class AlipayCustomsInquireRequest(AlipayRequest):

    def __init__(self):
        super(AlipayCustomsInquireRequest, self).__init__(AlipayPlusPathConstants.INQUIRE_DECLARE_PATH)
        self.__declaration_request_ids = None # type: list[str]

    @property
    def declaration_request_ids(self):
        return self.__declaration_request_ids

    @declaration_request_ids.setter
    def declaration_request_ids(self, value):
        self.__declaration_request_ids = value

    def to_aps_json(self):
        json_str = json.dumps(obj=self.__to_aps_dict(), default=lambda o: o.to_aps_dict(), indent=3)
        return json_str

    def __to_aps_dict(self):
        params = dict()

        if hasattr(self, "declaration_request_ids") and self.declaration_request_ids:
            params['declarationRequestIds'] = self.declaration_request_ids

        return params
