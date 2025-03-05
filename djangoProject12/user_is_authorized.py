# from django.http import HttpResponseForbidden
#
#
#
# def user_is_authorized(view_func):
#     def wrapper(request, *args, **kwargs):
#         if request.user.is_authenticated:
#             if request.user.email == 'bita4akhgar@gmail.com':
#                 print("User is authorized")
#                 return view_func(request, *args, **kwargs)
#         print("User is not authorized")
#         return HttpResponseForbidden("شما مجاز به انجام این عملیات نیستید!")
#     return wrapper