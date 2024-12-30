from django.urls import path
from . import views

urlpatterns = [
    path("", views.endpoints_summary, name="endpoints_summary"),
    path("/auth/<str:action>", views.auth_controller, name="auth_controller"),
    path("/user", views.user_controller, name="user_controller"),
    path("/tasks", views.tasks_controller, name="tasks_controller"),
    path("/task/<int:task_id>", views.task_controller, name="task_controller"),
    path("/task/<int:task_id>/<str:action>", views.task_controller, name="task_controller")
]