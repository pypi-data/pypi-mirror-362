import json

from alipayplusmcp.sdk.model.user_name import UserName


class Certificate(object):

    def __init__(self):
        self.__certificate_type = None
        self.__certificate_no = None
        self.__holder_name = None # type: UserName
        self.__effective_date = None
        self.__expire_date = None

    @property
    def certificate_type(self):
        return self.__certificate_type

    @certificate_type.setter
    def certificate_type(self, value):
        self.__certificate_type = value

    @property
    def certificate_no(self):
        return self.__certificate_no

    @certificate_no.setter
    def certificate_no(self, value):
        self.__certificate_no = value

    @property
    def holder_name(self):
        return self.__holder_name

    @holder_name.setter
    def holder_name(self, value):
        self.__holder_name = value

    @property
    def effective_date(self):
        return self.__effective_date

    @effective_date.setter
    def effective_date(self, value):
        self.__effective_date = value

    @property
    def expire_date(self):
        return self.__expire_date

    @expire_date.setter
    def expire_date(self, value):
        self.__expire_date = value

    def to_aps_dict(self):
        params = dict()
        if hasattr(self, "certificate_type") and self.certificate_type:
            params['certificateType'] = self.certificate_type

        if hasattr(self, "certificate_no") and self.certificate_no:
            params['certificateNo'] = self.certificate_no

        if hasattr(self, "holder_name") and self.holder_name:
            params['holderName'] = self.holder_name

        if hasattr(self, "effective_date") and self.effective_date:
            params['effectiveDate'] = self.effective_date

        if hasattr(self, "expire_date") and self.expire_date:
            params['expireDate'] = self.expire_date

        return params

    def parse_rsp_body(self, body_data):
        if type(body_data) == str:
            body_data = json.loads(body_data)

        if 'certificateType' in body_data:
            self.certificate_type = body_data['certificateType']

        if 'certificateNo' in body_data:
            self.certificate_no = body_data['certificateNo']

        if 'holderName' in body_data and body_data['holderName'] is not None:
            user_name = UserName()
            user_name.parse_rsp_body(body_data['holderName'])
            self.holder_name = user_name

        if 'effectiveDate' in body_data:
            self.effective_date = body_data['effectiveDate']

        if 'expireDate' in body_data:
            self.expire_date = body_data['expireDate']
