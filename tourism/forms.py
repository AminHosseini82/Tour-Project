from django import forms
from django.core.exceptions import ValidationError
from .models import tourism
from datetime import date


class tourismform(forms.ModelForm):
    class Meta:
        model = tourism
        fields = ['title_tourism', 'firstdistination_tourism', 'capacity_tourism', 'image_tourism', 'startdate_tourism',
                  'price_tourism', 'ticket_typetourism']
        widgets = {
            'startdate_tourism': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_price_tourism(self):
        price = self.cleaned_data['price_tourism']
        if price < 0:
            raise ValidationError("هزینه نمی‌تواند عدد منفی باشد.")
        return price

    def clean_capacity_tourism(self):
        capacity = self.cleaned_data['capacity_tourism']
        if capacity < 0:
            raise ValidationError("ظرفیت نمی‌تواند عدد منفی باشد.")
        return capacity

    def clean_startdate_tourism(self):
        start_date = self.cleaned_data['startdate_tourism']
        today = date.today()  # تاریخ امروز میلادی

        if start_date < today:
            # فرمت تاریخ برای نمایش بهتر
            today_formatted = today.strftime('%Y-%m-%d')
            selected_date_formatted = start_date.strftime('%Y-%m-%d')
            raise ValidationError(
                f"تاریخ گردشگری نمی‌تواند در گذشته باشد. امروز {today_formatted} است، ولی شما تاریخ {selected_date_formatted} را انتخاب کرده‌اید. لطفاً تاریخ امروز یا آینده را وارد کنید.")
        return start_date


# class SearchForm(forms.Form):
#     query = forms.CharField(label='Search', max_length=100)


class TourismSearchForm(forms.Form):
    query = forms.CharField(required=False, max_length=255, label='جستجوی گردشگری (عنوان یا مبدا)')

# class TourismSearchForm(forms.Form):
#     firstdistination_tourism = forms.CharField(required=False, max_length=255, label='مبدا')
#     title_tourism = forms.CharField(required=False, max_length=255, label='عنوان گردشگری')
# lastDistination = forms.CharField(required=False, max_length=255, label='مقصد')
#
# startdate = forms.DateField(required=False, label='تاریخ رفت', widget=forms.SelectDateWidget())
# finishdate = forms.DateField(required=False, label='تاریخ برگشت', widget=forms.SelectDateWidget())
















# --------------------------این کد از همه درست تر ویرایش 21 بعد از درست کردن search 👇--------------------------------
# from django import forms
# from django.core.exceptions import ValidationError
# from .models import tourism
# from datetime import date
#
#
# class tourismform(forms.ModelForm):
#     class Meta:
#         model = tourism
#         fields = ['title_tourism', 'firstdistination_tourism', 'capacity_tourism', 'image_tourism', 'startdate_tourism',
#                   'price_tourism', 'ticket_typetourism']
#         widgets = {
#             'startdate_tourism': forms.DateInput(attrs={'type': 'date'}),
#         }
#
#     def clean_price_tourism(self):
#         price = self.cleaned_data['price_tourism']
#         if price < 0:
#             raise ValidationError("هزینه نمی‌تواند عدد منفی باشد.")
#         return price
#
#     def clean_capacity_tourism(self):
#         capacity = self.cleaned_data['capacity_tourism']
#         if capacity < 0:
#             raise ValidationError("ظرفیت نمی‌تواند عدد منفی باشد.")
#         return capacity
#
#     def clean_startdate_tourism(self):
#         start_date = self.cleaned_data['startdate_tourism']
#         today = date.today()  # تاریخ امروز میلادی
#
#         if start_date < today:
#             # فرمت تاریخ برای نمایش بهتر
#             today_formatted = today.strftime('%Y-%m-%d')
#             selected_date_formatted = start_date.strftime('%Y-%m-%d')
#             raise ValidationError(
#                 f"تاریخ گردشگری نمی‌تواند در گذشته باشد. امروز {today_formatted} است، ولی شما تاریخ {selected_date_formatted} را انتخاب کرده‌اید. لطفاً تاریخ امروز یا آینده را وارد کنید.")
#         return start_date
#
#
# # class SearchForm(forms.Form):
# #     query = forms.CharField(label='Search', max_length=100)
#
#
# class TourismSearchForm(forms.Form):
#     firstdistination_tourism = forms.CharField(required=False, max_length=255, label='مبدا')
#     title_tourism = forms.CharField(required=False, max_length=255, label='عنوان گردشگری')
#     # lastDistination = forms.CharField(required=False, max_length=255, label='مقصد')
#     #
#     # startdate = forms.DateField(required=False, label='تاریخ رفت', widget=forms.SelectDateWidget())
#     # finishdate = forms.DateField(required=False, label='تاریخ برگشت', widget=forms.SelectDateWidget())

# --------------------------این کد از همه درست تر ویرایش 21 بعد از درست کردن search 👆--------------------------------


































# --------------------------این کد از همه درست تر ویرایش 20 قبل از درست کردن search 👇--------------------------------

#
# from django import forms
# from django.core.exceptions import ValidationError
# from .models import tourism
# from datetime import date
#
#
# class tourismform(forms.ModelForm):
#     class Meta:
#         model = tourism
#         fields = ['title_tourism', 'firstdistination_tourism', 'capacity_tourism', 'image_tourism', 'startdate_tourism',
#                   'price_tourism', 'ticket_typetourism']
#         widgets = {
#             'startdate_tourism': forms.DateInput(attrs={'type': 'date'}),
#         }
#
#     def clean_price_tourism(self):
#         price = self.cleaned_data['price_tourism']
#         if price < 0:
#             raise ValidationError("هزینه نمی‌تواند عدد منفی باشد.")
#         return price
#
#     def clean_capacity_tourism(self):
#         capacity = self.cleaned_data['capacity_tourism']
#         if capacity < 0:
#             raise ValidationError("ظرفیت نمی‌تواند عدد منفی باشد.")
#         return capacity
#
#     def clean_startdate_tourism(self):
#         start_date = self.cleaned_data['startdate_tourism']
#         today = date.today()  # تاریخ امروز میلادی
#
#         if start_date < today:
#             # فرمت تاریخ برای نمایش بهتر
#             today_formatted = today.strftime('%Y-%m-%d')
#             selected_date_formatted = start_date.strftime('%Y-%m-%d')
#             raise ValidationError(
#                 f"تاریخ گردشگری نمی‌تواند در گذشته باشد. امروز {today_formatted} است، ولی شما تاریخ {selected_date_formatted} را انتخاب کرده‌اید. لطفاً تاریخ امروز یا آینده را وارد کنید.")
#         return start_date
#
#
# # class SearchForm(forms.Form):
# #     query = forms.CharField(label='Search', max_length=100)
#
#
# class TourismSearchForm(forms.Form):
#     firstdistination_tourism = forms.CharField(required=False, max_length=255, label='مبدا')
#     # lastDistination = forms.CharField(required=False, max_length=255, label='مقصد')
#     #
#     # startdate = forms.DateField(required=False, label='تاریخ رفت', widget=forms.SelectDateWidget())
#     # finishdate = forms.DateField(required=False, label='تاریخ برگشت', widget=forms.SelectDateWidget())

# --------------------------این کد از همه درست تر ویرایش 20 قبل از درست کردن search 👆--------------------------------






















# # --------------------------این کد از همه درست تر و از همه چدیدتره 👇-----------------------------------
# from django import forms
# from django.core.exceptions import ValidationError
# from .models import tourism
# from datetime import date
#
#
# class tourismform(forms.ModelForm):
#     class Meta:
#         model = tourism
#         fields = ['title_tourism', 'firstdistination_tourism', 'capacity_tourism', 'image_tourism', 'startdate_tourism',
#                   'price_tourism', 'ticket_typetourism']
#         widgets = {
#             'startdate_tourism': forms.DateInput(attrs={'type': 'date'}),
#         }
#
#     def clean_price_tourism(self):
#         price = self.cleaned_data['price_tourism']
#         if price < 0:
#             raise ValidationError("هزینه نمی‌تواند عدد منفی باشد.")
#         return price
#
#     def clean_capacity_tourism(self):
#         capacity = self.cleaned_data['capacity_tourism']
#         if capacity < 0:
#             raise ValidationError("ظرفیت نمی‌تواند عدد منفی باشد.")
#         return capacity
#
#     def clean_startdate_tourism(self):
#         start_date = self.cleaned_data['startdate_tourism']
#         today = date.today()  # تاریخ امروز میلادی
#
#         if start_date < today:
#             raise ValidationError("تاریخ گردشگری نمی‌تواند در گذشته باشد. لطفاً تاریخ امروز یا آینده را وارد کنید.")
#         return start_date
#
#
# # class SearchForm(forms.Form):
# #     query = forms.CharField(label='Search', max_length=100)
#
#
# class TourismSearchForm(forms.Form):
#     firstdistination_tourism = forms.CharField(required=False, max_length=255, label='مبدا')
#     # lastDistination = forms.CharField(required=False, max_length=255, label='مقصد')
#     #
#     # startdate = forms.DateField(required=False, label='تاریخ رفت', widget=forms.SelectDateWidget())
#     # finishdate = forms.DateField(required=False, label='تاریخ برگشت', widget=forms.SelectDateWidget())
# --------------------------این کد از همه درست تر و از همه چدیدتره 👆-----------------------------------


# --------------------------این کد جدید درست هست 👇-----------------------------------
# from django import forms
# from django.core.exceptions import ValidationError
# from .models import tourism
#
#
# class tourismform(forms.ModelForm):
#     class Meta:
#         model = tourism
#         fields = ['title_tourism', 'firstdistination_tourism', 'capacity_tourism', 'image_tourism', 'startdate_tourism',
#                   'price_tourism', 'ticket_typetourism']
#
#     def clean_price_tourism(self):
#         price = self.cleaned_data['price_tourism']
#         if price < 0:
#             raise ValidationError("هزینه نمی‌تواند عدد منفی باشد.")
#         return price
#
#     def clean_capacity_tourism(self):
#         capacity = self.cleaned_data['capacity_tourism']
#         if capacity < 0:
#             raise ValidationError("ظرفیت نمی‌تواند عدد منفی باشد.")
#         return capacity
#
#
# # class SearchForm(forms.Form):
# #     query = forms.CharField(label='Search', max_length=100)
#
#
# class TourismSearchForm(forms.Form):
#     firstdistination_tourism = forms.CharField(required=False, max_length=255, label='مبدا')
#     # lastDistination = forms.CharField(required=False, max_length=255, label='مقصد')
#     #
#     # startdate = forms.DateField(required=False, label='تاریخ رفت', widget=forms.SelectDateWidget())
#     # finishdate = forms.DateField(required=False, label='تاریخ برگشت', widget=forms.SelectDateWidget())

# --------------------------این کد جدید درست هست 👆-----------------------------------


# --------------------------این کد درست بوده 👇-----------------------------------

# from django import forms
# from .models import tourism
#
#
# class tourismform(forms.ModelForm):
#     class Meta:
#         model = tourism
#         fields = ['title_tourism','firstdistination_tourism','capacity_tourism', 'image_tourism', 'startdate_tourism', 'price_tourism', 'ticket_typetourism', ]
#
#
# # class SearchForm(forms.Form):
# #     query = forms.CharField(label='Search', max_length=100)
#
#
# class TourismSearchForm(forms.Form):
#     firstdistination_tourism = forms.CharField(required=False, max_length=255, label='مبدا')
#     # lastDistination = forms.CharField(required=False, max_length=255, label='مقصد')
#     #
#     # startdate = forms.DateField(required=False, label='تاریخ رفت', widget=forms.SelectDateWidget())
#     # finishdate = forms.DateField(required=False, label='تاریخ برگشت', widget=forms.SelectDateWidget())

# --------------------------این کد درست بوده 👆-----------------------------------
