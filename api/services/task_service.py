from api.models import Task
from api.serializers import TaskSerializer
from api.utils import respond, validate

# Task Management Service Layer

def create_task(request):
    """
    Handle the creation of a new task.
    
    Args:
        request (Request): Incoming HTTP request containing task data.
        
    Returns:
        Response: Created task data or validation error response.
    """
    serializer = TaskSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return respond.created_data(serializer.data)
    return respond.validation_error(serializer.errors)

def get_task(task):
    """
    Retrieve a specific task by ID.
    
    Args:
        task (Task): Task instance to retrieve.
        
    Returns:
        Response: Retrieved task data.
    """
    serializer = TaskSerializer(task)
    return respond.retreived_data(serializer.data)

def update_task_status(task, new_status):
    """
    Update the status of an existing task.
    
    Args:
        task (Task): Task instance to update.
        new_status (str): New status to apply to the task.
        
    Returns:
        Response: Updated task response or validation error if status is unchanged.
    """
    if task.status == new_status:
        return respond.validation_error(f"Task is already {new_status}")
    
    updated_data = {"status": new_status}
    return _update_task(task, updated_data)

def update_task(task, task_data):
    """
    Update task details.
    
    Args:
        task (Task): Task instance to update.
        task_data (dict): Data to update in the task.
        
    Returns:
        Response: Updated task response or validation error.
    """
    if task.status == Task.Status.COMPLETED:
        return respond.validation_error("Cannot update completed task")
    
    return _update_task(task, task_data)

def delete_task(task):
    """
    Delete a specific task.
    
    Args:
        task (Task): Task instance to delete.
        
    Returns:
        Response: Confirmation of deletion.
    """
    task.delete()
    return respond.deleted_data()

def get_tasks(query_params):
    """
    Retrieve a list of tasks filtered and sorted by query parameters.
    
    Args:
        query_params (dict): Query parameters for filtering and sorting tasks.
        
    Returns:
        Response: List of retrieved tasks or validation error.
    """
    filters, filters_error = validate.tasks_query_filters(query_params)
    sort, sort_error = validate.tasks_query_sort(query_params)
    
    if filters_error or sort_error:
        return respond.validation_error(filters_error or sort_error)
    
    tasks = Task.objects.filter(**filters).select_related("owner")
    if sort:
        tasks = tasks.order_by(sort)
    
    serializer = TaskSerializer(tasks, many=True)
    return respond.retreived_data(serializer.data)

# Private Helper Function

def _update_task(task, updated_data):
    """
    Internal helper to update task data.
    
    Args:
        task (Task): Task instance to update.
        updated_data (dict): Data to update in the task.
        
    Returns:
        Response: Updated task response or validation error.
    """
    serializer = TaskSerializer(task, data=updated_data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return respond.updated_data(serializer.data)
    return respond.validation_error(serializer.errors)
