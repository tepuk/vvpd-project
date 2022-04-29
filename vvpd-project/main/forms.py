from django import forms
from django.forms.models import modelformset_factory
from .models import *


class FormAddAchievement(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['name', 'description', 'image']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Название достижения'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Изображение'
            })
        }


class FormUpdateAchievement(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['name', 'description', 'image']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Название достижения'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Изображение'
            })
        }


class FormGetAchievement(forms.ModelForm):
    class Meta:
        model = GetAchievement
        fields = ['student', 'achievement']

    def __init__(self, *args, **kwargs):
        super(FormGetAchievement, self).__init__(*args, **kwargs)
        self.fields['student'].empty_label = ' '
        self.fields['achievement'].empty_label = ' '


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'email']
        widgets = {'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
                   'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
                   'middle_name': forms.TextInput(attrs={'placeholder': 'Отчество'}),
                   'email': forms.TextInput(attrs={'placeholder': 'E-mail'}),
                   }


class StudentUpdateForm(forms.ModelForm):
    link_vk = forms.URLField(label='Ссылка на VK', required=False)
    link_gitlab = forms.URLField(label='Сcылка на GitLab', required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'email']


class TeacherUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'email']
