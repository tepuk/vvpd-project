from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from .forms import PasswordChangeForm


class LoginUser(LoginView):
    redirect_authenticated_user = True


class UserTypeRedirectView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.user_status == 'student':
            return reverse_lazy('student')
        else:
            return reverse_lazy('teacher')


class ChangePassword(LoginRequiredMixin, TemplateView):
    form_class = PasswordChangeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(self.request.user)
        return render(request, 'change_password.html', {'form': form, })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Пароль успешно изменен')
            update_session_auth_hash(request, user)
            return render(request, 'change_password.html', {'form': form})
        else:
            return render(request, 'change_password.html', {'form': form})
