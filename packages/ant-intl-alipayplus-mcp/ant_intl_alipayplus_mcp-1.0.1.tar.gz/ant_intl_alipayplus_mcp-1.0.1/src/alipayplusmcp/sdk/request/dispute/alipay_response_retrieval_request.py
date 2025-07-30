import json

from alipayplusmcp.sdk.model.AlipayPlusPathConstant import AlipayPlusPathConstants
from alipayplusmcp.sdk.model.attachment import Attachment
from alipayplusmcp.sdk.model.buyer import Buyer
from alipayplusmcp.sdk.model.merchant import Merchant
from alipayplusmcp.sdk.model.order_status import OrderStatus
from alipayplusmcp.sdk.model.proof_of_delivery import ProofOfDelivery
from alipayplusmcp.sdk.model.transaction_receipt import TransactionReceipt
from alipayplusmcp.sdk.request.alipay_request import AlipayRequest

# https://docs.alipayplus.com/alipayplus/alipayplus/api_acq/response_retrieval?role=ACQP&product=Payment1&version=1.4.6
class AlipayResponseRetrievalRequest(AlipayRequest):

    def __init__(self):
        super(AlipayResponseRetrievalRequest, self).__init__(AlipayPlusPathConstants.RESPONSE_RETRIEVAL_PATH)
        self.__dispute_request_id = None
        self.__response_code = None # type: OrderStatus
        self.__transaction_receipt = None #type: TransactionReceipt
        self.__proof_of_delivery = None #type: ProofOfDelivery
        self.__merchant_information = None #type: Merchant
        self.__end_user_information = None #type: Buyer
        self.__other_documentation = None #type: list[Attachment]

    @property
    def dispute_request_id(self):
        return self.__dispute_request_id

    @dispute_request_id.setter
    def dispute_request_id(self, value):
        self.__dispute_request_id = value

    @property
    def response_code(self):
        return self.__response_code

    @response_code.setter
    def response_code(self, value):
        self.__response_code = value

    @property
    def transaction_receipt(self):
        return self.__transaction_receipt

    @transaction_receipt.setter
    def transaction_receipt(self, value):
        self.__transaction_receipt = value

    @property
    def proof_of_delivery(self):
        return self.__proof_of_delivery

    @proof_of_delivery.setter
    def proof_of_delivery(self, value):
        self.__proof_of_delivery = value

    @property
    def merchant_information(self):
        return self.__merchant_information

    @merchant_information.setter
    def merchant_information(self, value):
        self.__merchant_information = value

    @property
    def end_user_information(self):
        return self.__end_user_information

    @end_user_information.setter
    def end_user_information(self, value):
        self.__end_user_information = value

    @property
    def other_documentation(self):
        return self.__other_documentation

    @other_documentation.setter
    def other_documentation(self, value):
        self.__other_documentation = value

    def to_aps_json(self):
        json_str = json.dumps(obj=self.__to_aps_dict(), default=lambda o: o.to_aps_dict(), indent=3)
        return json_str

    def __to_aps_dict(self):
        params = dict()

        if hasattr(self, "dispute_request_id") and self.dispute_request_id:
            params['disputeRequestId'] = self.dispute_request_id

        if hasattr(self, "response_code") and self.response_code:
            params['responseCode'] = self.response_code

        if hasattr(self, "transaction_receipt") and self.transaction_receipt:
            params['transactionReceipt'] = self.transaction_receipt

        if hasattr(self, "proof_of_delivery") and self.proof_of_delivery:
            params['proofOfDelivery'] = self.proof_of_delivery

        if hasattr(self, "merchant_information") and self.merchant_information:
            params['merchantInformation'] = self.merchant_information

        if hasattr(self, "end_user_information") and self.end_user_information:
            params['endUserInformation'] = self.end_user_information

        if hasattr(self, "other_documentation") and self.other_documentation:
            params['otherDocumentation'] = self.other_documentation

        return params
