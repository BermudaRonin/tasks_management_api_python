from rest_framework.serializers import ModelSerializer, ValidationError
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password

from .models import Task, User
from api.utils import validate

class UserSerializer(ModelSerializer):
    '''
    Serializer for User model
    '''
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class TaskSerializer(ModelSerializer):
    '''
    Serializer for Task model
    '''
    class Meta:
        model = Task
        fields = ["id", "title", "description", "category", "priority", "deadline", "status", "completion_date", "owner"]
        read_only_fields = ["completion_date", "owner"]

    # Validate task fields, title is already validated by model
    def validate(self, next):
        deadline = next.get("deadline")
        status = next.get("status")
        priority = next.get("priority")
        category = next.get("category")

        if deadline and validate.task_deadline(deadline):
            raise ValidationError("Deadline must be in the future.")

        if status and not validate.task_status(status):
            raise ValidationError("Invalid status")

        if priority and not validate.task_priority(priority):
            raise ValidationError("Invalid priority")

        if category and not validate.task_category(category):
            raise ValidationError("Invalid category")

        return next
    
    def create(self, validated_data):
        # Append user to validated data
        request = self.context['request']
        validated_data['owner'] = request.user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Update completion_date on status change

        if validated_data.get("status") == Task.Status.COMPLETED:
            validated_data["completion_date"] = now()

        if validated_data.get("status") == Task.Status.PENDING:
            validated_data["completion_date"] = None

        return super().update(instance, validated_data)
