from django import forms
from .models import Profile


class AddTeacherForm(forms.Form):
    first_name = forms.CharField(label="Имя", max_length=50, required=True,
                                 widget=forms.widgets.TextInput(attrs={'class': "form-control"}),
                                 error_messages={'required': "Обязательное поле"})
    last_name = forms.CharField(label="Фамилия", max_length=30, required=True,
                                widget=forms.widgets.TextInput(attrs={'class': "form-control"}),
                                error_messages={'required': "Обязательное поле"})
    birthday = forms.DateField(label="День рождения", input_formats=['%d.%m.%Y'], required=False,
                               widget=forms.widgets.DateInput(format='%d.%m.%Y', attrs={'class': "form-control"}),
                               help_text="Введите дату в формате ДД.ММ.ГГГГ",
                               error_messages={'invalid': "Введите дату в формате ДД.ММ.ГГГГ"})
    manager = forms.ModelChoiceField(label="Менеджер", queryset=Profile.objects.filter(role__code='manager'),
                                     required=False,
                                     widget=forms.widgets.Select(attrs={'class': "form-control"}))
    phone = forms.CharField(label="Телефон", max_length=15, required=False,
                            widget=forms.widgets.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(label="Email", required=False,
                             widget=forms.widgets.EmailInput(attrs={'class': "form-control"}))
    additional_contact = forms.CharField(label="Дополнительный контакт", required=False,
                                         widget=forms.widgets.TextInput(attrs={"class": "form-control"}))
    additional_contact_description = forms.CharField(label="Описание", required=False,
                                                     widget=forms.widgets.TextInput(attrs={"class": "form-control"}))


class AddStudentForm(forms.Form):
    first_name = forms.CharField(label="Имя", max_length=50, required=True,
                                 widget=forms.widgets.TextInput(attrs={'class': "form-control"}),
                                 error_messages={'required': "Обязательное поле"})
    last_name = forms.CharField(label="Фамилия", max_length=30, required=True,
                                widget=forms.widgets.TextInput(attrs={'class': "form-control"}),
                                error_messages={'required': "Обязательное поле"})
    birthday = forms.DateField(label="День рождения", input_formats=['%d.%m.%Y'], required=False,
                               widget=forms.widgets.DateInput(format='%d.%m.%Y', attrs={'class': "form-control"}),
                               help_text="Введите дату в формате ДД.ММ.ГГГГ",
                               error_messages={'invalid': "Введите дату в формате ДД.ММ.ГГГГ"})
    manager = forms.ModelChoiceField(label="Менеджер", queryset=Profile.objects.filter(role__code='manager'),
                                     required=False,
                                     widget=forms.widgets.Select(attrs={'class': "form-control"}))
    phone = forms.CharField(label="Телефон", max_length=15, required=False,
                            widget=forms.widgets.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(label="Email", required=False,
                             widget=forms.widgets.EmailInput(attrs={'class': "form-control"}))
    additional_contact = forms.CharField(label="Дополнительный контакт", required=False,
                                         widget=forms.widgets.TextInput(attrs={"class": "form-control"}))
    additional_contact_description = forms.CharField(label="Описание", required=False,
                                                     widget=forms.widgets.TextInput(attrs={"class": "form-control"}))
    is_adult = forms.BooleanField(label="Взрослый?", initial=True, required=False,
                                  widget=forms.widgets.CheckboxInput(attrs={'class': "form-control"}))
    trustee_first_name = forms.CharField(label="Имя родителя", max_length=50, required=False,
                                         widget=forms.widgets.TextInput(attrs={'class': "form-control"}),
                                         error_messages={'required': "Обязательное поле"})
    trustee_last_name = forms.CharField(label="Фамилия родителя", max_length=30, required=False,
                                        widget=forms.widgets.TextInput(attrs={'class': "form-control"}),
                                        error_messages={'required': "Обязательное поле"})
    trustee_phone = forms.CharField(label="Телефон родителя", max_length=15, required=False,
                                    widget=forms.widgets.TextInput(attrs={'class': "form-control"}))
    trustee_email = forms.EmailField(label="Email родителя", required=False,
                                     widget=forms.widgets.EmailInput(attrs={'class': "form-control"}))
    trustee_additional_contact = forms.CharField(label="Дополнительный контакт родителя", required=False,
                                                 widget=forms.widgets.TextInput(attrs={"class": "form-control"}))
    trustee_additional_contact_description = forms.CharField(label="Описание", required=False,
                                                             widget=forms.widgets.TextInput(attrs={"class": "form-control"}))
