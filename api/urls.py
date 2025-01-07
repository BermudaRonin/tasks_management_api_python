from django.urls import path
from api import views

urlpatterns = [
    path("/user", views.user_details, name="user_details"),
    path("/user/<str:param>", views.authentication, name="authentication"),
    path("/task/<int:id>", views.task_details, name="task_details"),
    path("/task/<int:id>/<str:param>", views.task_details, name="task_details"),
    path("/tasks", views.tasks_list, name="tasks_list"),
]
