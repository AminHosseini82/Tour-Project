from .forms import tour, tourform
from django.shortcuts import render, redirect, get_object_or_404
# from .forms import SearchForm
from .forms import TourSearchForm
from .models import tour, Purchase, Profile  # فراموش نکنید مدل‌های تور و خرید را وارد کنید
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from email_sending.tour.delete_tour_email import delete_tour_massages
from django.http import HttpResponseForbidden
from django.utils.timezone import now
from django.contrib import messages
from email_sending.tour.create_tour_email import create_tour_massages
from email_sending.tour.edit_tour_email import edit_tour_massages

list = []
form = tourform()


# @login_required(login_url='/accounts/login')
# def tour_create(request):
#     user = request.user
#     list = []
#
#     if request.method == 'POST':
#         form = tourform(request.POST, request.FILES)  # necessary if user wants to upload a picture
#         if form.is_valid():
#             instance = form.save(commit=False)  # lets us make some changes on the form before saving it on database
#             instance.clas = user  # Associate the tour with the logged-in user
#             # instance.image = request.FILES.get('image', False)  # Get the uploaded image
#             instance.image = form.cleaned_data['image']  # Ensure the image is correctly assigned from the form
#             # Check if the title already exists in the list
#             if instance.title in list:
#                 tours = tour.objects.filter(title=instance.title)
#                 tours.delete()  # Delete existing tours with the same title
#             instance.save()  # Save the new tour
#             return redirect('tour:homepage')  # Redirect to the tour list or add page
#
#     else:
#         form = tourform()  # Create a new form instance if not a POST request
#
#     # Get the tours created by the logged-in user
#     query = tour.objects.filter(clas=user)
#
#     for tourww in query:
#         list.append(tourww.title)
#
#     return render(request, 'tour/addpage.html', {'form': form, 'tours_list': query})
#
# این کد قبلی درست هست
# @login_required(login_url='/accounts/login')
# def tour_create(request):
#     user = request.user
#     list = []
#
#     if request.method == 'POST':
#         form = tourform(request.POST, request.FILES)  # necessary if user wants to upload a picture
#         if form.is_valid():
#             instance = form.save(commit=False)  # lets us make some changes on the form before saving it on database
#             instance.clas = user  # Associate the tour with the logged-in user
#             instance.image = form.cleaned_data['image']  # Ensure the image is correctly assigned from the form
#             # Check if the title already exists in the list
#             if instance.title in list:
#                 tours = tour.objects.filter(title=instance.title)
#                 tours.delete()  # Delete existing tours with the same title
#             instance.save()  # Save the new tour
#             return redirect('tour:homepage')  # Redirect to the tour list or add page
#
#     else:
#         form = tourform()  # Create a new form instance if not a POST request
#
#     # Get the tours created by the logged-in user
#     query = tour.objects.filter(clas=user)
#
#     for tourww in query:
#         list.append(tourww.title)
#
#     return render(request, 'tour/addpage.html', {'form': form, 'tours_list': query})
# --------------------------------------


def user_is_authorized(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.email == 'aminhosseini822003@gmail.com':
                print("User is authorized")
                return view_func(request, *args, **kwargs)
        print("User is not authorized")
        return HttpResponseForbidden("شما مجاز به انجام این عملیات نیستید!")

    return wrapper



# --------------------------------------------------------------------------


@login_required
@user_is_authorized
def tour_create(request):
    user = request.user
    tour_titles = set()

    if request.method == 'POST':
        form = tourform(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.clas = user
            instance.image = form.cleaned_data['image']
            if instance.title in tour_titles:
                tours = tour.objects.filter(title=instance.title)
                tours.delete()
            instance.save()

            # اصلاح خطا: استفاده از کلاس مدل tour برای گرفتن نمونه
            selected_email = request.user.email
            selected_tour = tour.objects.get(id=instance.id)
            # ذخیره تمام فیلدهای تور در یک دیکشنری
            tour_details = {
                'title': selected_tour.title,
                'idtour': selected_tour.idtour,
                'firstdistination': selected_tour.firstdistination,
                'lastDestination': selected_tour.lastDestination,
                'startdate': selected_tour.startdate,
                'finishdate': selected_tour.finishdate,
                'ticket_type': selected_tour.ticket_type
            }

            # # چاپ دیکشنری tour_details برای دیباگ (بدون encode/decode، فقط با str)
            # for key, value in tour_details.items():
            #     print(f"{key}: {value}")
            create_tour_massages(selected_email, tour_details)
            return redirect('tour:homepage')

    else:
        form = tourform()

    user_tours = tour.objects.filter(clas=user)

    is_authorized = (user.email == 'aminhosseini822003@gmail.com')
    print("is_authorized:", is_authorized)  # پیام دیباگینگ

    return render(request, 'tour/addpage.html', {
        'form': form,
        'tours_list': user_tours,
        'is_authorized': is_authorized
    })


# --------------------------------------------------------------------------
# @login_required
# @user_is_authorized
# def edittour(request, pk):
#     try:
#         tour_id = tour.objects.get(id=pk)
#     except tour.DoesNotExist:
#         messages.error(request, "تور مورد نظر پیدا نشد.")
#         return redirect('tour:homepage')
#
#     form = tourform(instance=tour_id)
#
#     if request.method == "POST":
#         form = tourform(request.POST, instance=tour_id)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "تور با موفقیت به‌روزرسانی شد.")
#             return redirect('tour:homepage')
#
#     is_authorized = (request.user.email == 'bita4akhgar@gmail.com')  # بررسی مجوز
#     context = {'form': form, 'is_authorized': is_authorized}
#
#     return render(request, 'tour/addpage.html', context)
# --------------------------------------------------------------------------


# @login_required
# @user_is_authorized
# def edittour(request, pk):
#     # تلاش برای دریافت شیء تور از پایگاه داده
#     tour_item = get_object_or_404(tour, id=pk)
#
#     if request.method == "POST":
#         form = tourform(request.POST, request.FILES, instance=tour_item)  # اضافه شدن request.FILES برای بارگذاری فایل‌ها
#         if form.is_valid():
#             form.save()
#             messages.success(request, "تور با موفقیت به‌روزرسانی شد.")
#             return redirect('tour:homepage')  # تغییر به URL مربوط به صفحه اصلی تور
#     else:
#         form = tourform(instance=tour_item)  # فرم با اطلاعات قبلی پر می‌شود
#
#     is_authorized = (request.user.email == 'bita4akhgar@gmail.com')  # بررسی مجوز
#     context = {'form': form, 'is_authorized': is_authorized, 'tour_item': tour_item}  # می‌توانید متغیر tour_item را به context اضافه کنید
#
#     return render(request, 'tour/addpage.html', context)
# --------------------------------------------------------------------------


# ------------------------------------اخرین تغییرات درست edittour👇--------------------------------------
# @login_required
# @user_is_authorized
# def edittour(request, pk):
#     # دریافت شیء تور از پایگاه داده
#     tour_item = get_object_or_404(tour, id=pk)
#
#     if request.method == "POST":
#         form = tourform(request.POST, request.FILES, instance=tour_item)  # بارگذاری فایل‌ها نیز
#         if form.is_valid():
#             form.save()  # ذخیره تغییرات
#             messages.success(request, "تور با موفقیت به‌روزرسانی شد.")
#             return redirect('tour:homepage')  # تغییر به صفحه اصلی تور
#     else:
#         # نمایش فرم با اطلاعات قبلی
#         form = tourform(instance=tour_item)
#
#     cities = ["کرمان", "شیراز", "اصفهان", "تهران", "گیلان", "یزد", "همدان", "مشهد", "هرمزگان"]
#     is_authorized = (request.user.email == 'bita4akhgar@gmail.com')  # بررسی مجوز کاربر
#     context = {
#         'form': form,
#         'is_authorized': is_authorized,
#         'tour_item': tour_item,
#         "cities": cities
#     }
#
#     return render(request, 'tour/addpage.html', context)
# ----------------------------------------اخرین تغییرات درست edittour👆---------------------------------------


@login_required
@user_is_authorized
def edittour(request, pk):
    # دریافت شیء تور از پایگاه داده
    tour_item = get_object_or_404(tour, id=pk)
    today = now().date()  # دریافت تاریخ امروز


    # 'title': selected_tour.title,
    # 'idtour': selected_tour.idtour,
    # 'firstdistination': selected_tour.firstdistination,
    # 'lastDestination': selected_tour.lastDestination,
    # 'startdate': selected_tour.startdate,
    # 'finishdate': selected_tour.finishdate,
    # 'ticket_type': selected_tour.ticket_type

    # دیکشنری برای ذخیره مقادیر قدیمی
    old_tour_details = {
        'title': tour_item.title,
        'idtour': tour_item.idtour,
        'firstdistination': tour_item.firstdistination,
        'lastDestination': tour_item.lastDestination,
        'startdate': tour_item.startdate,
        'finishdate': tour_item.finishdate,
        'ticket_type': tour_item.ticket_type
    }

    if request.method == "POST":
        form = tourform(request.POST, request.FILES, instance=tour_item)  # بارگذاری فایل‌ها نیز
        if form.is_valid():
            startdate = form.cleaned_data["startdate"]
            finishdate = form.cleaned_data["finishdate"]

            # **بررسی اینکه تاریخ حرکت نباید از امروز عقب‌تر باشد**
            if startdate < today:
                messages.error(request, "تاریخ حرکت نمی‌تواند قبل از امروز باشد!")
                return render(request, "tour/addpage.html", {
                    "form": form,
                    "tour_item": tour_item,
                    "today": today,
                })

            # **بررسی اینکه تاریخ برگشت نباید قبل از تاریخ حرکت باشد**
            if finishdate < startdate:
                messages.error(request, "تاریخ برگشت نمی‌تواند قبل از تاریخ حرکت باشد!")
                return render(request, "tour/addpage.html", {
                    "form": form,
                    "tour_item": tour_item,
                    "today": today,
                })

            form.save()  # ذخیره تغییرات

            # دیکشنری برای ذخیره مقادیر جدید
            new_tour_details = {
                'title': form.cleaned_data['title'],
                'idtour': form.cleaned_data['idtour'],
                'firstdistination': form.cleaned_data['firstdistination'],
                'lastDestination': form.cleaned_data['lastDestination'],
                'startdate': form.cleaned_data['startdate'],
                'finishdate': form.cleaned_data['finishdate'],
                'ticket_type': form.cleaned_data['ticket_type']
            }

            # email_sending = request.user.email

            # # می‌توانید حالا old_tour_details و new_tour_details را برای هر کاری که نیاز دارید استفاده کنید
            # print("Old Tour Details:", old_tour_details)
            # print("New Tour Details:", new_tour_details)

            messages.success(request, "تور با موفقیت به‌روزرسانی شد.")

            edit_tour_massages("aminhosseini822003@gmail.com",old_tour_details, new_tour_details)

            return redirect('tour:homepage')  # تغییر به صفحه اصلی تور
    else:
        # نمایش فرم با اطلاعات قبلی
        form = tourform(instance=tour_item)

    cities = ["کرمان", "شیراز", "اصفهان", "تهران", "گیلان", "یزد", "همدان", "مشهد", "هرمزگان"]
    is_authorized = (request.user.email == 'aminhosseini822003@gmail.com')  # بررسی مجوز کاربر
    context = {
        'form': form,
        'is_authorized': is_authorized,
        'tour_item': tour_item,
        "cities": cities,
        "today": today,  # ارسال تاریخ امروز به قالب
    }

    return render(request, 'tour/addpage.html', context)


# @login_required
# @user_is_authorized
# def edittour(request, pk):
#     tour_item = get_object_or_404(tour, id=pk)
#     if request.method == "POST":
#         form = tourform(request.POST, request.FILES, instance=tour_item)
#         if form.is_valid():
#             updated_tour = form.save(commit=False)
#             if 'image' in request.FILES:
#                 updated_tour.image = request.FILES['image']
#             else:
#                 updated_tour.image = tour_item.image
#             updated_tour.save()
#             messages.success(request, "تور با موفقیت به‌روزرسانی شد.")
#             return redirect('tour:homepage')
#     else:
#         form = tourform(instance=tour_item)
#
#     context = {'form': form, 'tour_item': tour_item}
#     return render(request, 'tour/addpage.html', context)
#
#


# @login_required
# @user_is_authorized
# def edittour(request, pk):
#     # دریافت شیء تور از پایگاه داده
#     tour_item = get_object_or_404(tour, id=pk)
#
#     if request.method == "POST":
#         form = tourform(request.POST, request.FILES, instance=tour_item)  # بارگذاری فایل‌ها نیز
#         if form.is_valid():
#             # اگر تصویر جدیدی آپلود نشده باشد، مقدار قبلی را حفظ کنید
#             if not request.FILES.get('image'):  # نام فیلد تصویر در مدل 'image' است
#                 form.instance.image = tour_item.image
#             form.save()  # ذخیره تغییرات
#             messages.success(request, "تور با موفقیت به‌روزرسانی شد.")
#             return redirect('tour:homepage')  # تغییر به صفحه اصلی تور
#     else:
#         # نمایش فرم با اطلاعات قبلی
#         form = tourform(instance=tour_item)
#
#     is_authorized = (request.user.email == 'bita4akhgar@gmail.com')  # بررسی مجوز کاربر
#     context = {
#         'form': form,
#         'is_authorized': is_authorized,
#         'tour_item': tour_item
#     }
#
#     return render(request, 'tour/addpage.html', context)


# @login_required
# @user_is_authorized
# def edittour(request, pk):
#     # دریافت شیء تور از پایگاه داده
#     tour_item = get_object_or_404(tour, id=pk)
#
#     if request.method == "POST":
#         form = tourform(request.POST, request.FILES, instance=tour_item)  # بارگذاری فایل‌ها نیز
#         if form.is_valid():
#             # اگر تصویر جدیدی آپلود نشده باشد، مقدار قبلی را حفظ کنید
#             if not request.FILES.get('image'):  # فرض بر این است که نام فیلد تصویر 'image_tour' است
#                 form.instance.image = tour_item.image
#             form.save()  # ذخیره تغییرات
#             messages.success(request, "تور با موفقیت به‌روزرسانی شد.")
#             return redirect('tour:homepage')  # تغییر به صفحه اصلی تور
#     else:
#         # نمایش فرم با اطلاعات قبلی
#         form = tourform(instance=tour_item)
#
#     is_authorized = (request.user.email == 'bita4akhgar@gmail.com')  # بررسی مجوز کاربر
#     context = {
#         'form': form,
#         'is_authorized': is_authorized,
#         'tour_item': tour_item
#     }
#
#     return render(request, 'tour/addpage.html', context)


# --------------------------------------------------------------------------

def home_view(request):
    tours = tour.objects.all()  # نام مدل باید با حرف بزرگ باشد: Tour
    form = TourSearchForm(request.GET)  # دریافت داده‌های فرم جستجو

    if form.is_valid():
        origin = form.cleaned_data.get('firstdistination')
        destination = form.cleaned_data.get('lastDestination')
        startdate = form.cleaned_data.get('startdate')  # تاریخ رفت
        finishdate = form.cleaned_data.get('finishdate')  # تاریخ برگشت

        # print(f"Origin: {origin}, Destination: {destination}, Startdate: {startdate}, Finishdate: {finishdate}")  # برای بررسی
        # تبدیل تاریخ شمسی به میلادی

        # فیلتر کردن تورها بر اساس مبدا و مقصد
        if origin:
            tours = tours.filter(firstdistination__icontains=origin)
        if destination:
            tours = tours.filter(lastDestination__icontains=destination)
        if startdate:
            tours = tours.filter(startdate__gte=startdate)  # تاریخ شروع باید بزرگتر یا مساوی تاریخ انتخابی باشد
        if finishdate:
            tours = tours.filter(finishdate__lte=finishdate)  # تاریخ برگشت باید کوچکتر یا مساوی تاریخ انتخابی باشد

    return render(request, 'tour/home_page.html', {'tours': tours, 'form': form})


# --------------------------------------------------------------------------

def deletetour(request, pk):
    # بررسی اینکه آیا کاربر وارد شده است و آیا ایمیل او مجاز است
    if not request.user.is_authenticated or request.user.email != 'aminhosseini822003@gmail.com':
        return HttpResponseForbidden("شما مجاز به انجام این عمل نیستید.")

        # استفاده از get_object_or_404 برای یافتن تور با PK
    item = get_object_or_404(tour, id=pk)
    user_email = request.user.email
    # حذف عکس‌ها
    if item.image:
        item.image.delete()  # حذف فایل عکس از سیستم فایل
        # print("dalite phiter")

    selected_tour = tour.objects.get(id=item.id)
    # حذف تور
    item.delete()

    # ذخیره تمام فیلدهای تور در یک دیکشنری
    tour_details = {
        'title': selected_tour.title,
        'idtour': selected_tour.idtour,
        'firstdistination': selected_tour.firstdistination,
        'lastDestination': selected_tour.lastDestination,
        'startdate': selected_tour.startdate,
        'finishdate': selected_tour.finishdate,
        'ticket_type': selected_tour.ticket_type
    }

    delete_tour_massages(user_email, tour_details)

    return redirect('tour:homepage')


# --------------------------------------------------------------------------

# اخرین کد ادیت درست
# def edittour(request, pk):
#     tour_id = tour.objects.get(id=pk)
#     form = tourform(instance=tour_id)
#
#     if request.method == "POST":
#         form = tourform(request.POST, instance=tour_id)
#         if form.is_valid():
#             form.save()
#             return redirect('tour:homepage')
#     context = {'form': form}
#     return render(request, 'tour/addpage.html', context)


# لگر خرتب شد اینو از کمتمنی در بیار

# def edittour(request, pk):
#     tour_id = tour.objects.get(id=pk)
#     form = tourform(instance=tour_id)
#
#     if request.method == "POST":
#         form = tourform(request.POST, instance=tour_id)
#         if form.is_valid():
#             form.save()
#             return redirect('tour:homepage')
#     context = {'form': form}
#     return render(request, 'tour/addpage.html', context)

# --------------------------------------------------------------------------

def edandde(request):
    if 'edit' in request.POST:
        user = request.user
        students_list = tour.objects.all().values_list('name', flat=True)
        name = request.POST.get('tt')
        if name in list:
            tours = tour.objects.filter(title=name, cls=user)
            form = tourform(instance=tours)
            return redirect('tour:add')
        return redirect('tour:add')
    if 'delete' in request.POST:
        user = request.user
        if request.method == 'POST':
            name = request.POST.get('tt')
            tours = tour.objects.filter(title=name, clas=user)
            if tours.exists():
                tours.delete()
            return redirect('tour:add')
        return redirect('tour:add')
    return redirect('tour:add')


# --------------------------------------------------------------------------

def tour_detail(request, tour_id):
    # دریافت تور با id مشخص شده یا 404 در صورتی که تور پیدا نشود
    tours = get_object_or_404(tour, id=tour_id)
    return render(request, 'tour/tour_detail.html', {'tour': tours})


# --------------------------------------------------------------------------

def main_page(request):
    tours = tour.objects.all()  # تمام تورها را از پایگاه‌داده بگیرید
    context = {
        'tours': tours  # ارسال تورها به قالب
    }
    return render(request, 'tour/main_page.html', context)  # از context استفاده کنید


# --------------------------------------------------------------------------

def buy_tour(request, tour_id):
    # ابتدا بررسی می‌کنیم که کاربر احراز هویت شده است
    if not request.user.is_authenticated:
        messages.error(request, "لطفاً ابتدا وارد حساب کاربری خود شوید.")
        return redirect('accounts:login')  # یا صفحه‌ای که می‌خواهید کاربر را به آن هدایت کنید

    # حالا می‌خواهیم تور منتخب را پیدا کنیم
    try:
        tour_to_buy = tour.objects.get(id=tour_id)
    except tour.DoesNotExist:
        messages.error(request, "تور مورد نظر یافت نشد.")
        return redirect('tour:profile_view')  # یا به هر صفحه دلخواه

    # بررسی می‌کنیم که آیا ظرفیت بیشتر از صفر است
    if tour_to_buy.capacity <= 0:
        messages.error(request, "متأسفانه این تور پر شده است.")
        return redirect('tour:profile_view')

    # خرید ثبت می‌شود
    Purchase.objects.create(user=request.user, tour=tour_to_buy)

    # کاهش ظرفیت تور
    # TODO: نباید یک دونه ازش کم بشه باید بره توی صفحه تعداد بعدش تعداد رو وارد کرد بفرستیم تعداد رو این ور
    # TODO: بعدش تعداد رو اینجا کم بکنیم.
    tour_to_buy.capacity -= 1
    tour_to_buy.save()  # ذخیره تغییرات ظرفیت در پایگاه داده

    # ارسال پیام تأیید به کاربر
    messages.success(request, f"{tour_to_buy.title} به درستی خریداری شد.")

    return redirect('tour:profile_view')  # به صفحه‌ای که می‌خواهید کاربر را به آن هدایت کنید


# --------------------------------------------------------------------------

# الان اینو گذاشتم دقیقا زیریش بهتره

# --------------------------------------------------------------------------

@login_required(login_url='accounts/signup/')
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    tours = profile.tours.all()
    purchases = Purchase.objects.filter(user=user)  # خریدهای کاربر
    available_tours = tour.objects.all()  # لیست تورهای موجود

    return render(request, 'tour/profile_view.html', {
        'user': user,
        'purchases': purchases,
        'available_tours': available_tours,  # ارسال لیست تورهای موجود به قالب
        'tours': tours  # ارسال لیست تورهای کاربر به قالب
    })
