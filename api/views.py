from enum import Enum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from .models import User, Task
from .services import user_service, task_service
from .utils import respond


@api_view(["POST"])
def authentication(request, param=None):
    """
    Handle user registration and login.
    """

    class Param(Enum):
        REGISTER = "register"
        LOGIN = "login"

    _param = Param(param) if param in Param._value2member_map_ else None

    match _param:
        case Param.REGISTER:
            # Register a new user
            return user_service.create_user(request.data)
        case Param.LOGIN:
            # Authenticate the user
            return user_service.authenticate_user(request.data)
        case _:
            # Invalid param
            return respond.bad_request("Invalid param")

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def user_details(request):
    """
    Handle user details retrieval, update, and deletion.
    """

    # Ensure user is authenticated
    user = get_object_or_404(User, id=request.user.id)

    match request.method:
        case "GET":
            # Return the user details
            return user_service.get_user(user)
        case "PUT":
            # Update the user details
            return user_service.update_user(user, request.data)
        case "DELETE":
            # Delete the user
            return user_service.delete_user(user)

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def tasks_list(request):
    """
    Handle task creation and listing.
    """
    if request.method == "POST":
        # Create a new task
        return task_service.create_task(request)
    else:
        # List all tasks
        return task_service.get_tasks(request)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def task_details(request, id, param=None):
    """
    Handle task retrieval, update, and deletion.
    """
    # Ensure task belongs to the authenticated user
    task = get_object_or_404(Task, id=id, owner=request.user)

    match request.method:
        case "GET":
            # Return the task details
            return task_service.get_task(task)
        case "DELETE":
            # Delete the task
            return task_service.delete_task(task)
        case "PUT":
            
            class Param(Enum):
                COMPLETE = "complete"
                PENDING = "pending"

            _param = Param(param) if param in Param._value2member_map_ else None

            match _param:
                case Param.COMPLETE:
                    # Update the task status to completed
                    return task_service.update_task_status(task, Task.Status.COMPLETED)
                case Param.PENDING:
                    # Update the task status to pending
                    return task_service.update_task_status(task, Task.Status.PENDING)
                case _:
                    # Update the task
                    return task_service.update_task(task, request.data)
