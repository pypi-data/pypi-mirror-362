import json

from alipayplusmcp.sdk.model.amount import Amount
from alipayplusmcp.sdk.model.customs_info import CustomsInfo
from alipayplusmcp.sdk.model.merchant_customs_info import MerchantCustomsInfo


class DeclarationRecord(object):
    def __init__(self):
        self.__customs_declaration_request_id = None
        self.__psp_declaration_request_id = None
        self.__psp_payment_id = None
        self.__customs = None # type: CustomsInfo
        self.__merchant_customs_info = None # type: MerchantCustomsInfo
        self.__declaration_amount = None # type: Amount
        self.__is_split = None
        self.__reference_order_id = None
        self.__declaration_request_status = None
        self.__modified_time = None
        self.__customs_result_code = None
        self.__customs_result_description = None
        self.__customs_result_returned_time = None


    @property
    def customs_declaration_request_id(self):
        return self.__customs_declaration_request_id

    @customs_declaration_request_id.setter
    def customs_declaration_request_id(self, value):
        self.__customs_declaration_request_id = value

    @property
    def psp_declaration_request_id(self):
        return self.__psp_declaration_request_id

    @psp_declaration_request_id.setter
    def psp_declaration_request_id(self, value):
        self.__psp_declaration_request_id = value

    @property
    def psp_payment_id(self):
        return self.__psp_payment_id

    @psp_payment_id.setter
    def psp_payment_id(self, value):
        self.__psp_payment_id = value

    @property
    def customs(self):
        return self.__customs

    @customs.setter
    def customs(self, value):
        self.__customs = value

    @property
    def merchant_customs_info(self):
        return self.__merchant_customs_info

    @merchant_customs_info.setter
    def merchant_customs_info(self, value):
        self.__merchant_customs_info = value

    @property
    def declaration_amount(self):
        return self.__declaration_amount

    @declaration_amount.setter
    def declaration_amount(self, value):
        self.__declaration_amount = value

    @property
    def is_split(self):
        return self.__is_split

    @is_split.setter
    def is_split(self, value):
        self.__is_split = value

    @property
    def reference_order_id(self):
        return self.__reference_order_id

    @reference_order_id.setter
    def reference_order_id(self, value):
        self.__reference_order_id = value

    @property
    def declaration_request_status(self):
        return self.__declaration_request_status

    @declaration_request_status.setter
    def declaration_request_status(self, value):
        self.__declaration_request_status = value

    @property
    def modified_time(self):
        return self.__modified_time

    @modified_time.setter
    def modified_time(self, value):
        self.__modified_time = value

    @property
    def customs_result_code(self):
        return self.__customs_result_code

    @customs_result_code.setter
    def customs_result_code(self, value):
        self.__customs_result_code = value

    @property
    def customs_result_description(self):
        return self.__customs_result_description

    @customs_result_description.setter
    def customs_result_description(self, value):
        self.__customs_result_description = value

    @property
    def customs_result_returned_time(self):
        return self.__customs_result_returned_time

    @customs_result_returned_time.setter
    def customs_result_returned_time(self, value):
        self.__customs_result_returned_time = value

    def to_aps_dict(self):
        params = dict()
        if hasattr(self, "customs_declaration_request_id") and self.customs_declaration_request_id:
            params['customsDeclarationRequestId'] = self.customs_declaration_request_id
        if hasattr(self, "psp_declaration_request_id") and self.psp_declaration_request_id:
            params['pspDeclarationRequestId'] = self.psp_declaration_request_id
        if hasattr(self, "psp_payment_id") and self.psp_payment_id:
            params['pspPaymentId'] = self.psp_payment_id
        if hasattr(self, "customs") and self.customs:
            params['customs'] = self.customs.to_aps_dict()
        if hasattr(self, "merchant_customs_info") and self.merchant_customs_info:
            params['merchantCustomsInfo'] = self.merchant_customs_info.to_aps_dict()
        if hasattr(self, "declaration_amount") and self.declaration_amount:
            params['declarationAmount'] = self.declaration_amount.to_aps_dict()
        if hasattr(self, "is_split") and self.is_split is not None:
            params['isSplit'] = self.is_split
        if hasattr(self, "reference_order_id") and self.reference_order_id:
            params['referenceOrderId'] = self.reference_order_id
        if hasattr(self, "declaration_request_status") and self.declaration_request_status:
            params['declarationRequestStatus'] = self.declaration_request_status
        if hasattr(self, "modified_time") and self.modified_time:
            params['modifiedTime'] = self.modified_time
        if hasattr(self, "customs_result_code") and self.customs_result_code:
            params['customsResultCode'] = self.customs_result_code
        if hasattr(self, "customs_result_description") and self.customs_result_description:
            params['customsResultDescription'] = self.customs_result_description
        if hasattr(self, "customs_result_returned_time") and self.customs_result_returned_time:
            params['customsResultReturnedTime'] = self.customs_result_returned_time
        return params

    def parse_rsp_body(self, body_data):
        if type(body_data) == str:
            body_data = json.loads(body_data)

        if 'customsDeclarationRequestId' in body_data:
            self.customs_declaration_request_id = body_data['customsDeclarationRequestId']

        if 'pspDeclarationRequestId' in body_data:
            self.psp_declaration_request_id = body_data['pspDeclarationRequestId']

        if 'pspPaymentId' in body_data:
            self.psp_payment_id = body_data['pspPaymentId']

        if 'customs' in body_data and body_data['customs'] is not None:
            customs_info = CustomsInfo()
            customs_info.parse_rsp_body(body_data['customs'])
            self.customs = customs_info

        if 'merchantCustomsInfo' in body_data and body_data['merchantCustomsInfo'] is not None:
            merchant_customs_info = MerchantCustomsInfo()
            merchant_customs_info.parse_rsp_body(body_data['merchantCustomsInfo'])
            self.merchant_customs_info = merchant_customs_info

        if 'declarationAmount' in body_data and body_data['declarationAmount'] is not None:
            declaration_amount = Amount()
            declaration_amount.parse_rsp_body(body_data['declarationAmount'])
            self.declaration_amount = declaration_amount

        if 'isSplit' in body_data:
            self.is_split = body_data['isSplit']

        if 'referenceOrderId' in body_data:
            self.reference_order_id = body_data['referenceOrderId']

        if 'declarationRequestStatus' in body_data:
            self.declaration_request_status = body_data['declarationRequestStatus']

        if 'modifiedTime' in body_data:
            self.modified_time = body_data['modifiedTime']

        if 'customsResultCode' in body_data:
            self.customs_result_code = body_data['customsResultCode']

        if 'customsResultDescription' in body_data:
            self.customs_result_description = body_data['customsResultDescription']

        if 'customsResultReturnedTime' in body_data:
            self.customs_result_returned_time = body_data['customsResultReturnedTime']
