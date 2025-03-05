from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import house
from .forms import houseForm  # فرض کنید فرم مربوط به House با این نام ایجاد شده است

@login_required
def house_list(request):
    houses = house.objects.all()  # دریافت همه اقامتگاه‌ها
    return render(request, 'house/house_list.html', {'houses': houses})  # نام فایل HTML ممکن است تغییر کند

def user_is_authorized(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.email == 'aminhosseini822003@gmail.com':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("شما مجاز به انجام این عملیات نیستید!")

    return wrapper

@login_required
@user_is_authorized
def house_create(request):
    if request.method == 'POST':
        form = houseForm(request.POST, request.FILES)
        if form.is_valid():
            house_instance = form.save(commit=False)
            house_instance.owner = request.user  # ارتباط با کاربر
            house_instance.save()
            messages.success(request, "اقامتگاه با موفقیت اضافه شد.")
            return redirect('house:house_list')  # تغییر مسیر به لیست اقامتگاه‌ها
    else:
        form = houseForm()

    return render(request, 'house/add_house.html', {'form': form})

@login_required
@user_is_authorized
def edit_house(request, pk):
    house_item = get_object_or_404(house, id=pk)  # دریافت شیء اقامتگاه

    if request.method == "POST":
        form = houseForm(request.POST, request.FILES, instance=house_item)
        if form.is_valid():
            form.save()
            messages.success(request, "اقامتگاه با موفقیت به‌روزرسانی شد.")
            return redirect('house:house_list')  # بازگشت به لیست اقامتگاه‌ها
    else:
        form = houseForm(instance=house_item)

    is_authorized = (request.user.email == 'bita4akhgar@gmail.com')
    context = {
        'form': form,
        'is_authorized': is_authorized,
        'house_item': house_item
    }

    return render(request, 'house/add_house.html', context)  # نمایش فرم ویرایش
#
# @login_required
# @user_is_authorized
# def delete_house(request, pk):
#     house_item = get_object_or_404(house, id=pk)
#
#     if request.method == "POST":
#         house_item.delete()
#         messages.success(request, "اقامتگاه با موفقیت حذف شد.")
#         return redirect('house:house_list')  # بازگشت به لیست اقامتگاه‌ها

@login_required
@user_is_authorized  # بررسی کنید که این دکوریتور به درستی کار می‌کند
def delete_house(request, pk):
    house_item = get_object_or_404(house, id=pk)
    if request.method == "POST":
        house_item.delete()
        messages.success(request, "اقامتگاه با موفقیت حذف شد.")
        return redirect('house:house_list')
    else:
        messages.error(request, "فقط می‌توانید از فرمت POST استفاده کنید.")
        return redirect('house:house_list')