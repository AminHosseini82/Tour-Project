# import ghasedakpack
import requests
import json


def sms_test(number = "09133958238"):
    url = "https://gateway.ghasedak.me/rest/api/v1/WebService/SendSingleSMS"
    payload = json.dumps({
        "sendDate": "2024-07-03T07:22:15.842Z",
        "lineNumber": "30006703249249",
        "receptor": number,
        "message": "سایت تور و گردشگری. لغو11",
        "clientReferenceId": "string",
        "udh": True
    })
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': "f0bd847ec0cbb0969c00a9ae1e835e02e04f4ec3ba086a088df012c4f9fd68efqABKusnCeeGzXcPk"
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

# def sms_test():
#     sms = ghasedakpack.Ghasedak('2b8dcce987651120477b7ec169cc69b3760de741cc010a76a46fae8447a6d56bf3vboVB2hmzyFgft')
#     message = "sdfsdf. لغو11"
#     my_number_1 = "09133772351"
#     line_number = "90002930"
#     answer = sms.send({
#         "message": message, "receptor": my_number_1, "linenumber": line_number
#     })

#
# def sms_test():
#     url = "https://gateway.ghasedak.me/rest/api/v1/WebService/SendSingleSMS"
#
#     payload = json.dumps({
#         "sendDate": "2024-07-03T07:22:15.842Z",
#         "lineNumber": "30006703249249",
#         "receptor": "string",
#         "message": "amin hoosseini لغو 11",
#         "clientReferenceId": "1",
#         "udh": False
#     })
#     headers = {
#         'Content-Type': 'application/json',
#         'ApiKey': "4f5508bedeaa98699e6b7f2f76e44ba4017c1992c1ef749fa7242a8283c1ba5asYAhj5sYUhET4uM7"
#     }
#
#     response = requests.request("POST", url, headers=headers, data=payload)
#
#     print(response.text)

#
#
# def sms_test():
#     # کلید جدیدت رو اینجا بذار
#     sms = Ghasedak("4f5508bedeaa98699e6b7f2f76e44ba4017c1992c1ef749fa7242a8283c1ba5asYAhj5sYUhET4uM7")
#     answer = sms.send({
#         "message": "تست ساده",
#         "receptor": "09133772351",
#         "linenumber": "90002930"
#     })
#     print(answer)
