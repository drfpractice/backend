from django.urls import path
from authentication.models import Student
from rest_framework.serializers import Serializer
from ninja import NinjaAPI
from ninja.schema import Schema

api = NinjaAPI()


class StudentSchema(Schema):
    name: str
    surname: str
    age: int
    level: int


@api.get("/get")
def get(request):
    students = Student.objects.all()
    content = [StudentSchema.from_orm(i).dict() for i in students]

    return content


@api.post("/create")
def create(request, payload: StudentSchema):
    student = Student.objects.create(**payload.dict())
    student.save()

    return {"id": student.id}


urlpatterns = [
    path("", api.urls, name="say hello")
]
