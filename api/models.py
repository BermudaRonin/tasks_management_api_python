from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authentication import TokenAuthentication

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
    
class BearerTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

class Task(models.Model):

    class Priority(models.TextChoices):
        LOW = "LOW"
        MEDIUM = "MEDIUM"
        HIGH = "HIGH"

    class Status(models.TextChoices):
        PENDING = "PENDING"
        COMPLETED = "COMPLETED"

    class Category(models.TextChoices):
        WORK = "WORK"
        PERSONAL = "PERSONAL"
        UNCATEGORIZED = "UNCATEGORIZED"

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=Priority, default=Priority.LOW)
    status = models.CharField(max_length=10, choices=Status, default=Status.PENDING)
    category = models.CharField(max_length=20, choices=Category, default=Category.UNCATEGORIZED)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.title

