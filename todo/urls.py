from django.urls import path

from . import views

urlpatterns = [
    path('', views.TodoListView.as_view()),
    path('edit/', views.TodoCreateView.as_view()),
    path('edit/<int:pk>/', views.TodoUpdateView.as_view()),
]
