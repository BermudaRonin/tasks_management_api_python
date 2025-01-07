from api.models import Task
from django.utils.timezone import now

# User validators

def user_credentials(userCredentials):
    username = userCredentials.get("username")
    password = userCredentials.get("password")

    if not username:
        return False, "Username is required"
    if not password:
        return False, "Password is required"

    return True, None

# Task validators

def task_priority(value):
    return value in [Task.Priority.LOW, Task.Priority.MEDIUM, Task.Priority.HIGH]

def task_status(value):
    return value in [Task.Status.PENDING, Task.Status.COMPLETED]

def task_category(value):
    return value in [
        Task.Category.WORK,
        Task.Category.PERSONAL,
        Task.Category.UNCATEGORIZED,
    ]

def task_deadline(value):
    return value > now()
    
def task_sort(value):
        attrs = ["title", "deadline", "priority"]
        if value.startswith("-"):
            return value[1:] in attrs
        else:
            return value in attrs

# Query validators

def tasks_query_filters(query_params):
    filters = {}

    status = query_params.get("status")
    priority = query_params.get("priority")
    category = query_params.get("category")

    if status and not task_status(status):
        return None, "Invalid status value"
    if priority and not task_priority(priority):
        return None, "Invalid priority value"
    if category and not task_category(category):
        return None, "Invalid category value"

    if status:
        filters["status"] = status
    if priority:
        filters["priority"] = priority
    if category:
        filters["category"] = category

    return filters, None

def tasks_query_sort(query_params):
    sort = query_params.get("sort")
    if sort and not task_sort(sort):
        return None, "Invalid sort value"
    return sort, None