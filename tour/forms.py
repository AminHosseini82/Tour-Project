# ------------------------------------اخرین تغییرات درست 👇--------------------------------------
# from django import forms
# from .models import tour
#
#
# class tourform(forms.ModelForm):
#     class Meta:
#         model = tour
#         fields = ['title', 'idtour', 'firstdistination', 'lastDestination', 'capacity', 'image', 'startdate',
#                   'finishdate', 'ticket_type']
#
#
# # class SearchForm(forms.Form):
# #     query = forms.CharField(label='Search', max_length=100)
#
#
# class TourSearchForm(forms.Form):
#     firstdistination = forms.CharField(required=False, max_length=255, label='مبدا')
#     lastDistination = forms.CharField(required=False, max_length=255, label='مقصد')
#
#     startdate = forms.DateField(required=False, label='تاریخ رفت', widget=forms.SelectDateWidget())
#     finishdate = forms.DateField(required=False, label='تاریخ برگشت', widget=forms.SelectDateWidget())
# ----------------------------------------اخرین تغییرات درست 👆---------------------------------------


from django import forms
from .models import tour


class tourform(forms.ModelForm):
    class Meta:
        model = tour
        fields = ['title', 'idtour', 'firstdistination', 'lastDestination', 'capacity', 'image', 'startdate',
                  'finishdate', 'ticket_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اگه در حال ویرایش باشیم (یعنی شیء از قبل وجود داشته باشه)، تصویر اختیاری می‌شه
        if self.instance and self.instance.pk:
            self.fields['image'].required = False
        # اگه در حال ایجاد باشیم، تصویر به‌صورت پیش‌فرض اجباریه (به‌خاطر مدل)


# این بخش‌ها رو دست نزدم
class TourSearchForm(forms.Form):
    firstdistination = forms.CharField(required=False, max_length=255, label='مبدا')
    lastDistination = forms.CharField(required=False, max_length=255, label='مقصد')
    startdate = forms.DateField(required=False, label='تاریخ رفت', widget=forms.SelectDateWidget())
    finishdate = forms.DateField(required=False, label='تاریخ برگشت', widget=forms.SelectDateWidget())