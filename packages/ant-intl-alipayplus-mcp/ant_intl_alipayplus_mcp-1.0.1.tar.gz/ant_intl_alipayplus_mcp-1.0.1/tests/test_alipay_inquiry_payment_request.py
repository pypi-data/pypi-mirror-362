import os
import unittest

from dotenv import load_dotenv

from alipayplusmcp.sdk.default_alipay_client import DefaultAlipayClient
from alipayplusmcp.sdk.request.pay.alipay_inquiry_payment_request import AlipayInquiryPaymentRequest
from alipayplusmcp.sdk.response.pay.alipay_inquiry_payment_response import AlipayInquiryPaymentResponse


class TestDefaultAlipayClient(unittest.TestCase):

    def setUp(self):
        load_dotenv()  # 尝试从项目根目录或当前工作目录加载 .env
        self.gateway_url = os.environ.get("TEST_GATEWAY_URL", "https://open-sea-global.alipay.com")
        self.client_id = os.environ.get("TEST_CLIENT_ID", "test_client_id_from_env")
        self.merchant_private_key = os.environ.get("TEST_MERCHANT_PRIVATE_KEY", "dummy_private_key_from_env")
        self.alipay_public_key = os.environ.get("TEST_ALIPAY_PUBLIC_KEY", "dummy_public_key_from_env")

        self.client = DefaultAlipayClient(
            gateway_url=self.gateway_url,
            client_id=self.client_id,
            merchant_private_key=self.merchant_private_key,
            alipay_public_key=self.alipay_public_key
        )


    def test_initialization_is_sandbox(self):
        alipayInquiryRequest = AlipayInquiryPaymentRequest()

        alipayInquiryRequest.payment_request_id = 'pay_1089760038715669_102775745070000'

        resp = self.client.execute(alipayInquiryRequest)

        payResp = AlipayInquiryPaymentResponse(resp)
        self.assertEquals(payResp.result.result_code, 'SUCCESS')
        self.assertEquals(payResp.payment_result.result_code, 'ORDER_IS_CLOSED')


if __name__ == '__main__':
    # 这部分允许你直接运行这个测试文件
    unittest.main()
