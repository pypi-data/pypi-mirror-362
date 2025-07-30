import os
import sys

from alipayplusmcp.server import Account, serve


def main_cli():
    # 定义所需环境变量的名称和默认值（如果适用）
    env_vars_config = {
        "GATEWAY_URL": "https://open-sea-global.alipayplus.com",
        "CLIENT_ID": None, # 商户分配的Id
        "MERCHANT_PRIVATE_KEY": None,  # 商户私钥
        "ALIPAY_PUBLIC_KEY": None,  # 平台公钥
        "PAYMENT_REDIRECT_URL": "",
        "PAYMENT_NOTIFY_URL": "http://localhost:8080/notify",
        "SETTLEMENT_CURRENCY": "",
        "MERCHANT_NAME": "Alipayplus MCP",
        "MERCHANT_ID":"M0000000001",
        "MERCHANT_MCC":"5411",
        "MERCHANT_REGION":"CN",
    }

    account_data = {}
    missing_vars = []

    for var_name, default_value in env_vars_config.items():
        var_value = os.getenv(var_name)
        if var_value is None:
            if default_value is not None:
                print(f"Warning: Environment variable {var_name} not set. Using default value: '{default_value}'")
                account_data[var_name.lower()] = default_value # Convert keys to lowercase to match Account attributes
            else:
                missing_vars.append(var_name)
        else:
            account_data[var_name.lower()] = var_value

    if missing_vars:
        print(f"Error: Required environment variables are not set: {', '.join(missing_vars)}")
        print("Please set these environment variables before running the application.")
        sys.exit(1) # Exit program with error code 1


    # 创建 Account 对象
    account = Account()
    account.gateway_url = account_data.get('gateway_url')
    account.client_id = account_data.get('client_id')
    account.merchant_private_key = account_data.get('merchant_private_key')
    account.alipay_public_key = account_data.get('alipay_public_key')
    account.payment_redirect_url = account_data.get('payment_redirect_url')
    account.payment_notify_url = account_data.get('payment_notify_url')
    account.settlement_currency = account_data.get('settlement_currency')
    account.merchant_name = account_data.get('merchant_name')
    account.merchant_id = account_data.get('merchant_id')
    account.merchant_mcc = account_data.get('merchant_mcc')
    account.merchant_region = account_data.get('merchant_region')

    serve(account)


if __name__ == '__main__':
    main_cli()