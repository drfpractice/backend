from django.db import models
import uuid


class Student(models.Model):
    def __str__(self):
        return self.name

    id = models.CharField(max_length=120, primary_key=True, unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    age = models.IntegerField()
    level = models.IntegerField(default=0)
    teacher_id = models.CharField(max_length=120, blank=False)

    class Meta:
        verbose_name = 'student'
        verbose_name_plural = 'students'


class Teacher(models.Model):
    def __str__(self):
        return self.id

    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    password = models.IntegerField(blank=False)
    email = models.IntegerField(blank=False)

    class Meta:
        verbose_name = 'teacher'
        verbose_name_plural = 'teachers'


class Lesson(models.Model):
    def __str__(self):
        return self.id

    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    teacher_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    student_id = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
    duration = models.IntegerField(blank=False)
    words = models.JSONField()
    date = models.DateTimeField(blank=False)
    current_percent = models.IntegerField(default=100)

    class Meta:
        verbose_name = 'lesson'
        verbose_name_plural = 'lessons'

