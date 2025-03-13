from multiprocessing.connection import answer_challenge
import ghasedakpack
from ghasedakpack import Ghasedak
import requests
import json


def sms_test():
    url = "https://gateway.ghasedak.me/rest/api/v1/WebService/SendSingleSMS"

    payload = json.dumps({
        "sendDate": "2024-07-03T07:22:15.842Z",
        "lineNumber": "30006703249249",
        "receptor": "string",
        "message": "amin hoosseini لغو 11",
        "clientReferenceId": "1",
        "udh": False
    })
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': "4f5508bedeaa98699e6b7f2f76e44ba4017c1992c1ef749fa7242a8283c1ba5asYAhj5sYUhET4uM7"
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

# def sms_test():
#     sms = ghasedakpack.Ghasedak('4f5508bedeaa98699e6b7f2f76e44ba4017c1992c1ef749fa7242a8283c1ba5asYAhj5sYUhET4uM7')
#     message = "this is just a test! لغو 11"
#     my_number_1 = "09133772351"
#     line_number = "30006703249249"
#     context = {
#         "message" : message,"receptor" : my_number_1 , "linenumber":line_number
#     }
#     answer = sms.send(context)
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
