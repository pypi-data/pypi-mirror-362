import json

from alipayplusmcp.sdk.model.AlipayPlusPathConstant import AlipayPlusPathConstants
from alipayplusmcp.sdk.model.amount import Amount
from alipayplusmcp.sdk.model.attachment import Attachment
from alipayplusmcp.sdk.model.buyer import Buyer
from alipayplusmcp.sdk.model.merchant import Merchant
from alipayplusmcp.sdk.model.proof_of_delivery import ProofOfDelivery
from alipayplusmcp.sdk.model.transaction_receipt import TransactionReceipt
from alipayplusmcp.sdk.request.alipay_request import AlipayRequest

# https://docs.alipayplus.com/alipayplus/alipayplus/api_acq/response_escalation?role=ACQP&product=Payment1&version=1.4.6
class AlipayResponseEscalationRequest(AlipayRequest):

    def __init__(self):
        super(AlipayResponseEscalationRequest, self).__init__(AlipayPlusPathConstants.RESPONSE_ESCALATION_PATH)
        self.__dispute_request_id = None
        self.__refund_type = None
        self.__refund_amount = None #type: Amount
        self.__planned_refund_time = None
        self.__transaction_receipt = None #type: TransactionReceipt
        self.__proof_of_delivery = None #type: ProofOfDelivery
        self.__merchant_information = None #type: Merchant
        self.__end_user_information = None #type: Buyer
        self.__other_documentation = None #type: Attachment
        self.__remarks = None


    @property
    def dispute_request_id(self):
        return self.__dispute_request_id

    @dispute_request_id.setter
    def dispute_request_id(self, value):
        self.__dispute_request_id = value

    @property
    def refund_type(self):
        return self.__refund_type

    @refund_type.setter
    def refund_type(self, value):
        self.__refund_type = value

    @property
    def refund_amount(self):
        return self.__refund_amount

    @refund_amount.setter
    def refund_amount(self, value):
        self.__refund_amount = value

    @property
    def planned_refund_time(self):
        return self.__planned_refund_time

    @planned_refund_time.setter
    def planned_refund_time(self, value):
        self.__planned_refund_time = value

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

    @property
    def remarks(self):
        return self.__remarks

    @remarks.setter
    def remarks(self, value):
        self.__remarks = value

    def to_aps_json(self):
        json_str = json.dumps(obj=self.__to_aps_dict(), default=lambda o: o.to_aps_dict(), indent=3)
        return json_str

    def __to_aps_dict(self):
        params = dict()

        if hasattr(self, "dispute_request_id") and self.dispute_request_id:
            params['disputeRequestId'] = self.dispute_request_id

        if hasattr(self, "refund_type") and self.refund_type:
            params['refundType'] = self.refund_type

        if hasattr(self, "refund_amount") and self.refund_amount:
            params['refundAmount'] = self.refund_amount

        if hasattr(self, "planned_refund_time") and self.planned_refund_time:
            params['plannedRefundTime'] = self.planned_refund_time

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

        if hasattr(self, "remarks") and self.remarks:
            params['remarks'] = self.remarks

        return params
