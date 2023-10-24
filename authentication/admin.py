from django.contrib import admin
from authentication.models import Student, Teacher, Lesson

admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Lesson)
