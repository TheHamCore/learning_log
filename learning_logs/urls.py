"""Определяет схемы URL для learning_logs"""

from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
    # домашняя страница
    path('', views.index, name='index'),
    # страница со списком всех тем
    path('topics/', views.topics, name='topics'),
    # страница с подробной информацией по отдельной теме
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # страница для добавления новой темы
    path('new_topic/', views.new_topic, name='new_topic'),
    # страница для добавления новой записи
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),  # id = число, равное идентификатору темы
    # страница для редактирования записи
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]
