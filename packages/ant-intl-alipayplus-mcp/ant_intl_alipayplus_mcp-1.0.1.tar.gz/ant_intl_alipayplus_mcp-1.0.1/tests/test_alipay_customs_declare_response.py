import json
import unittest

from alipayplusmcp.sdk.model.amount import Amount
from alipayplusmcp.sdk.response.customs.alipay_customs_declare_response import AlipayCustomsDeclareResponse
from alipayplusmcp.sdk.response.result_status_type import ResultStatusType


class TestAlipayCustomsDeclareResponse(unittest.TestCase):

    def test_parse_response(self):
        # Mock response body based on the provided JSON
        mock_response_body = json.dumps({
            "result": {
                "resultCode": "SUCCESS",
                "resultMessage": "Success",
                "resultStatus": "S"
            },
            "pspPaymentId": "202108120000000231200000",
            "pspDeclarationRequestId": "2013112611001004680073950000",
            "pspCustomsCode": "31222699S7",
            "clearingTransactionId": "202108120000000808000000",
            "clearingChannel": "CUP",
            "pspOrderAmount": {
                "currency": "CNY",
                "value": "100"
            },
            "identityCheckResult": "CHECK_NOT_PASSED"
        })

        # Create response object with mock data
        response = AlipayCustomsDeclareResponse(mock_response_body)

        # Verify result
        self.assertIsNotNone(response.result)
        self.assertEqual("SUCCESS", response.result.result_code)
        self.assertEqual("Success", response.result.result_message)
        self.assertEqual(ResultStatusType.S, response.result.result_status)

        # Verify other fields
        self.assertEqual("202108120000000231200000", response.psp_payment_id)
        self.assertEqual("2013112611001004680073950000", response.psp_declaration_request_id)
        self.assertEqual("31222699S7", response.psp_customs_code)
        self.assertEqual("202108120000000808000000", response.clearing_transaction_id)
        self.assertEqual("CUP", response.clearing_channel)
        
        # Verify psp_order_amount
        self.assertIsNotNone(response.psp_order_amount)
        self.assertIsInstance(response.psp_order_amount, Amount)
        self.assertEqual("CNY", response.psp_order_amount.currency)
        self.assertEqual("100", response.psp_order_amount.value)
        
        # Verify identity_check_result
        self.assertEqual("CHECK_NOT_PASSED", response.identity_check_result)


if __name__ == '__main__':
    unittest.main()