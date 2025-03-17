# import ghasedakpack
import requests
import json


def sms_test_lowSMS(number="09133772351", input_message="هیچ پیامی برای نمایش ذخیره نشده است. لفو11"):
    url = "https://gateway.ghasedak.me/rest/api/v1/WebService/SendSingleSMS"
    payload = json.dumps({
        "sendDate": "2024-07-03T07:22:15.842Z",
        "lineNumber": "30006703249249",
        "receptor": number,
        "message": input_message,
        "clientReferenceId": "string",
        "udh": True
    })
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': "f0bd847ec0cbb0969c00a9ae1e835e02e04f4ec3ba086a088df012c4f9fd68efqABKusnCeeGzXcPk"
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
