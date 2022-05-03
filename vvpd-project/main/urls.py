from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *

urlpatterns = [
    # URL teacher
    path('teacher/', TeacherView.as_view(), name='teacher'),
    path('teacher/id^<int:pk>/edit/', TeacherUpdateView.as_view(), name="edit_teacher_lk"),
    path('teacher/achievement/view/', AchievementListView.as_view(), name='achievement'),
    path('teacher/achievement/add/', AchievementCreateView.as_view(), name='achievement_add'),
    path('teacher/achievement/get', GetAchievementCreateView.as_view(), name='get_achievement'),
    path('teacher/achievement/id^<int:pk>/edit/', AchievementUpdateView.as_view(), name='edit_achievement'),
    path('teacher/achievement/id^<int:pk>/del/', AchievementDeleteView.as_view(), name='del_achievement'),
    path('teacher/student/add/', StudentCreateView.as_view(), name='student_add'),
    path('teacher/group/add/', GroupCreateView.as_view(), name='group_add'),
    path('teacher/work/add/', WorkCreateView.as_view(), name='work_add'),
    path('teacher/work/^<int:pk>/delete/', WorkDeleteView.as_view(), name='delete_work'),
    path('teacher/work/^<int:pk>/edit', WorkUpdateView.as_view(), name='update_work'),
    path('teacher/work/all/', WorkListView.as_view(), name='work'),
    path('teacher/group/all/', GroupListView.as_view(), name='group'),
    path('teacher/student/all/', StudentListView.as_view(), name='student_view'),
    path('teacher/student/^<int:pk>/info/', StudentDetailView.as_view(), name='student_detail'),
    path('teacher/student/^<int:student_id>/info/id^<int:pk>/edit/', GradeWorkUpdateView.as_view(), name='grade_work_edit'),
    path('teacher/student/^<int:student_id>/info/^<int:work_id>/grade/', GradeWorkCreateView.as_view(), name='grade_work'),

    # URL student
    path('student/id^<int:pk>/edit/', StudentUpdateView.as_view(), name="edit_student_lk"),
    path('student/', StudentView.as_view(), name='student'),
]
