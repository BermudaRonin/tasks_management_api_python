from rest_framework.generics import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

from .serializers import TaskSerializer, UserSerializer
from .models import Task, User
from .utils import TaskValidator, Respond

@api_view(["GET"])
def endpoints_summary(request):
    return Respond.retreived({
        "Authentication": {
            "Register user": "POST /api/auth/register",
            "Login user": "POST /api/auth/login",
        },
        "User manaegement": {
            "Get current user": "GET /api/user",
            "Update current user": "PUT /api/user",
            "Delete current user": "DELETE /api/user",
        },
        "Tasks management": {
            "Create task": "POST /api/task",
            "Get tasks": "GET /api/tasks",
        },
        "Task management": {
            "Get task by id": "GET /api/task/{id}",
            "Update task by id": "PUT /api/task/{id}",
            "Complete task by id": "PUT /api/task/{id}/complete",
            "Uncomplete task by id": "PUT /api/task/{id}/pending",
            "Delete task by id": "DELETE /api/task/{id}",
        },
    })

@api_view(["POST"])
def auth_controller(request, action):
    """
    Handle user authentication: registration and login.
    """
    if action == "register":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Respond.created(serializer.data)
        else:
            return Respond.request_error(serializer.errors)
    elif action == "login":
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Respond.request_error("Missing credentials")

        user = authenticate(username=username, password=password)

        if not user:
            return Respond.request_error("Invalid credentials")

        serializer = UserSerializer(user, many=False)

        token, created = Token.objects.get_or_create(user=user)

        return Respond.retreived({"user": serializer.data, "token": token.key})
    else:
        return Respond.request_error("Invalid action")

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def user_controller(request):
    """
    Handle user-related actions: retrieve, update, and delete user.
    """
    user = get_object_or_404(User, id=request.user.id)

    if request.method == "GET":
        serializer = UserSerializer(user, many=False)
        return Respond.created(serializer.data)

    elif request.method == "PUT":
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Respond.updated()
        else:
            return Respond.request_error("Error updating user")

    elif request.method == "DELETE":
        user.delete()
        return Respond.deleted()

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def task_controller(request, task_id, action=None):
    """
    Handle task-related actions: retrieve, update, and delete tasks.
    """
    task = get_object_or_404(Task, id=task_id, owner=request.user)

    if request.method == "GET":
        serializer = TaskSerializer(task, many=False)
        return Respond.retreived(serializer.data)

    elif request.method == "PUT":

        update = None

        if not action:
            if task.status == Task.Status.COMPLETED:
                return Respond.request_error("Cannot edit a completed Task")
            update = request.data
        elif action == "complete":
            if task.status == Task.Status.COMPLETED:
                return Respond.request_error("Task is already completed")
            update = {"status": Task.Status.COMPLETED}
        elif action == "pending":
            if task.status == Task.Status.PENDING:
                return Respond.request_error("Task is already pending")
            update = {"status": Task.Status.PENDING}
        else:
            return Respond.request_error("Invalid endpoint : /task/<id>/" + action)

        serializer = TaskSerializer(task, data=update, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Respond.updated()
        else:
            return Respond.request_error("Error updating task")

    elif request.method == "DELETE":
        task.delete()
        return Respond.deleted()

@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def tasks_controller(request):
    """
    Handle task creation and retrieval.
    """
    if request.method == "POST":
        serializer = TaskSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Respond.created(serializer.data)
        else:
            return Respond.request_error(serializer.errors)
    else:
        tasks = Task.objects.filter(owner=request.user).select_related("owner")

        ## Filters
        filters = {}
        status = request.query_params.get("status")
        priority = request.query_params.get("priority")
        category = request.query_params.get("category")

        if status and not TaskValidator.status(status):
            return Respond.request_error("Invalid status value")
        if priority and not TaskValidator.priority(priority):
            return Respond.request_error("Invalid priority value")
        if category and not TaskValidator.category(category):
            return Respond.request_error("Invalid category value")

        if status:
            filters["status"] = status
        if priority:
            filters["priority"] = priority
        if category:
            filters["category"] = category

        tasks = tasks.filter(**filters)

        ## Sorting

        sort = request.query_params.get("sort")

        if sort and not TaskValidator.sort(sort):
            return Respond.request_error("Invalid sort value")

        if sort:
            tasks = tasks.order_by(sort)

        serializer = TaskSerializer(tasks, many=True)
        return Respond.retreived(serializer.data)
