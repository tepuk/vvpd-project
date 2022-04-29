from django.views.generic import ListView, CreateView, DeleteView, UpdateView, TemplateView, FormView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages

from config.permissions import TeacherPermissionsMixin, StudentPermissionsMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *


class TeacherListView(LoginRequiredMixin, TeacherPermissionsMixin, ListView):
    model = Teacher
    template_name = 'teacher_lk.html'


class StudentListView(LoginRequiredMixin, StudentPermissionsMixin, ListView):
    model = Student
    template_name = 'student_lk.html'


class AchievementView(LoginRequiredMixin, TeacherPermissionsMixin, ListView):
    model = Achievement
    template_name = 'achievement.html'
    context_object_name = 'achievements'


class AchievementAddView(LoginRequiredMixin, TeacherPermissionsMixin, CreateView):
    form_class = FormAddAchievement
    template_name = 'add_achievement.html'
    success_url = reverse_lazy('achievement')

    def post(self, request, *args, **kwargs):
        form = FormAddAchievement(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.render_to_response({'form': form})


class AchievementEditView(LoginRequiredMixin, TeacherPermissionsMixin, UpdateView):
    model = Achievement
    form_class = FormUpdateAchievement
    template_name = 'edit_achievement.html'
    success_url = reverse_lazy('achievement')


class AchievementDelView(LoginRequiredMixin, TeacherPermissionsMixin, DeleteView):
    model = Achievement
    template_name = 'del_achievement.html'
    success_url = reverse_lazy('achievement')


class AchievementGetView(LoginRequiredMixin, TeacherPermissionsMixin, CreateView):
    form_class = FormGetAchievement
    template_name = 'get_achievement.html'
    success_url = reverse_lazy('achievement')

    def post(self, request, *args, **kwargs):
        form = FormGetAchievement(self.request.POST)
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.render_to_response({'form': form})


class UpdateStudentView(LoginRequiredMixin, StudentPermissionsMixin, UpdateView):
    model = User
    template_name = 'edit_student_lk.html'
    form_class = StudentUpdateForm
    initial = {}

    def get_initial(self):
        base_initial = super().get_initial()
        base_initial['link_vk'] = Student.objects.get(
            user__pk=self.request.user.pk).link_vk
        base_initial['link_gitlab'] = Student.objects.get(
            user__pk=self.request.user.pk).link_gitlab
        print(base_initial)
        return base_initial

    def get_success_url(self):
        return reverse_lazy('edit_student_lk', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['second_model'] = Student.objects.get(
            user__pk=self.request.user.pk
        )
        return context

    def form_valid(self, form):
        link_vk = form.cleaned_data.get('link_vk', None)
        link_gitlab = form.cleaned_data.get('link_gitlab', None)
        if link_vk and link_gitlab:
            instance = self.get_context_data().get('second_model')
            instance.link_vk = link_vk
            instance.link_gitlab = link_gitlab
            instance.save()
        return super().form_valid(form)

    def post(self, *args, **kwargs):
        messages.success(self.request, 'Ваш профиль успешно обновлен!')
        return super().post(*args, **kwargs)


class UpdateTeacherView(LoginRequiredMixin, TeacherPermissionsMixin, UpdateView):
    model = User
    template_name = 'edit_teacher_lk.html'
    form_class = TeacherUpdateForm

    def get_success_url(self):
        return reverse_lazy('edit_teacher_lk', kwargs={'pk': self.kwargs['pk']})

    def post(self, *args, **kwargs):
        messages.success(self.request, 'Ваш профиль успешно обновлен!')
        return super().post(*args, **kwargs)
