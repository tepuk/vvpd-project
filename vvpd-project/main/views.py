from config.permissions import StudentPermissionsMixin, TeacherPermissionsMixin
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, FormView, ListView,
                                  TemplateView, UpdateView, DetailView, View)

from .forms import *
from .models import *


class TeacherView(LoginRequiredMixin, TeacherPermissionsMixin, View):
    def get(self, request):
        return render(request, 'teacher_lk.html')


class StudentView(LoginRequiredMixin, StudentPermissionsMixin, View):
    def get(self, request):
        return render(request, 'student_lk.html')


class AchievementListView(LoginRequiredMixin, TeacherPermissionsMixin, ListView):
    model = Achievement
    template_name = 'achievement.html'
    context_object_name = 'achievements'


class AchievementCreateView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, CreateView):
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


class AchievementUpdateView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, UpdateView):
    model = Achievement
    form_class = FormUpdateAchievement
    template_name = 'edit_achievement.html'
    success_message = "Достижение было успешно обновленно!"

    def get_success_url(self):
        return reverse_lazy('edit_achievement', kwargs={'pk': self.kwargs['pk']})


class AchievementDeleteView(LoginRequiredMixin, TeacherPermissionsMixin, DeleteView):
    model = Achievement
    template_name = 'del_achievement.html'
    success_url = reverse_lazy('achievement')


class GetAchievementCreateView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, CreateView):
    form_class = FormGetAchievement
    template_name = 'get_achievement.html'
    success_message = "Достижение '%(achievement)s' было успешно выдано '%(student)s!'"
    success_url = reverse_lazy('get_achievement')

    def post(self, request, *args, **kwargs):
        form = FormGetAchievement(self.request.POST)
        students = Student.objects.all()
        groups = Group.objects.all()
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.error(
                request, 'Что-то пошло не так, попробуйте снова!')
            return self.render_to_response({'form': form, 'students': students, 'groups': groups})

    def get_context_data(self, **kwargs):
        data = super(GetAchievementCreateView, self).get_context_data(**kwargs)
        data['students'] = Student.objects.all()
        data['groups'] = Group.objects.all()
        return data


class StudentUpdateView(LoginRequiredMixin, StudentPermissionsMixin, SuccessMessageMixin, UpdateView):
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


class TeacherUpdateView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, UpdateView):
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
    success_message = 'Cтудент успешно добавлен'

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


class WorkListView(LoginRequiredMixin, TeacherPermissionsMixin, ListView):
    model = Work
    template_name = 'work.html'
    context_object_name = 'works'


class GroupListView(LoginRequiredMixin, TeacherPermissionsMixin, ListView):
    model = Group
    template_name = 'group.html'
    context_object_name = 'groups'


class StudentListView(LoginRequiredMixin, TeacherPermissionsMixin, ListView):
    model = Student
    template_name = 'student.html'
    context_object_name = 'students'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['years'] = set(
            [x.year_of_enrollment for x in Group.objects.all()]
        )
        return context


class StudentDetailView(LoginRequiredMixin, TeacherPermissionsMixin, DetailView):
    template_name = 'student_detail.html'

    def get_queryset(self):
        queryset = User.objects.select_related(
            'student__group').filter(user_status='student')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['works'] = Work.objects.all()
        context['grades'] = Grade.objects.filter(student__user=context['user'])
        context['work_grade'] = [x.work for x in Grade.objects.filter(
            student__user=context['user'])]
        return context


class GradeWorkCreateView(LoginRequiredMixin, TeacherPermissionsMixin, CreateView):
    template_name = 'grade_work.html'
    form_class = GradeWorkCreateForm

    def post(self, request, student_id, work_id, *args, **kwargs):
        form = GradeWorkCreateForm(self.request.POST)
        if form.is_valid():
            forms = form.save(commit=False)
            forms.student = Student.objects.get(user__id=student_id)
            forms.work = Work.objects.get(id=work_id)

            # Расчет оценки за дедлайн: 1 нелеля - 10 баллов
            dedline = Work.objects.get(id=work_id).dedline
            date_of_delivery = forms.date_of_delivery
            grade_work = int(str(date_of_delivery - dedline).split()[0])

            if grade_work > 0:
                if (100 - abs(grade_work // 6) * 10) < 0:
                    forms.grade = 0
                else:
                    forms.grade = (100 - abs(grade_work // 6) * 10)
            else:
                forms.grade = 100
            form.save()
            return self.form_valid(form)

        return self.render_to_response({'form': form})

    def get_success_url(self):
        return reverse_lazy('student_detail', kwargs={'pk': self.kwargs['student_id']})


class GradeWorkUpdateView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, UpdateView):
    model = Grade
    template_name = 'update_student_grade.html'
    success_message = "Оценка за практическую работу успешно обновлена!"
    form_class = GradeUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student_id'] = self.kwargs['student_id']
        return context

    def get_success_url(self):
        return reverse_lazy('grade_work_edit', kwargs={'student_id': self.kwargs['student_id'], 'pk': self.kwargs['pk']})


class WorkUpdateView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, UpdateView):
    model = Work
    form_class = WorkUpdateForm
    template_name = 'work_update.html'
    success_message = "Практическая работа успешно обновлена!"

    def get_success_url(self):
        return reverse_lazy('update_work', kwargs={'pk': self.kwargs['pk']})


class WorkDeleteView(LoginRequiredMixin, TeacherPermissionsMixin, SuccessMessageMixin, DeleteView):
    model = Work
    template_name = 'work_delete.html'
    success_url = reverse_lazy('work')
