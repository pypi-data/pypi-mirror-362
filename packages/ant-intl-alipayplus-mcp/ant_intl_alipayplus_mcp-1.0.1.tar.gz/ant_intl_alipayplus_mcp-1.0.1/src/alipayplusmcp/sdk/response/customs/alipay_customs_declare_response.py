from alipayplusmcp.sdk.model.amount import Amount
from alipayplusmcp.sdk.response.alipay_response import AlipayResponse


class AlipayCustomsDeclareResponse(AlipayResponse):

    def __init__(self, rsp_body):
        super(AlipayCustomsDeclareResponse, self).__init__()
        self.__psp_payment_id = None
        self.__psp_declaration_request_id = None
        self.__psp_customs_code = None
        self.__clearing_channel = None
        self.__clearing_transaction_id = None
        self.__psp_order_amount = None # type: Amount
        self.__identity_check_result = None
        self.__parse_rsp_body(rsp_body)


    @property
    def psp_payment_id(self):
        return self.__psp_payment_id

    @property
    def psp_declaration_request_id(self):
        return self.__psp_declaration_request_id

    @property
    def psp_customs_code(self):
        return self.__psp_customs_code

    @property
    def clearing_channel(self):
        return self.__clearing_channel

    @property
    def clearing_transaction_id(self):
        return self.__clearing_transaction_id

    @property
    def psp_order_amount(self):
        return self.__psp_order_amount

    @property
    def identity_check_result(self):
        return self.__identity_check_result

    def __parse_rsp_body(self, rsp_body):
        response = super(AlipayCustomsDeclareResponse, self).parse_rsp_body(rsp_body)
        if 'pspPaymentId' in response:
            self.__psp_payment_id = response['pspPaymentId']
        if 'pspDeclarationRequestId' in response:
            self.__psp_declaration_request_id = response['pspDeclarationRequestId']
        if 'pspCustomsCode' in response:
            self.__psp_customs_code = response['pspCustomsCode']
        if 'clearingChannel' in response:
            self.__clearing_channel = response['clearingChannel']
        if 'clearingTransactionId' in response:
            self.__clearing_transaction_id = response['clearingTransactionId']
        if 'pspOrderAmount' in response:
            self.__psp_order_amount = Amount(response['pspOrderAmount']['currency'], response['pspOrderAmount']['value'])
        if 'identityCheckResult' in response:
            self.__identity_check_result = response['identityCheckResult']
