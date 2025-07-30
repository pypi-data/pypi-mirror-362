import json
import unittest

from alipayplusmcp.sdk.model.amount import Amount
from alipayplusmcp.sdk.model.customs_info import CustomsInfo
from alipayplusmcp.sdk.model.declaration_record import DeclarationRecord
from alipayplusmcp.sdk.model.merchant_customs_info import MerchantCustomsInfo
from alipayplusmcp.sdk.response.customs.alipay_customs_inquire_response import AlipayCustomsInquireResponse
from alipayplusmcp.sdk.response.result_status_type import ResultStatusType


class TestAlipayCustomsInquireResponse(unittest.TestCase):

    def test_parse_response(self):
        # Mock response body based on the provided JSON
        mock_response_body = json.dumps({
            "result": {
                "resultCode": "SUCCESS",
                "resultMessage": "Success",
                "resultStatus": "S"
            },
            "declarationRequestsNotFound": [
                "2021081900000000000000002"
            ],
            "declarationRecords": [
                {
                    "customsDeclarationRequestId": "2021081900000000000000001",
                    "pspDeclarationRequestId": "2013112611001004680073950000",
                    "pspPaymentId": "202108120000000231200000",
                    "customs": {
                        "customsCode": "HANGZHOU",
                        "region": "CN"
                    },
                    "merchantCustomsInfo": {
                        "merchantCustomsCode": "test_merchant_customs_code",
                        "merchantCustomsName": "test_merchant_customs_name"
                    },
                    "declarationAmount": {
                        "currency": "CNY",
                        "value": "100"
                    },
                    "isSplit": "true",
                    "referenceOrderId": "P202108120000000231280000",
                    "declarationRequestStatus": "WAITING_FOR_PROCESSING",
                    "modifiedTime": "2021-01-01T12:08:55Z",
                    "customsResultCode": "2",
                    "customsResultDescription": "success_201508201108237064750527108110000",
                    "customsResultReturnedTime": "2021-01-01T12:08:55Z"
                }
            ]
        })

        # Create response object with mock data
        response = AlipayCustomsInquireResponse(mock_response_body)

        # Verify result
        self.assertIsNotNone(response.result)
        self.assertEqual("SUCCESS", response.result.result_code)
        self.assertEqual("Success", response.result.result_message)
        self.assertEqual(ResultStatusType.S, response.result.result_status)

        # Verify declarationRequestsNotFound
        self.assertIsNotNone(response.declaration_requests_not_found)
        self.assertEqual(1, len(response.declaration_requests_not_found))
        self.assertEqual("2021081900000000000000002", response.declaration_requests_not_found[0])

        # Verify declarationRecords
        self.assertIsNotNone(response.declaration_records)
        self.assertEqual(1, len(response.declaration_records))

        record = response.declaration_records[0]
        self.assertIsInstance(record, DeclarationRecord)
        self.assertEqual("2021081900000000000000001", record.customs_declaration_request_id)
        self.assertEqual("2013112611001004680073950000", record.psp_declaration_request_id)
        self.assertEqual("202108120000000231200000", record.psp_payment_id)

        # Verify customs info
        self.assertIsInstance(record.customs, CustomsInfo)
        self.assertEqual("HANGZHOU", record.customs.customs_code)
        self.assertEqual("CN", record.customs.region)

        # Verify merchant customs info
        self.assertIsInstance(record.merchant_customs_info, MerchantCustomsInfo)
        self.assertEqual("test_merchant_customs_code", record.merchant_customs_info.merchant_customs_code)
        self.assertEqual("test_merchant_customs_name", record.merchant_customs_info.merchant_customs_name)

        # Verify declaration amount
        self.assertIsInstance(record.declaration_amount, Amount)
        self.assertEqual("CNY", record.declaration_amount.currency)
        self.assertEqual("100", record.declaration_amount.value)

        # Verify other fields
        self.assertEqual("true", record.is_split)
        self.assertEqual("P202108120000000231280000", record.reference_order_id)
        self.assertEqual("WAITING_FOR_PROCESSING", record.declaration_request_status)
        self.assertEqual("2021-01-01T12:08:55Z", record.modified_time)
        self.assertEqual("2", record.customs_result_code)
        self.assertEqual("success_201508201108237064750527108110000", record.customs_result_description)
        self.assertEqual("2021-01-01T12:08:55Z", record.customs_result_returned_time)


if __name__ == '__main__':
    unittest.main()
