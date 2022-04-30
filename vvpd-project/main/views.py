from config.permissions import StudentPermissionsMixin, TeacherPermissionsMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, FormView, ListView,
                                  TemplateView, UpdateView)

from .forms import *
from .models import *


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


class AchievementAddView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, CreateView):
    form_class = FormAddAchievement
    template_name = 'add_achievement.html'
    success_url = reverse_lazy('achievement_add')
    success_message = "Достижение '%(name)s' было успешно добавленно!"

    def post(self, request, *args, **kwargs):
        form = FormAddAchievement(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.render_to_response({'form': form})


class AchievementEditView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, UpdateView):
    model = Achievement
    form_class = FormUpdateAchievement
    template_name = 'edit_achievement.html'
    success_message = "Достижение было успешно обновленно!"

    def get_success_url(self):
        return reverse_lazy('edit_achievement', kwargs={'pk': self.kwargs['pk']})


class AchievementDelView(LoginRequiredMixin, TeacherPermissionsMixin, DeleteView):
    model = Achievement
    template_name = 'del_achievement.html'
    success_url = reverse_lazy('achievement')


class AchievementGetView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, CreateView):
    form_class = FormGetAchievement
    template_name = 'get_achievement.html'
    success_message = "Достижение '%(achievement)s' было успешно выдано '%(student)s!'"
    success_url = reverse_lazy('get_achievement')

    def post(self, request, *args, **kwargs):
        form = FormGetAchievement(self.request.POST)
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            messages.error(
                request, 'Данное достижение уже выданно этому студенту!')
            return self.render_to_response({'form': form})


class UpdateStudentView(LoginRequiredMixin, StudentPermissionsMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'edit_student_lk.html'
    success_message = "Ваш профиль успешно обновлен!"
    form_class = StudentUpdateForm
    initial = {}

    def get_initial(self):
        base_initial = super().get_initial()
        base_initial['link_vk'] = Student.objects.get(
            user__pk=self.request.user.pk).link_vk
        base_initial['link_gitlab'] = Student.objects.get(
            user__pk=self.request.user.pk).link_gitlab
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
        if link_vk or link_gitlab:
            instance = self.get_context_data().get('second_model')
            instance.link_vk = link_vk
            instance.link_gitlab = link_gitlab
            instance.save()
        return super().form_valid(form)


class UpdateTeacherView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'edit_teacher_lk.html'
    success_message = "Ваш профиль успешно обновлен!"
    form_class = TeacherUpdateForm

    def get_success_url(self):
        return reverse_lazy('edit_teacher_lk', kwargs={'pk': self.kwargs['pk']})


class StudentCreateView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'add_student.html'
    success_url = reverse_lazy('student_add')
    success_message = 'Cтудент усешно добавлен'

    def get_context_data(self, **kwargs):
        data = super(StudentCreateView, self).get_context_data(**kwargs)
        data['student_form'] = StudentForm()
        return data

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        student_form = StudentForm(self.request.POST)
        if form.is_valid() and student_form.is_valid():
            user = form.save(commit=False)
            user.user_status = 'student'
            student = student_form.save(commit=False)
            student.user = user
            user.save()
            student.save()
            return self.form_valid(form)
        else:
            return self.render_to_response({'form': form, 'student_form': student_form})


class GroupCreateView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, CreateView):
    form_class = GroupCreateForm
    template_name = 'add_group.html'
    success_message = 'Группа успешно добавлена'
    success_url = reverse_lazy('group_add')


class WorkCreateView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, CreateView):
    form_class = WorkCreateForm
    template_name = 'add_work.html'
    success_message = 'Практическая работа успешно добавлена'
    success_url = reverse_lazy('work_add')


class WorkView(LoginRequiredMixin, TeacherPermissionsMixin, ListView):
    model = Work
    template_name = 'work.html'
    context_object_name = 'works'


class GroupView(LoginRequiredMixin, TeacherPermissionsMixin, ListView):
    model = Group
    template_name = 'group.html'
    context_object_name = 'groups'
