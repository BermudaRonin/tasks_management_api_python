from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from .models import Task

"""
Validators
"""


class TaskValidator:
    def priority(value):
        return value in [Task.Priority.LOW, Task.Priority.MEDIUM, Task.Priority.HIGH]

    def status(value):
        return value in [Task.Status.PENDING, Task.Status.COMPLETED]

    def category(value):
        return value in [
            Task.Category.WORK,
            Task.Category.PERSONAL,
            Task.Category.UNCATEGORIZED,
        ]

    def deadline(value):
        return value > now()

    def sort(value):
        attrs = ["title", "deadline", "priority"]
        if value.startswith("-"):
            return value[1:] in attrs
        else:
            return value in attrs


"""
REST responses
"""


class Respond:
    @staticmethod
    def deleted():
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @staticmethod
    def updated():
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def retreived(data):
        return Response(status=status.HTTP_200_OK, data=data)

    @staticmethod
    def created(data):
        return Response(status=status.HTTP_201_CREATED, data=data)

    @staticmethod
    def request_error(message="Invalid request"):
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": message})
    
    @staticmethod
    def unauthorized(message="Unauthorized"):
        return Response(status=status.HTTP_401_UNAUTHORIZED, data={"error": message})
