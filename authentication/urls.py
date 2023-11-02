from http.client import HTTPException, HTTPResponse

from django.http import response
from django.urls import path

from authentication.models import Student, Teacher, Lesson
from ninja import NinjaAPI
from ninja.schema import Schema
import datetime
import json

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import bcrypt


api = NinjaAPI()


class StudentSchema(Schema):
    name: str
    surname: str
    age: int
    level: int
    teacher_id_id: str


class StudentSchemaWithId(StudentSchema):
    id: str


@api.get("/student")
def get_student(request):
    students = Student.objects.all()
    content = [StudentSchemaWithId.from_orm(i).dict() for i in students]

    return content


@api.post("/student")
def create_student(request, payload: StudentSchema):
    student = Student.objects.create(**payload.dict())
    student.save()

    return {"id": student.id}


@api.get("/student/{sid}")
def get_student(request, sid: str):
    student = [Student.objects.get(id=sid)]
    return [StudentSchemaWithId.from_orm(i).dict() for i in student][0]

class TeacherSchema(Schema):
    name: str
    surname: str
    password: str
    email: str

class TeacherSchemaWithId(TeacherSchema):
    id: str



@api.get("/teacher")
def get_teacher(request):
    teachers = Teacher.objects.all()
    content = [TeacherSchemaWithId.from_orm(i).dict() for i in teachers]

    return content


@api.post("/teacher")
def create_teacher(request, payload: TeacherSchema):
    hashed_password = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt(5))
    teacher = Teacher.objects.create(
        name=payload.name,
        surname=payload.surname,
        email=payload.email,
        password=hashed_password.decode('utf-8')  # Store the hashed password as a string
    )
    teacher.save()

    return {"id": teacher.id}

@api.get("/teacher/{sid}")
def get_teacher(request, sid: str):
    teacher = [Teacher.objects.get(id=sid)]
    return [TeacherSchemaWithId.from_orm(i).dict() for i in teacher][0]

@api.put("/teacher")
def update_teacher(request, sid: str, payload: TeacherSchema):
    try:
        teacher = Teacher.objects.get(id=sid)
    except Teacher.DoesNotExist:
        raise HTTPException(status_code=404, detail="Преподаватель не найден")

    for attr, value in payload.dict().items():
        setattr(teacher, attr, value)

    teacher.save()


class LessonSchema(Schema):
    student_id: str
    duration: int
    words: str
    date: str
    current_percent: int


class LessonSchemaWithId(LessonSchema):
    id: str
    date: datetime.datetime


@api.get("/lesson")
def get_lesson(request):
    lessons = Lesson.objects.all()
    content = [LessonSchemaWithId.from_orm(i).dict() for i in lessons]

    return content


@api.post("/lesson")
def create_lesson(request, payload: LessonSchema):
    # Предположим, что payload содержит teacher_id и student_id, полученные из запроса
    student_id = payload.student_id

    # Попробуйте получить объект Teacher и Student на основе предоставленных teacher_id и student_id
    try:
        student = Student.objects.get(id=student_id)
    except Teacher.DoesNotExist:
        return {"error": "Teacher not found"}
    except Student.DoesNotExist:
        return {"error": "Student not found"}

    # Создайте объект Lesson с присвоением teacher и student
    lesson = Lesson(
        student_id=student,
        duration=payload.duration,
        words=payload.words,
        current_percent=payload.current_percent
    )
    lesson.save()

    # return {"id": lesson.id}



@api.get("/lesson/{sid}")
def get_teacher(request, sid: str):
    lesson = [Lesson.objects.get(id=sid)]
    return [LessonSchemaWithId.from_orm(i).dict() for i in lesson][0]


@api.put("/lesson")
def update_teacher(request, sid: str, payload: LessonSchema):
    try:
        lesson = Lesson.objects.get(id=sid)
    except Lesson.DoesNotExist:
        raise HTTPException(status_code=404, detail="Урок не найден")

    for attr, value in payload.dict().items():
        setattr(lesson, attr, value)

    lesson.save()

    return response.HttpResponse("200")



class LessonSchemaWithId1(Schema):
        id: str
        duration: int
        words: str
        date: datetime.datetime
        current_percent: int



@api.get("/teacher/{tid}/students-with-lessons")
def get_students_with_lessons(request, tid: str):
    try:
        # Попробуйте найти учителя по ID
        teacher = Teacher.objects.get(id=tid)
    except Teacher.DoesNotExist:
        raise HTTPException(status_code=404, detail="Учитель не найден")

    # Теперь найдите всех студентов, связанных с этим учителем
    students = Student.objects.filter(teacher_id_id=tid)

    teacher_data = TeacherSchemaWithId.from_orm(teacher).dict()

    students_with_lessons = []

    for student in students:
        student_data = StudentSchemaWithId.from_orm(student).dict()
        lessons = Lesson.objects.filter(student_id=student.id)
        lesson_data = [LessonSchemaWithId1.from_orm(lesson).dict() for lesson in lessons]
        student_data["lessons"] = lesson_data
        students_with_lessons.append(student_data)

    return {
        "teacher": teacher_data,
        "students_with_lessons": students_with_lessons
    }

@api.post("/login")
def login(request, mail: str, password: str):
    try:
        teacher = Teacher.objects.get(email=mail)
    except Teacher.DoesNotExist:
        return response.HttpResponse("User not found")

        # Verify the hashed password
    if bcrypt.checkpw(password.encode('utf-8'), teacher.password.encode('utf-8')):
            # Password is correct
            # Create a token for the user here if you have a token-based authentication system
            # Return appropriate response
        return {"id": teacher.id}
    teacher = Teacher.objects.get(email=mail)
    if teacher.password == password:
        return {"id": teacher.id}
    elif teacher.password != password:
        return response.HttpResponse("pass incorrect")
    else:
            # Password is incorrect
        return response.HttpResponse("Login failed")


@api.get("tokens")
def get_tokens_for_user(request, id: str):
    refresh = RefreshToken.for_user(id)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



urlpatterns = [
    path("", api.urls, name="say hello"),
    path("", api.urls, name="say hello"),
    path("token", TokenObtainPairView.as_view())
]
