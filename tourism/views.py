import os
from django.conf import settings
from .forms import tourism, tourismform
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TourismSearchForm
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import tourism, Purchase, Profile
from email_sending.tourism.create_tourism_email import create_tourism_massages
from email_sending.tourism.delete_tourism_email import delete_tourism_massages
from email_sending.tourism.edit_touriam_email import edit_tourism_massages

list = []
form = tourismform()
#
# @login_required(login_url='/accounts/login')
# def tourism_create(request):
#     user = request.user
#     list = []
#
#     if request.method == 'POST':
#         form = tourismform(request.POST, request.FILES)  # necessary if user wants to upload a picture
#         if form.is_valid():
#             instance = form.save(commit=False)  # lets us make some changes on the form before saving it on database
#             instance.clas = user  # Associate the tour with the logged-in user
#             instance.pic = request.FILES.get('image', False)  # Get the uploaded image
#
#             # Check if the title already exists in the list
#             if instance.title in list:
#                 tourisms = tourism.objects.filter(title=instance.title)
#                 tourisms.delete()  # Delete existing tours with the same title
#             instance.save()  # Save the new tour
#             return redirect('tourism:tourismpage')  # Redirect to the tour list or add page
#
#     else:
#         form = tourismform()  # Create a new form instance if not a POST request
#
#     # Get the tours created by the logged-in user
#     query = tourism.objects.filter(clas=user)
#
#     for tourww in query:
#         list.append(tourww.title)
#
#     return render(request, 'tourism/addtourism_page.html', {'form': form, 'tourisms': query})
# این پایینی کد قبلی بود
# def tourism_create(request):
#     user = request.user
#     existing_titles = []  # Use a different name
#
#     if request.method == 'POST':
#         form = tourismform(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.clas = user
#             instance.image = form.cleaned_data.get('image')  # Properly assign the image
#
#             # Check if the title already exists in the list
#             if instance.title in existing_titles:
#                 tourism.objects.filter(title=instance.title).delete()
#
#             instance.save()
#             return redirect('tourism:tourismpage')
#
#     else:
#         form = tourismform()
#
#     # Get the tours created by the logged-in user
#     query = tourism.objects.filter(clas=user)
#     for tour in query:
#         existing_titles.append(tour.title)
#
#     return render(request, 'tourism/addtourism_page.html', {'form': form, 'tourisms': query})

# این درست بوده من قایل کلش رو انداختم توی djangoProject12👇
def user_is_authorized(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.email == 'aminhosseini822003@gmail.com':
                print("User is authorized")
                return view_func(request, *args, **kwargs)
        print("User is not authorized")
        return HttpResponseForbidden("شما مجاز به انجام این عملیات نیستید!")

    return wrapper


# این درست بوده من قایل کلش رو انداختم توی djangoProject12👆


# ------------------------------------این کد درست بوده tourism_create👇---------------------------------------

# @login_required
# @user_is_authorized
# def tourism_create(request):
#     user = request.user
#     tourism_titles = set(tourism.objects.values_list('title_tourism', flat=True))  # دریافت عناوین تور های موجود
#
#     if request.method == 'POST':
#         form = tourismform(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.clas = user  # افزودن کاربر به عنوان فیلد ForeignKey
#             # استفاده از نام فیلد جدید
#             if instance.title_tourism in tourism_titles:
#                 tours = tourism.objects.filter(title_tourism=instance.title_tourism)
#                 tours.delete()
#             instance.save()
#             return redirect('tourism:tourismpage')
#
#     else:
#         form = tourismform()
#
#     user_tours = tourism.objects.filter(clas=user)
#
#     is_authorized = (user.email == 'bita4akhgar@gmail.com')
#     print("is_authorized:", is_authorized)  # پیام دیباگینگ
#
#     return render(request, 'tourism/addtourism_page.html', {
#         'form': form,
#         'tours_list': user_tours,
#         'is_authorized': is_authorized
#     })


# ------------------------------------این کد درست بوده tourism_create 👆---------------------------------------

@login_required
@user_is_authorized
def tourism_create(request):
    user = request.user
    user_email = "aminhosseini822003@gmail.com"
    tourism_titles = set(tourism.objects.values_list('title_tourism', flat=True))  # دریافت عناوین تور های موجود

    if request.method == 'POST':
        form = tourismform(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.clas = user  # افزودن کاربر به عنوان فیلد ForeignKey

            # چک کردن برای جلوگیری از مقادیر منفی در ظرفیت و هزینه
            if instance.capacity_tourism < 0:
                form.add_error('capacity_tourism', "ظرفیت نمی‌تواند عدد منفی باشد.")
            if instance.price_tourism < 0:
                form.add_error('price_tourism', "هزینه نمی‌تواند عدد منفی باشد.")

            # اگر خطایی وجود نداره، ذخیره کن
            if not form.errors:
                # استفاده از نام فیلد جدید
                if instance.title_tourism in tourism_titles:
                    tours = tourism.objects.filter(title_tourism=instance.title_tourism)
                    tours.delete()

                instance.save()
                # pk = instance.pk
                # tourism_item = get_object_or_404(tourism, id=pk)

                tourism_detile = {
                    'title': instance.title_tourism,
                    "firstdistination_tourism": instance.firstdistination_tourism,
                    "capacity_tourism": instance.capacity_tourism,
                    "image_tourism": instance.image_tourism,
                    "startdate_tourism": instance.startdate_tourism,
                    "price_tourism": instance.price_tourism,
                    "ticket_typetourism": instance.ticket_typetourism
                }

                # for key, value in tourism_detile.items():
                #     print(f"{key}: {value}")
                create_tourism_massages("aminhosseini822003@gmail.com", tourism_detile)

                return redirect('tourism:tourismpage')

    else:
        form = tourismform()

    user_tours = tourism.objects.filter(clas=user)

    is_authorized = (user.email == 'aminhosseini822003@gmail.com')
    print("is_authorized:", is_authorized)  # پیام دیباگینگ

    return render(request, 'tourism/addtourism_page.html', {
        'form': form,
        'tours_list': user_tours,
        'is_authorized': is_authorized
    })


# def tourism_create(request):
#     user = request.user
#     tourism_titles = set()
#
#     if request.method == 'POST':
#         form = tourismform(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.clas = user
#             # instance.image = form.cleaned_data['image']
#             if instance.title in tourism_titles:
#                 tours = tourism.objects.filter(title=instance.title)
#                 tours.delete()
#             instance.save()
#             return redirect('tourism:tourismpage')
#
#     else:
#         form = tourismform()
#
#     user_tours = tourism.objects.filter(clas=user)
#
#     is_authorized = (user.email == 'darya.yazdanpanah22@gmail.com')
#     print("is_authorized:", is_authorized)  # پیام دیباگینگ
#
#     return render(request, 'tourism/addtourism_page.html', {
#         'form': form,
#         'tours_list': user_tours,
#         'is_authorized': is_authorized
#     })


# ------------------------------این کد درست بوده ویرایش 20 قبل از درست کردن سرچ 👇---------------------------

# def tourism_view(request):
#     tourisms = tourism.objects.all()  # نام مدل باید با حرف بزرگ باشد: Tour
#     form = TourismSearchForm(request.GET)  # دریافت داده‌های فرم جستجو
#
#     if form.is_valid():
#         origin = form.cleaned_data.get('firstdistination_tourism')
#         # destination = form.cleaned_data.get('lastDestination')
#         # startdate = form.cleaned_data.get('startdate_persian')  # تاریخ رفت
#         # finishdate = form.cleaned_data.get('finishdate')  # تاریخ برگشت
#
#         # فیلتر کردن تورها بر اساس مبدا و مقصد
#         if origin:
#             tourisms = tourisms.filter(firstdistination_tourism__icontains=origin)
#         # if destination:
#         #     tourisms = tourisms.filter(lastDestination__icontains=destination)
#         # if startdate:
#         #     tourisms = tourisms.filter(startdate__gte=startdate)  # تاریخ شروع باید بزرگتر یا مساوی تاریخ انتخابی باشد
#         # if finishdate:
#         #     tourisms = tourisms.filter(finishdate__lte=finishdate)  # تاریخ برگشت باید کوچکتر یا مساوی تاریخ انتخابی باشد
#
#     return render(request, 'tourism/tourism_page.html', {'tourisms': tourisms, 'form': form})


# ------------------------------این کد درست بوده ویرایش 20 قبل از درست کردن سرچ 👆----------------------------

# ------------------------------این کد درست بوده ویرایش 21 یعد از درست کردن سرچ 👇----------------------------

# def tourism_view(request):
#     tourisms = tourism.objects.all()  # نام مدل باید با حرف بزرگ باشد: Tour
#     form = TourismSearchForm(request.GET)  # دریافت داده‌های فرم جستجو
#
#     if form.is_valid():
#         origin = form.cleaned_data.get('firstdistination_tourism')
#         title = form.cleaned_data.get('title_tourism')
#         # destination = form.cleaned_data.get('lastDestination')
#         # startdate = form.cleaned_data.get('startdate_persian')  # تاریخ رفت
#         # finishdate = form.cleaned_data.get('finishdate')  # تاریخ برگشت
#
#         # فیلتر کردن تورها بر اساس مبدا و عنوان
#         if origin:
#             tourisms = tourisms.filter(firstdistination_tourism__icontains=origin)
#         if title:
#             tourisms = tourisms.filter(title_tourism__icontains=title)
#         # if destination:
#         #     tourisms = tourisms.filter(lastDestination__icontains=destination)
#         # if startdate:
#         #     tourisms = tourisms.filter(startdate__gte=startdate)  # تاریخ شروع باید بزرگتر یا مساوی تاریخ انتخابی باشد
#         # if finishdate:
#         #     tourisms = tourisms.filter(finishdate__lte=finishdate)  # تاریخ برگشت باید کوچکتر یا مساوی تاریخ انتخابی باشد
#
#     return render(request, 'tourism/tourism_page.html', {'tourisms': tourisms, 'form': form})


# ------------------------------این کد درست بوده ویرایش 21 یعد از درست کردن سرچ 👆----------------------------

def tourism_view(request):
    tourisms = tourism.objects.all()  # نام مدل باید با حرف بزرگ باشد: Tour
    form = TourismSearchForm(request.GET)  # دریافت داده‌های فرم جستجو

    if form.is_valid():
        query = form.cleaned_data.get('query')
        # origin = form.cleaned_data.get('firstdistination_tourism')
        # title = form.cleaned_data.get('title_tourism')
        # destination = form.cleaned_data.get('lastDestination')
        # startdate = form.cleaned_data.get('startdate_persian')  # تاریخ رفت
        # finishdate = form.cleaned_data.get('finishdate')  # تاریخ برگشت

        # فیلتر کردن تورها بر اساس query (عنوان یا مبدا)
        if query:
            tourisms = tourisms.filter(
                title_tourism__icontains=query
            ) | tourisms.filter(
                firstdistination_tourism__icontains=query
            )
        # if origin:
        #     tourisms = tourisms.filter(firstdistination_tourism__icontains=origin)
        # if title:
        #     tourisms = tourisms.filter(title_tourism__icontains=title)
        # if destination:
        #     tourisms = tourisms.filter(lastDestination__icontains=destination)
        # if startdate:
        #     tourisms = tourisms.filter(startdate__gte=startdate)  # تاریخ شروع باید بزرگتر یا مساوی تاریخ انتخابی باشد
        # if finishdate:
        #     tourisms = tourisms.filter(finishdate__lte=finishdate)  # تاریخ برگشت باید کوچکتر یا مساوی تاریخ انتخابی باشد

    return render(request, 'tourism/tourism_page.html', {'tourisms': tourisms, 'form': form})


@login_required
def deletetourism(request, pk):
    # بررسی اینکه آیا کاربر مجاز است
    if request.user.email != 'aminhosseini822003@gmail.com':
        return HttpResponseForbidden("شما مجاز به انجام این عمل نیستید.")

    # استفاده از get_object_or_404 برای یافتن تور با PK
    item = get_object_or_404(tourism, id=pk)

    tourism_detile = {
        'title': item.title_tourism,
        "firstdistination_tourism": item.firstdistination_tourism,
        "capacity_tourism": item.capacity_tourism,
        "image_tourism": item.image_tourism,
        "startdate_tourism": item.startdate_tourism,
        "price_tourism": item.price_tourism,
        "ticket_typetourism": item.ticket_typetourism
    }

    # for key, value in tourism_detile.items():
    #     print(f"{key}: {value}")

    # حذف تور
    item.delete()

    delete_tourism_massages("aminhosseini822003@gmail.com", tourism_detile)

    # اگر فیلد تصویر وجود دارد
    if item.image_tourism:
        image_path = os.path.join(settings.MEDIA_ROOT, str(item.image_tourism))
        # بررسی اینکه آیا تور دیگری از این تصویر استفاده می‌کند
        other_tours_using_image = tourism.objects.filter(image_tourism=item.image_tourism).exclude(id=item.id)
        if not other_tours_using_image.exists() and os.path.exists(image_path):
            # اگر هیچ تور دیگری از این تصویر استفاده نمی‌کند و فایل وجود دارد، حذفش می‌کنیم
            os.remove(image_path)

    messages.success(request, "تور با موفقیت حذف شد.")
    return redirect('tourism:tourismpage')


# def edittourism(request, pk):
#     # بررسی اینکه آیا کاربر مجاز است
#     if request.user.email != 'bita4akhgar@gmail.com':
#         return HttpResponseForbidden("شما مجاز به انجام این عمل نیستید.")
#
#     try:
#         tour_id = get_object_or_404(tourism, id=pk)
#     except tourism.DoesNotExist:
#         messages.error(request, "تور مورد نظر پیدا نشد.")
#         return redirect('tourism:tourismpage')
#
#     form = tourismform(instance=tour_id)
#
#     if request.method == "POST":
#         form = tourismform(request.POST, instance=tour_id)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "تور با موفقیت به‌روزرسانی شد.")
#             return redirect('tourism:tourismpage')
#
#     return render(request, 'tourism/addtourism_page.html', {'form': form})


# ------------------------------------این کد درست بوده edittourism👇---------------------------------------

# @login_required
# def edittourism(request, pk):
#     # بررسی اینکه آیا کاربر مجاز است
#     if request.user.email != 'bita4akhgar@gmail.com':
#         return HttpResponseForbidden("شما مجاز به انجام این عمل نیستید.")
#
#     # دریافت شیء تور
#     tour_id = get_object_or_404(tourism, id=pk)
#
#     # بررسی نوع درخواست
#     if request.method == "POST":
#         form = tourismform(request.POST, instance=tour_id)  # بارگذاری اطلاعات فرم با instance
#         if form.is_valid():
#             form.save()  # ذخیره تغییرات
#             messages.success(request, "تور با موفقیت به‌روزرسانی شد.")
#             return redirect('tourism:tourismpage')  # انتقال به صفحه مربوطه
#     else:
#         form = tourismform(instance=tour_id)  # بارگذاری فرم با اطلاعات قبلی برای GET
#
#     # نمایش فرم
#     context = {
#         'form': form,
#         'tour_id': tour_id,  # ارسال شیء تور برای نمایش در template
#     }
#     return render(request, 'tourism/addtourism_page.html', context)
# ------------------------------------این کد درست بودهedittourism 👆---------------------------------------


@login_required
def edittourism(request, pk):
    if request.user.email != 'aminhosseini822003@gmail.com':
        return HttpResponseForbidden("شما مجاز به انجام این عمل نیستند.")

    tour = get_object_or_404(tourism, id=pk)
    # print(f"ID before edit: {tour.id}".encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
    tourism_detile = {
        'title': tour.title_tourism,
        "firstdistination_tourism": tour.firstdistination_tourism,
        "capacity_tourism": tour.capacity_tourism,
        "image_tourism": tour.image_tourism,
        "startdate_tourism": tour.startdate_tourism,
        "price_tourism": tour.price_tourism,
        "ticket_typetourism": tour.ticket_typetourism
    }

    if request.method == "POST":
        # استفاده از request.FILES برای بارگذاری تصویر جدید
        form = tourismform(request.POST, request.FILES, instance=tour)  # اضافه کردن request.FILES
        if form.is_valid():
            updated_tour = form.save()
            # print(
            #     f"ID after save: {updated_tour.id}".encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
            messages.success(request, "تور با موفقیت به‌روزرسانی شد.")

            tourism_detile2 = {
                'title': updated_tour.title_tourism,
                "firstdistination_tourism": updated_tour.firstdistination_tourism,
                "capacity_tourism": updated_tour.capacity_tourism,
                "image_tourism": updated_tour.image_tourism,
                "startdate_tourism": updated_tour.startdate_tourism,
                "price_tourism": updated_tour.price_tourism,
                "ticket_typetourism": updated_tour.ticket_typetourism
            }

            edit_tourism_massages("aminhosseini822003@gmail.com", tourism_detile, tourism_detile2)

            edit_tourism_massages("aminhosseini822003@gmail.com", tour, updated_tour)
            return redirect('tourism:tourismpage')
    else:
        form = tourismform(instance=tour)

    context = {
        'form': form,
        'tour_id': tour,
    }
    return render(request, 'tourism/addtourism_page.html', context)


# @login_required
# def edittourism(request, pk):
#     if request.user.email != 'aminhosseini822003@gmail.com':
#         return HttpResponseForbidden("شما مجاز به انجام این عمل نیستید.")
#
#     tour = get_object_or_404(tourism, id=pk)
#     # استفاده از encode برای مدیریت کاراکترهای فارسی
#     print(f"ID before edit: {tour.id}".encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
#
#     if request.method == "POST":
#         form = tourismform(request.POST, instance=tour)
#         if form.is_valid():
#             updated_tour = form.save()
#             print(
#                 f"ID after save: {updated_tour.id}".encode('utf-8', errors='replace').decode('utf-8', errors='replace'))
#             messages.success(request, "تور با موفقیت به‌روزرسانی شد.")
#             return redirect('tourism:tourismpage')
#     else:
#         form = tourismform(instance=tour)
#
#     context = {
#         'form': form,
#         'tour_id': tour,
#     }
#     return render(request, 'tourism/addtourism_page.html', context)


# ---------------------این کد درست بوده  و با کد قبلی هیچ تفاوتی تداردedittourism👇---------------------------

# @login_required
# def edittourism(request, pk):
#     # بررسی اینکه آیا کاربر مجاز است
#     if request.user.email != 'bita4akhgar@gmail.com':
#         return HttpResponseForbidden("شما مجاز به انجام این عمل نیستید.")
#
#     # دریافت شیء تور
#     tour_id = get_object_or_404(tourism, id=pk)
#
#     # # نمایش مقادیر فعلی به کاربر
#     # if request.method == "GET":
#     #     context = {
#     #         'tour': tour,  # ارسال شیء تور برای نمایش در template
#     #     }
#     #     return render(request, 'tourism/addtourism_page.html', context)  # صفحه‌ای برای نمایش اطلاعات فعلی
#
#     # بررسی نوع درخواست POST برای ویرایش
#     if request.method == "POST":
#         form = tourismform(request.POST, instance=tour_id)  # بارگذاری اطلاعات فرم با instance
#
#         if form.is_valid():
#             # ذخیره یک گردشگری جدید با داده‌های ویرایش شده
#             form.save()
#             # حذف گردشگری قبلی
#             tour_id.delete()
#             messages.success(request, "تور با موفقیت به‌روزرسانی شد.")
#             return redirect('tourism:tourismpage')  # انتقال به صفحه مربوطه
#
#     else:
#         form = tourismform(instance=tour_id)  # بارگذاری فرم با اطلاعات قبلی برای GET
#
#     # اگر فرم معتبر نیست، دوباره فرم را با اطلاعات قبلی بارگذاری می‌کنیم
#     context = {
#         'form': form,
#         'tour_id': tour_id,
#     }
#     return render(request, 'tourism/addtourism_page.html', context)

# -------------------------------این کد درست بوده  و با کد قبلی هیچ تفاوتی تداردedittourism👆----------------------


# @login_required
# def edittourism(request, pk):
#     # بررسی اینکه آیا کاربر مجاز است
#     if request.user.email != 'bita4akhgar@gmail.com':
#         return HttpResponseForbidden("شما مجاز به انجام این عمل نیستید.")
#
#     # دریافت شیء تور
#     tour = get_object_or_404(tourism, id=pk)
#
#     # نمایش مقادیر فعلی به کاربر
#     if request.method == "GET":
#         form = tourismform(instance=tour)  # بارگذاری فرم با اطلاعات فعلی برای نمایش
#         context = {
#             'form': form,
#             'tour': tour,  # ارسال شیء تور برای نمایش در template
#         }
#         return render(request, 'tourism/addtourism_page.html', context)
#
#     # بررسی نوع درخواست POST برای ویرایش
#     if request.method == "POST":
#         form = tourismform(request.POST)  # بارگذاری داده‌های جدید از فرم
#         if form.is_valid():
#             # ذخیره یک گردشگری جدید با داده‌های ویرایش شده
#             new_tour = form.save(commit=False)
#             new_tour.save()  # ذخیره شیء جدید
#
#             # حذف گردشگری قبلی
#             tour.delete()
#
#             messages.success(request, "تور با موفقیت به‌روزرسانی شد.")
#             return redirect('tourism:tourismpage')  # انتقال به صفحه مربوطه
#
#     # اگر فرم معتبر نیست، دوباره فرم را با اطلاعات قبلی بارگذاری می‌کنیم
#     form = tourismform(instance=tour)  # بارگذاری فرم با اطلاعات قبلی
#     context = {
#         'form': form,
#         'tour': tour,
#     }
#     return render(request, 'tourism/addtourism_page.html', context)


def tourism_detail(request, tourism_id):
    # دریافت تور با id مشخص شده یا 404 در صورتی که تور پیدا نشود
    tourisms = get_object_or_404(tourism, id=tourism_id)
    return render(request, 'tourism/tourism_detail.html', {'tour': tourisms})


def main_page(request):
    tourisms = tourism.objects.all()
    context = {
        'tourisms': tourisms
    }

    return render(request, 'tour/main_page.html', context)


def buy_tourism(request, tourism_id):
    # ابتدا بررسی می‌کنیم که کاربر احراز هویت شده است
    if not request.user.is_authenticated:
        messages.error(request, "لطفاً ابتدا وارد حساب کاربری خود شوید.")
        return redirect('accounts:login')  # یا صفحه‌ای که می‌خواهید کاربر را به آن هدایت کنید

    # حالا می‌خواهیم تور منتخب را پیدا کنیم
    try:
        tour_to_buy = tourism.objects.get(id=tourism_id)  # اطمینان از نام مدل
    except tourism.DoesNotExist:
        messages.error(request, "تور مورد نظر یافت نشد.")
        # TODO: باید یک صفحه html فرستاده بشه نه صفحه اصلی
        # TODO: که بگه تور مورد نظر پیدا نشد و دکمه ای باشه برای فرستادن دوباره به صفحه گردشگری ها
        return render(request, 'tourism/tourism_unavailable.html')
        # return redirect('tourism:profile_view')  # یا به هر صفحه دلخواه


    # بررسی می‌کنیم که آیا ظرفیت بیشتر از صفر است
    if tour_to_buy.capacity_tourism <= 0:  # به‌روزرسانی نام فیلد ظرفیت
        messages.error(request, "متأسفانه این تور پر شده است.")
        # TODO: باید بفرستی به صقحه ای که توش بگه تور مورد نظر پیدا نشد.
        # TODO: که بعدش توی اون صفحه دکمه ای باشه که برگردونه اون رو به صفحه همه گردشگری ها
        return render(request,"tourism/tourism_full.html")
        # return redirect('tourism:profile_view')

    # خرید ثبت می‌شود
    Purchase.objects.create(user=request.user, tour=tour_to_buy)

    # کاهش ظرفیت تور
    # TODO: دیگه نباید ایتجا چیزی حذف بشه باید کامنت بشه!
    # TODO: باید حذف باشه برای مرحله اخر در cart
    # tour_to_buy.capacity_tourism -= 1  # به‌روزرسانی نام فیلد ظرفیت
    tour_to_buy.save()  # ذخیره تغییرات ظرفیت در پایگاه داده

    # ارسال پیام تأیید به کاربر
    messages.success(request, f"{tour_to_buy.title_tourism} به درستی خریداری شد.")
    # TODO: باید اینجا فقط به این قسمت فرستاده نشه
    # TODO:  و باید فرستاده بشه به cart
    return redirect("cart:add_to_cart", item_type="tourism", item_id=tourism_id)
    # return redirect('tourism:profile_view')  # به صفحه‌ای که می‌خواهید کاربر را به آن هدایت کنید


@login_required(login_url='accounts/signup/')
def profile_view(request):
    user = request.user
    # دریافت لیست تورهای کاربر از پروفایل
    profile, created = Profile.objects.get_or_create(user=user)
    tours = profile.tours.all()
    purchases = Purchase.objects.filter(user=user)  # خریدهای کاربر
    available_tours = tourism.objects.all()  # لیست تورهای موجود

    return render(request, 'tourism/profile_view.html', {
        'user': user,
        'purchases': purchases,
        'available_tours': available_tours,  # ارسال لیست تورهای موجود به قالب
        'tours': tours  # ارسال لیست تورهای کاربر به قالب
    })
