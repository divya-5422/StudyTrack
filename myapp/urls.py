from django.urls import path
from .views import task_list, add_task, task_detail, edit_task, delete_task, register, toggle_status, user_login, complete_task, weekly_report, monthly_report
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', task_list, name='task_list'),
    path('add/', add_task, name='add_task'),
    path('task/<int:task_id>/', task_detail, name='task_detail'),
    path('task/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('task/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('task/complete/<int:task_id>/', complete_task, name='complete_task'),
    path('report/weekly/', weekly_report, name='weekly_report'),
    path('report/monthly/', monthly_report, name='monthly_report'),
    path('toggle-status/<int:task_id>/', toggle_status, name='toggle_status'),
]