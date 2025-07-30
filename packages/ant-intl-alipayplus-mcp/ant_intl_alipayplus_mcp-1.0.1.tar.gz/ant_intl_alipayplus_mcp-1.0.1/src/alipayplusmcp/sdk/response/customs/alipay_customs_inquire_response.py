from alipayplusmcp.sdk.model.declaration_record import DeclarationRecord
from alipayplusmcp.sdk.response.alipay_response import AlipayResponse


class AlipayCustomsInquireResponse(AlipayResponse):

    def __init__(self, rsp_body):
        super(AlipayCustomsInquireResponse, self).__init__()
        self.__declaration_requests_not_found = None # type: list[str]
        self.__declaration_records = None # type: list[DeclarationRecord]
        self.__parse_rsp_body(rsp_body)

    @property
    def declaration_requests_not_found(self):
        return self.__declaration_requests_not_found

    @property
    def declaration_records(self):
        return self.__declaration_records

    def __parse_rsp_body(self, rsp_body):
        response = super(AlipayCustomsInquireResponse, self).parse_rsp_body(rsp_body)
        if 'declarationRequestsNotFound' in response:
            self.__declaration_requests_not_found = response['declarationRequestsNotFound']

        if 'declarationRecords' in response and response['declarationRecords'] is not None:
            self.__declaration_records = []
            for record_data in response['declarationRecords']:
                # 如果 DeclarationRecord 的构造函数有特定参数，这里的初始化方式可能需要调整
                record = DeclarationRecord()
                record.parse_rsp_body(record_data)
                self.__declaration_records.append(record)
