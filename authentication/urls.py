from django.urls import path
from authentication.models import Student, Teacher, Lesson
from ninja import NinjaAPI
from ninja.schema import Schema
import datetime

api = NinjaAPI()


class StudentSchema(Schema):
    name: str
    surname: str
    age: int
    level: int


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
    teacher = Teacher.objects.create(**payload.dict())
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
    teacher_id: str
    student_id: str
    duration: int
    words: str
    date: str
    current_percent: int


class LessonSchemaWithId(Schema):
    id: str
    teacher_id: str
    student_id: str
    duration: int
    words: str
    date: datetime.datetime
    current_percent: int


@api.get("/lesson")
def get_lesson(request):
    lessons = Lesson.objects.all()
    content = [LessonSchemaWithId.from_orm(i).dict() for i in lessons]

    return content


@api.post("/lesson")
def create_lesson(request, payload: LessonSchema):
    lesson = Lesson.objects.create(**payload.dict())
    lesson.save()

    return {"id": lesson.id}

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



urlpatterns = [
    path("", api.urls, name="say hello"),
]
