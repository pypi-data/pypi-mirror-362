import os
import unittest

from dotenv import load_dotenv

from alipayplusmcp.sdk.default_alipay_client import DefaultAlipayClient
from alipayplusmcp.sdk.model.address import Address
from alipayplusmcp.sdk.model.amount import Amount
from alipayplusmcp.sdk.model.buyer import Buyer
from alipayplusmcp.sdk.model.env import Env
from alipayplusmcp.sdk.model.merchant import Merchant
from alipayplusmcp.sdk.model.order import Order
from alipayplusmcp.sdk.model.payment_factor import PaymentFactor
from alipayplusmcp.sdk.model.payment_method import PaymentMethod
from alipayplusmcp.sdk.model.settlement_strategy import SettlementStrategy
from alipayplusmcp.sdk.request.pay.alipay_pay_request import AlipayPayRequest
from alipayplusmcp.sdk.response.pay.alipay_pay_response import AlipayPayResponse


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
        alipayPayRequest = AlipayPayRequest()

        alipayPayRequest.payment_request_id = 'pay_1089760038715669_102775745070000'
        alipayPayRequest.payment_redirect_url = 'https://xmock.inc.alipay.net'
        alipayPayRequest.payment_notify_url = 'https://xmock.inc.alipay.net/api/Ipay/globalSite/automation/paymentNotify.htm'

        alipayPayRequest.user_region = 'PH'

        payment_factor_data = PaymentFactor()
        payment_factor_data.is_in_store_payment = 'false'
        payment_factor_data.is_cashier_payment = 'true'
        payment_factor_data.presentment_mode = 'UNIFIED'
        alipayPayRequest.payment_factor = payment_factor_data

        # order构建
        order_data = Order()
        order_data.reference_order_id = '102775745070000'
        order_data.order_description = 'test'
        order_data.order_amount = Amount('JPY','100')
        merchant_data = Merchant()
        merchant_data.reference_merchant_id = 'M0000000001'
        merchant_data.merchant_name = 'UGG'
        merchant_data.merchant_mcc = '5411'

        address_data = Address()
        address_data.region = 'JP'
        address_data.city = 'XXX'
        merchant_data.merchant_address = address_data

        env_data = Env()
        env_data.terminal_type = 'APP'
        env_data.os_type = 'IOS'
        order_data.env = env_data
        order_data.merchant = merchant_data

        buyer_data = Buyer()
        buyer_data.reference_buyer_id = '907410100070010000'
        order_data.buyer = buyer_data

        alipayPayRequest.order = order_data

        # 结算数据
        settlement_data = SettlementStrategy()
        settlement_data.settlement_currency = 'USD'
        alipayPayRequest.settlement_strategy = settlement_data

        # 支付方式
        method_data = PaymentMethod()
        method_data.payment_method_type = 'CONNECT_WALLET'
        alipayPayRequest.payment_method = method_data

        # 支付金额
        alipayPayRequest.payment_amount = Amount('JPY','100')

        resp = self.client.execute(alipayPayRequest)

        payResp = AlipayPayResponse(resp)
        self.assertEquals(payResp.result.result_code, 'PAYMENT_IN_PROCESS')


if __name__ == '__main__':
    # 这部分允许你直接运行这个测试文件
    unittest.main()
