from django.db import models
import uuid
from django.core.validators import RegexValidator, EmailValidator
from django.core import validators


class Student(models.Model):
    def __str__(self):
        return self.name

    id = models.CharField(max_length=120, primary_key=True, unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    age = models.IntegerField()
    level = models.IntegerField(default=0)
    teacher_id = models.ForeignKey('Teacher', on_delete=models.PROTECT)
    class Meta:
        verbose_name = 'student'
        verbose_name_plural = 'students'


class Teacher(models.Model):
    def __str__(self):
        return self.id

    id = models.CharField(max_length=120, primary_key=True, unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    password = models.CharField(blank=False, max_length=128, validators=[
            RegexValidator(
                regex='^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
                message='Password must be at least 8 characters long and contain at least one letter and one number'
            )
        ]
    )
    email = models.EmailField(blank=False, validators=[validators.EmailValidator(message="Invalid Email")])

    class Meta:
        verbose_name = 'teacher'
        verbose_name_plural = 'teachers'


class Lesson(models.Model):
    def __str__(self):
        return self.id

    id = models.CharField(max_length=120, primary_key=True, unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    teacher_id = models.CharField(max_length=120, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    student_id = models.ForeignKey('Student', on_delete=models.PROTECT)
    duration = models.IntegerField(blank=False)
    words = models.JSONField()
    date = models.DateTimeField(auto_now_add=True, blank=True)
    current_percent = models.IntegerField(default=100)

    class Meta:
        verbose_name = 'lesson'
        verbose_name_plural = 'lessons'

