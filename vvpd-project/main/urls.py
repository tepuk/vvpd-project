from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *


urlpatterns = [
    path('teacher/', TeacherListView.as_view(), name='teacher'),
    path('teacher/id^<int:pk>/edit/', UpdateTeacherView.as_view(), name="edit_teacher_lk"),
    path('teacher/achievement/all/', AchievementView.as_view(), name='achievement'),
    path('teacher/achievement/add/', AchievementAddView.as_view(), name='achievement_add'),
    path('teacher/achievement/get', AchievementGetView.as_view(), name='get_achievement'),
    path('teacher/achievement/id^<int:pk>/edit/', AchievementEditView.as_view(), name='edit_achievement'),
    path('teacher/achievement/id^<int:pk>/del/', AchievementDelView.as_view(), name='del_achievement'),
    path('student/id^<int:pk>/edit/', UpdateStudentView.as_view(), name="edit_student_lk"),
    path('student/', StudentListView.as_view(), name='student'),
]
