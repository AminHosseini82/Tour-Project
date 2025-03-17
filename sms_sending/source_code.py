# import ghasedakpack
import requests
import json
from email_sending.warining_sms.massage_creadit_low import warining_smsCredit_low
from colorama import Fore, Style
from sms_sending.warining_sms.source_code_lowSMS import sms_test_lowSMS


# def check_balance():
#     url = "https://gateway.ghasedak.me/rest/api/v1/WebService/GetAccountInformation"
#     headers = {
#         'Content-Type': 'application/json',
#         'apikey': "f0bd847ec0cbb0969c00a9ae1e835e02e04f4ec3ba086a088df012c4f9fd68efqABKusnCeeGzXcPk"
#     }
#
#     try:
#         response = requests.get(url, headers=headers)
#         print("""this is for Check_balance Method for Check account info 👇""")
#         print("کد وضعیت HTTP:", response.status_code)
#         print("پاسخ کامل سرور:", response.text)
#
#         if response.status_code == 200:
#             account_info = response.json()
#             data = account_info.get("data", {})  # تغییر "Data" به "data"
#             credit = data.get("credit", "نامشخص")  # تغییر "Credit" به "credit"
#             expire_date = data.get("expireDate", "نامشخص")  # تغییر "ExpireDate" به "expireDate"
#             plan = data.get("plan", "نامشخص")  # تغییر "Plan" به "plan"
#             print(f"مقدار اعتبار باقیمانده: {credit} ریال")
#             if isinstance(credit, int) and credit < 30000:
#                 sms_test(number="09133772351" , input_message="اخطار: اعتبار سامانه قاصدک برای سایت شما کمتر از 3 هزار تومان است. لفو11")
#                 warining_smsCredit_low()
#
#
#             # print(plan)
#             # print(isinstance(credit, int))  # Output: True
#             print(f"تاریخ انقضا: {expire_date}")
#             print(f"نوع پلن: {plan}")
#         else:
#             print("خطا در دریافت اطلاعات: کد وضعیت", response.status_code)
#     except requests.exceptions.RequestException as e:
#         print("خطای اتصال:", str(e))


# ----------------------------------------------------------------------------------------------


def sms_test(number="09133772351", input_message="هیچ پیامی برای نمایش ذخیره نشده است. لفو11"):
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

    # برای چک کردن مقدار حساب ای که دارن👇


    url = "https://gateway.ghasedak.me/rest/api/v1/WebService/GetAccountInformation"
    headers = {
        'Content-Type': 'application/json',
        'apikey': "f0bd847ec0cbb0969c00a9ae1e835e02e04f4ec3ba086a088df012c4f9fd68efqABKusnCeeGzXcPk"
    }

    try:
        response = requests.get(url, headers=headers)
        print(Fore.BLUE + "this is for Check_balance Method for Check account info 👇")
        print(Style.RESET_ALL)  # Reset colors
        print()
        print("کد وضعیت HTTP:", response.status_code)
        print("پاسخ کامل سرور:", response.text)

        if response.status_code == 200:
            account_info = response.json()
            data = account_info.get("data", {})  # تغییر "Data" به "data"
            credit = data.get("credit", "نامشخص")  # تغییر "Credit" به "credit"
            expire_date = data.get("expireDate", "نامشخص")  # تغییر "ExpireDate" به "expireDate"
            plan = data.get("plan", "نامشخص")  # تغییر "Plan" به "plan"
            print(f"مقدار اعتبار باقیمانده: {credit} ریال")
            if isinstance(credit, int) and credit < 30000:
                sms_test_lowSMS(number="09133772351",
                         input_message="اخطار: اعتبار سامانه قاصدک برای سایت شما کمتر از 3 هزار تومان است. لفو11")
                warining_smsCredit_low()
            # print(plan)
            # print(isinstance(credit, int))  # Output: True
            # print(f"تاریخ انقضا: {expire_date}")
            # print(f"نوع پلن: {plan}")
        else:
            print("خطا در دریافت اطلاعات: کد وضعیت", response.status_code)
    except requests.exceptions.RequestException as e:
        print("خطای اتصال:", str(e))

# ----------------------------------------------------------------------------------------------

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
