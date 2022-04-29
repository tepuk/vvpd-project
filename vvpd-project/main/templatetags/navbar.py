from django import template

from main.models import User, Teacher

register = template.Library()


@register.inclusion_tag('sidebar/student_sidebar.html', name='student_sidebar')
def student_sidebar(user):
    return {'user': user}


@register.inclusion_tag('sidebar/teacher_sidebar.html', name='teacher_sidebar')
def teacher_sidebar(user):
    return {'user': user}
