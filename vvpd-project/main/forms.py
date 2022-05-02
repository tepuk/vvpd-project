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
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Фамилия'
            }),
            'middle_name': forms.TextInput(attrs={
                'placeholder': 'Отчество'
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'E-mail'
            }),
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


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'password', 'first_name', 'last_name', 'middle_name',
            'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Имя пользователя'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Пароль'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Фамилия'
            }),
            'middle_name': forms.TextInput(attrs={
                'placeholder': 'Отчество'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email'
            }),
        }

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ('user', 'link_vk', 'link_gitlab')


class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Название группы'
            }),
            'year_of_enrollment': forms.TextInput(attrs={
                'placeholder': 'Год зачисления'
            }),
        }


class WorkCreateForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Название'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Описание'
            }),
            'dedline': forms.DateInput(attrs={
                'type': 'datetime-local'
            }),
        }


class GradeWorkCreateForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['grade_for_protection', 'comment', 'date_of_delivery']
        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Комментарий'
            }),
            'date_of_delivery': forms.DateInput(attrs={
                'type': 'datetime-local'
            }),
        }


StudentFormSet = modelformset_factory(Student, form=StudentForm, max_num=1, extra=1)
