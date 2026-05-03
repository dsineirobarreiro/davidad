from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/register/', views.register, name='register'),
    path('question/<int:question_id>/', views.answer_question, name='answer_question'),
]