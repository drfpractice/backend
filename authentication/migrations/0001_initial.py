# Generated by Django 4.2.5 on 2023-11-05 16:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=120, primary_key=True, serialize=False, unique=True, verbose_name='Public identifier')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('surname', models.CharField(blank=True, max_length=50)),
                ('password', models.CharField(max_length=128, validators=[django.core.validators.RegexValidator(message='Password must be at least 8 characters long and contain at least one letter and one number', regex='^(?=.*[A-Za-z])(?=.*\\d)[A-Za-z\\d]{8,}$')])),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator(message='Invalid Email')])),
            ],
            options={
                'verbose_name': 'teacher',
                'verbose_name_plural': 'teachers',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=120, primary_key=True, serialize=False, unique=True, verbose_name='Public identifier')),
                ('name', models.CharField(blank=True, max_length=30)),
                ('surname', models.CharField(blank=True, max_length=50)),
                ('age', models.IntegerField()),
                ('level', models.IntegerField(default=0)),
                ('teacher_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='authentication.teacher')),
            ],
            options={
                'verbose_name': 'student',
                'verbose_name_plural': 'students',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=120, primary_key=True, serialize=False, unique=True, verbose_name='Public identifier')),
                ('duration', models.IntegerField()),
                ('words', models.JSONField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('current_percent', models.IntegerField(default=100)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='authentication.student')),
                ('teacher_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='authentication.teacher')),
            ],
            options={
                'verbose_name': 'lesson',
                'verbose_name_plural': 'lessons',
            },
        ),
    ]