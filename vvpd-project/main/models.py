from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse_lazy
from PIL import Image

TYPE_USERS = [
    ("student", 'Студент'),
    ("teacher", 'Преподаватель')
]


TYPE_FORM_OF_EDUCATIONS = [
    (None, ''),
    ('очная', 'Очная'),
    ('заочная', 'Заочная')
]


class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    middle_name = models.CharField("Отчество", max_length=100, blank=True)
    user_status = models.CharField(
        "Статус", choices=TYPE_USERS, max_length=100)

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    get_full_name.short_description = 'Ф.И.О.'


class Teacher(models.Model):
    class Meta:
        verbose_name = "Предподаватель"
        verbose_name_plural = "Предподаватели"

    user = models.OneToOneField(
        User, verbose_name="Аккаунт", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


class Student(models.Model):
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    user = models.OneToOneField(
        User, verbose_name="Аккаунт", on_delete=models.CASCADE)
    group = models.ForeignKey(
        "Group", verbose_name="Группа", on_delete=models.CASCADE)
    form_of_education = models.CharField(
        "Форма обучения", max_length=7, choices=TYPE_FORM_OF_EDUCATIONS, default='очная')
    link_vk = models.URLField("Ссылка на ВК", blank="True")
    link_gitlab = models.URLField("Ссылка на gitlab", blank="True")

    def __str__(self):
        return f'{self.user.get_full_name()} {self.group}'


class Group(models.Model):
    name = models.CharField("Название группы", max_length=60, unique=True)
    year_of_enrollment = models.CharField("Год зачисления", max_length=4, validators=[
                                          RegexValidator("^[2][0-9]{3}$", message="Неверный формат ввода года")])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


class Work(models.Model):
    name = models.CharField(
        max_length=150, verbose_name="Название работы", unique=True)
    description = models.TextField(verbose_name="Описание")
    dedline = models.DateTimeField('Дедлайн')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Практическая работа"
        verbose_name_plural = "Практические работы"


class Achievement(models.Model):
    name = models.CharField("Название достижения", max_length=100, unique=True)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="static/img/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('achievement', kwargs={'pk': self.user_id})

    def save(self, *args, **kwargs):
        super(Achievement, self).save(*args, **kwargs)

        MAX_SIZE = 100

        if self.image:
            filepath = self.image.path
            width = self.image.width
            height = self.image.height

            max_size = max(width, height)

            if max_size > MAX_SIZE:
                image = Image.open(filepath)
                image = image.resize(
                    (round(width / max_size * MAX_SIZE),
                     round(height / max_size * MAX_SIZE)),
                    Image.ANTIALIAS
                )
                image.save(filepath)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(Achievement, self).delete(*args, **kwargs)
        storage.delete(path)

    class Meta:
        verbose_name = "Достижение"
        verbose_name_plural = "Достижения"


class GetAchievement(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name="Студент")
    achievement = models.ForeignKey(
        Achievement, on_delete=models.CASCADE, verbose_name="Достижение")
    issued_on_hand = models.BooleanField("Выдана студенту", default=False)

    def __str__(self):
        return f'{self.achievement} выдана {self.student}'

    class Meta:
        unique_together = ('student', 'achievement')


class Grade(models.Model):
    grade = models.PositiveSmallIntegerField(blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
