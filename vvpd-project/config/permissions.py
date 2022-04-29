from django.core.exceptions import PermissionDenied


class TeacherPermissionsMixin:
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permissions():
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def has_permissions(self):
        return self.request.user.is_superuser or self.request.user.user_status == 'teacher'


class StudentPermissionsMixin(TeacherPermissionsMixin):
    def has_permissions(self):
        return self.request.user.is_superuser or self.request.user.user_status == 'student'
