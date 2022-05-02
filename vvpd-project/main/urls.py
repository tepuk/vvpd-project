from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *

urlpatterns = [
    path('teacher/', TeacherListView.as_view(), name='teacher'),
    path('teacher/id^<int:pk>/edit/', UpdateTeacherView.as_view(), name="edit_teacher_lk"),
    path('teacher/achievement/all/', AchievementView.as_view(), name='achievement'),
    path('teacher/achievement/add/', AchievementAddView.as_view(), name='achievement_add'),
    path('teacher/achievement/get', AchievementGetView.as_view(), name='get_achievement'),
    path('teacher/achievement/id^<int:pk>/edit/', AchievementEditView.as_view(), name='edit_achievement'),
    path('teacher/achievement/id^<int:pk>/del/', AchievementDelView.as_view(), name='del_achievement'),
    path('teacher/student/add/', StudentCreateView.as_view(), name='student_add'),
    path('teacher/group/add/', GroupCreateView.as_view(), name='group_add'),
    path('teacher/work/add/', WorkCreateView.as_view(), name='work_add'),
    path('teacher/work/all/', WorkView.as_view(), name='work'),
    path('teacher/group/all/', GroupView.as_view(), name='group'),
    path('teacher/student/all/', StudentView.as_view(), name='student_view'),
    path('teacher/student/^<int:pk>/info/', StudentDetailView.as_view(), name='student_detail'),
    path('teacher/student/^<int:student_id>/info/^<int:work_id>/grade/', GradeWorkCreateView.as_view(), name='grade_work'),
    path('teacher/group/^<int:pk>/info/', GroupDetailView.as_view(), name='group_detail'),
    path('student/id^<int:pk>/edit/', UpdateStudentView.as_view(), name="edit_student_lk"),
    path('student/', StudentListView.as_view(), name='student'),
]