from django.urls import path
from authentication.models import Student
from ninja import NinjaAPI
from ninja.schema import Schema


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


urlpatterns = [
    path("", api.urls, name="say hello"),
]
