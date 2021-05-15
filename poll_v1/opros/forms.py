from django import forms
# from models import models
import re
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Variant


class ContactForm(forms.Form):
    subject = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # subject = forms.CharField(widget=forms.HiddenInput())
    content = forms.CharField(label='Текст вопроса', widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5}))



