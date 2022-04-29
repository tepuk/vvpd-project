from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user


class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': "Введите старый пароль..."})
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': "Введите новый пароль..."})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': "Введите новый пароль еще раз..."})
        self.fields['old_password'].label = "Старый пароль"
        self.fields['new_password1'].label = "Новый пароль"
        self.fields['new_password1'].help_text = None
        self.fields['new_password2'].label = "Подтверждение нового пароля"

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
