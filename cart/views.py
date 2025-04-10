from django.http import HttpResponseForbidden
from accounts.models import UserProfile
from sms_sending.source_code import sms_test
from tour.models import tour, Profile
from .forms import PaymentForm
# this is for sending email!
from email_sending.cart.sending_email import reject_message_email
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Payment, CartItem, Order
from tour.models import tour  # مدل تور رو وارد کن
from tourism.models import tourism  # مدل گردشگری رو وارد کن (اگه اپ جدا داری)
from email_sending.cart.sending_email import confirmation_message_email


# Create your views here.

# TODO must change the way HttpResponseForbidden to Error not accesses.
def user_is_authorized(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.email == 'aminhosseini822003@gmail.com':
                print("User is authorized")
                return view_func(request, *args, **kwargs)
        print("User is not authorized")
        return HttpResponseForbidden("شما مجاز به انجام این عملیات نیستید!")

    return wrapper


# cart/views.py

@login_required
@user_is_authorized
def admin_payment_review(request):
    payments = Payment.objects.all()
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        action = request.POST.get('action')
        payment = get_object_or_404(Payment, id=payment_id)

        if action == 'approve':
            order = payment.order
            cart_items = order.items.all()
            user_profile = Profile.objects.get(user=order.buyer)  # پروفایل کاربر
            email_user = payment.order.buyer.email
            confirmation_message_email(email_user)


            # TODO: must add a Gmail to say your Ticket is ready
            # TODO: must say in gmail : میتونید بلیط های خریداری شده خودتون رو در پروفایل خود مشاهده بکنید.
            # TODO: and must say also : سفر خوبی تیم سرای سفر برای شما ارزو دارد.
            # TODO: must add SMS in this also like gmail.

            # کم کردن ظرفیت و اضافه کردن به پروفایل
            for item in cart_items:
                if item.tourBuyed:
                    tour_item = item.tourBuyed
                    tour_item.capacity -= item.quantityItem
                    if tour_item.capacity < 0:
                        tour_item.capacity = 0
                    tour_item.save()
                    user_profile.tours.add(tour_item)  # اضافه کردن تور به پروفایل
                elif item.tourismBuyed:
                    tourism_item = item.tourismBuyed
                    tourism_item.capacity_tourism -= item.quantityItem
                    if tourism_item.capacity_tourism < 0:
                        tourism_item.capacity_tourism = 0
                    tourism_item.save()
                    user_profile.tourisms.add(tourism_item)  # اضافه کردن گردشگری به پروفایل

            payment.is_verified = True
            payment.verified_by = request.user
            payment.save()
            return redirect('cart:admin_payment_review')

        elif action == 'reject':
            return redirect('cart:reject_payment_message', payment_id=payment.id)

    return render(request, 'cart/admin_payment_review.html', {'payments': payments})


# @login_required
# @user_is_authorized  # دکوراتور خودت
# def admin_payment_review(request):
#     payments = Payment.objects.all()
#     if request.method == 'POST':
#         payment_id = request.POST.get('payment_id')
#         action = request.POST.get('action')
#         payment = get_object_or_404(Payment, id=payment_id)
#
#         if action == 'approve':
#             # سفارش مربوط به پرداخت
#             order = payment.order
#             # آیتم‌های سفارش
#             cart_items = order.items.all()
#
#             # کم کردن ظرفیت برای هر آیتم
#             for item in cart_items:
#                 if item.tourBuyed:  # اگه تور باشه
#                     tour_item = item.tourBuyed
#                     tour_item.capacity -= item.quantityItem  # کم کردن ظرفیت
#                     if tour_item.capacity < 0:  # چک کردن ظرفیت منفی
#                         tour_item.capacity = 0  # نمی‌ذاریم منفی بشه
#                     tour_item.save()
#                 elif item.tourismBuyed:  # اگه گردشگری باشه
#                     tourism_item = item.tourismBuyed
#                     tourism_item.capacity_tourism -= item.quantityItem
#                     if tourism_item.capacity_tourism < 0:
#                         tourism_item.capacity_tourism = 0
#                     tourism_item.save()
#
#             # تأیید پرداخت
#             payment.is_verified = True
#             payment.verified_by = request.user
#             payment.save()
#             return redirect('cart:admin_payment_review')
#
#         elif action == 'reject':
#             return redirect('cart:reject_payment_message', payment_id=payment.id)
#
#     return render(request, 'cart/admin_payment_review.html', {'payments': payments})
#


# cart/views.py
# @login_required
# @user_is_authorized
# def admin_payment_review(request):
#     payments = Payment.objects.all()
#     if request.method == 'POST':
#         payment_id = request.POST.get('payment_id')
#         action = request.POST.get('action')
#         payment = get_object_or_404(Payment, id=payment_id)
#         if action == 'approve':
#             # TODO: اینجا باید باتوجه به تور یا گردشگری ای که خریده بره اون ظرفیتش رو کم بکنه
#             payment.is_verified = True
#             payment.verified_by = request.user
#             # tour_capacity=Payment.tour.capacity
#             payment.save()
#             return redirect('cart:admin_payment_review')
#         elif action == 'reject':
#             # TODO: خب باید اینجا هدایت بشه به همین صفحه ولی با این تفاوت که دیگه نباید پیام رد شد رو دوباره نمایش بده.
#             return redirect('cart:reject_payment_message', payment_id=payment.id)  # هدایت به صفحه پیام
#     return render(request, 'cart/admin_payment_review.html', {'payments': payments})


@login_required
def no_phone_number_error(request):
    # دریافت آدرس صفحه قبلی
    previous_page = request.META.get('HTTP_REFERER', '/')  # اگر صفحه قبلی وجود نداشت، به صفحه اصلی هدایت می‌کند
    return render(request, "cart/errors/no_phone_number_error.html", {'previous_page': previous_page})

# code for sending email and SMS to User uploading a Photo.
# when someone is_verified  is false will return this code!
@login_required
@user_is_authorized  # دکوراتور خودت
def reject_payment_message(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    success = False  # متغیر برای موفقیت

    if request.method == 'POST':
        message = request.POST.get('message', '')
        payment.is_verified = False
        payment.verified_by = request.user
        payment.save()
        user_email = payment.order.buyer.email
        user = payment.order.buyer
        try:
            phone_number = user.userprofile.phone_number
        except UserProfile.DoesNotExist:
            return redirect("cart:no_phone_number_error")
        # ارسال ایمیل (تابع خودت)
        reject_message_email(user_email, message)
        # mobile_piment = payment.order.buyer
        message_sms = message + "لغو11."

        sms_test(phone_number, message_sms)

        # مثلاً: reject_message_sms(payment.order.buyer.phone_number, message)

        success = True  # بعد از ارسال موفق
        return render(request, 'cart/reject_payment_message.html', {'payment': payment, 'success': success})

    return render(request, 'cart/reject_payment_message.html', {'payment': payment, 'success': success})


#
# @login_required
# @user_is_authorized
# def reject_payment_message(request, payment_id):
#     payment = get_object_or_404(Payment, id=payment_id)
#     if request.method == 'POST':
#         message = request.POST.get('message', '')
#         payment.is_verified = False
#         payment.verified_by = request.user
#         payment.save()
#
#         # TODO must input email sending!
#         # ارسال ایمیل
#         reject_message_email(payment.order.buyer.email, message)
#
#         # TODO must input SMS sending
#         # ارسال SMS (فرض می‌کنم کد SMS داری)
#
#         return redirect('cart:admin_payment_review')
#
#     return render(request, 'cart/reject_payment_message.html', {'payment': payment})
#

# @login_required
# @user_is_authorized
# def admin_payment_review(request):
#     payments = Payment.objects.all()
#     if request.method == 'POST':
#         payment_id = request.POST.get('payment_id')
#         action = request.POST.get('action')
#         payment = get_object_or_404(Payment, id=payment_id)
#         if action == 'approve':
#             payment.is_verified = True
#             payment.verified_by = request.user
#         elif action == 'reject':
#             payment.is_verified = False
#             payment.verified_by = request.user
#         payment.save()
#         return redirect('cart:admin_payment_review')
#     return render(request, 'cart/admin_payment_review.html', {'payments': payments})


def is_valid_capacity(request, type_buy, item_id, quantity) -> bool:
    if type_buy == 'tour':
        tour_capacity = get_object_or_404(tour, id=item_id).capacity
        return quantity <= tour_capacity and quantity > 0  # چک صفر و منفی
    elif type_buy == 'tourism':
        tourism_capacity = get_object_or_404(tourism, id=item_id).capacity_tourism
        return quantity <= tourism_capacity and quantity > 0  # چک صفر و منفی
    return False  # اگه نوع اشتباه باشه


# def is_valid_capacity(request, type_buy, item_id, quantity) -> bool:
#     if type_buy == 'tour':
#         tour_capacity = get_object_or_404(tour, id=item_id).capacity
#         if quantity > tour_capacity:
#             return False
#     else:
#         tourism_capacity = get_object_or_404(tourism, id=item_id).capacity_tourism
#         if quantity > tourism_capacity:
#             return False
#
#     return True


# اضافه کردن تور یا گردشگری به سبد خرید
@login_required
def add_to_cart(request, item_type, item_id):
    if item_type == 'tour':
        item = get_object_or_404(tour, id=item_id)
    elif item_type == 'tourism':
        item = get_object_or_404(tourism, id=item_id)
    else:
        return redirect('home')

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        if not is_valid_capacity(request, item_type, item_id, quantity):
            capacity = item.capacity if item_type == 'tour' else item.capacity_tourism
            context = {
                'item': item,
                'item_type': item_type,
                'capacity_error': f"تعداد بلیط‌ها ({quantity}) بیشتر از ظرفیت ({capacity}) است یا نامعتبر است",
                'item_capacity': capacity
            }
            return render(request, 'cart/add_to_cart.html', context)

        cart_item, created = CartItem.objects.get_or_create(
            buyer=request.user,
            tourBuyed=item if item_type == 'tour' else None,
            tourismBuyed=item if item_type == 'tourism' else None
        )
        if not created:
            cart_item.quantityItem += quantity
        else:
            cart_item.quantityItem = quantity
        cart_item.save()
        return redirect('cart:place_order')

    return render(request, 'cart/add_to_cart.html', {'item': item, 'item_type': item_type})


# @login_required
# def add_to_cart(request, item_type, item_id):
#     # item_type is tour or tourism.
#     type_want_to_buy = "None"
#     if item_type == 'tour':
#         item = get_object_or_404(tour, id=item_id)
#         type_want_to_buy = "tour"
#     elif item_type == 'tourism':
#         item = get_object_or_404(tourism, id=item_id)
#         type_want_to_buy = "tourism"
#     else:
#         # TODO must return a block page to sead this tour or tourism not find.
#         return redirect('home')  # یه صفحه پیش‌فرض اگه نوع اشتباه باشه
#
#     if request.method == 'POST':
#
#         # TODO: اگر تعداد بلیطی که میخواد بخره بیشتر از ظرفیت باشه ارور بده از این نوع شناور که نمیتونی بخری!!
#         # TODO: باید اینجا یک کوییری بزنی بعدش تعدادی که زده از اون تور یا گردشگری رو به دسس بیاری
#         # TODO: بعدش باید بری سراغ تعداد گردشگری بگی همچین گردشگری ای کم بده تعداش یا تور
#         quantity = int(request.POST.get('quantity', 1))
#         # TODO: اول باید اینجا یه بررسی بکنه ایا تعداد کاربر ها اگر کم بشه چی میشه؟
#         """
#         This function checks the number of tickets being sent to the website.
#         If the requested number of tickets is greater than the available tickets on the site, it shows an error.
#         If the number of tickets is less than or equal to the available tickets, it does nothing.
#         """
#         if is_valid_capacity(request, item_type, item_id, quantity):
#             pass
#         else:
#             # this will return a message floating to say capacity is {} and you can't buy it this.
#             item_capacity = get_object_or_404(type_want_to_buy, id=item_id).capacity
#             context = {
#                 "capacity_erore": "تعداد بلیط ها بیشتر از ظرفیت بلیط سایت هست",
#                 "item_capacity" : item_capacity
#             }
#             return render(request, 'cart/add_to_cart.html', context)
#
#         # if item_type == 'tour':
#         #     tour_capacity = get_object_or_404(tour, id=item_id).capacity
#         #     if quantity > tour_capacity:
#         #         return render(request, "")
#         # else:
#         #     tourism_capacity = get_object_or_404(tourism, id=item_id).capacity_tourism
#         #     if quantity > tourism_capacity:
#         #         return render(request, "")
#         cart_item, created = CartItem.objects.get_or_create(
#             buyer=request.user,
#             tourBuyed=item if item_type == 'tour' else None,
#             tourismBuyed=item if item_type == 'tourism' else None
#         )
#         if not created:
#             cart_item.quantityItem += quantity
#         else:
#             cart_item.quantityItem = quantity
#         cart_item.save()
#         # return redirect('cart_checkout')
#         return redirect('cart:place_order')  # تغییر از 'cart_checkout' به 'place_order'
#     # TODO must add a page, GROK page.
#     return render(request, 'cart/add_to_cart.html', {'item': item, 'item_type': item_type})


# صفحه تسویه‌حساب
# cart/views.py
# cart/views.py
# TODO: باید در این صفحه html یک دکمه بگذاری که برگرده به ثبت تور یا گردشگری ای که بود.
# cart/views.py

@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(buyer=request.user)
    total_price = sum(item.get_total() for item in cart_items)

    if request.method == 'POST':
        if 'delete_item' in request.POST:  # چک کن اگه درخواست حذف باشه
            item_id = request.POST.get('delete_item')
            CartItem.objects.filter(id=item_id, buyer=request.user).delete()
            return redirect('cart:place_order')  # برگرد به همون صفحه با سبد آپدیت‌شده

        # اگه درخواست ثبت سفارش باشه
        order = Order(buyer=request.user, total_price=total_price)
        order.save()
        order.items.set(cart_items)
        return redirect('cart:upload_payment', order_id=order.id)

    return render(request, 'cart/checkout.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def upload_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)

    # چک کن اگه پرداخت وجود داره
    try:
        payment = Payment.objects.get(order=order)
        # اگه پرداخت وجود داره، فقط آپدیتش کن
        if request.method == 'POST':
            form = PaymentForm(request.POST, request.FILES, instance=payment)
            if form.is_valid():
                form.save()
                return redirect('cart:payment_success')
    except Payment.DoesNotExist:
        # اگه پرداخت وجود نداره، یه پرداخت جدید بساز
        if request.method == 'POST':
            form = PaymentForm(request.POST, request.FILES)
            if form.is_valid():
                payment = form.save(commit=False)
                payment.order = order
                payment.save()
                return redirect('cart:payment_success')

    # نمایش فرم (برای GET یا اگه فرم معتبر نباشه)
    form = PaymentForm(instance=payment if 'payment' in locals() else None)
    return render(request, 'cart/upload_payment.html', {'form': form, 'order': order})


# The successful Massage for correct payment
# TODO this function should rename to show_payment_success
@login_required
def payment_success(request):
    return render(request, 'cart/payment_success.html')
