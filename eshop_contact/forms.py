from django import forms
from django.core import validators
from django.contrib.auth.models import User


class CreateContactForm(forms.Form):
    full_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'لطفا نام و نام خوانوادگی خود را وارد نمایید', 'class': 'form-control'}),
        label='نام و نام خوانوادگی',
        validators=[validators.MaxLengthValidator(150, "نام و نام خوانوادگی شما نمیتواند بیشتر از 200 باشد")]
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'لطفا ایمیل خود را وارد نمایید', 'class': 'form-control'}),
        label='ایمیل',
        validators=[validators.MaxLengthValidator(150, "ایمیل شما نمیتواند بیشتر از 159 باشد")]
    )

    subject = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا عنوان پیام خود را وارد نمایید', 'class': 'form-control'}),
        label='عنوان',
        validators=[validators.MaxLengthValidator(150, "عنوان پیام شما نمیتواند بیشتر از 200 باشد")]
    )
    text = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder': 'لطفا متن پیام خود را وارد نمایید', 'class': 'form-control', 'rows': '8'}),
        label='پیام',
    )


class CreateEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'لطفا ایمیل خود را وارد نمایید', 'class': 'form-control'}),
        label='ایمیل',
        validators=[validators.MaxLengthValidator(150, "نام و نام خوانوادگی شما نمیتواند بیشتر از 150 باشد")]
    )
