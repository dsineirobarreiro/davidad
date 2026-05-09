from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/register/', views.register, name='register'),
    path('question/<int:question_id>/', views.answer_question, name='answer_question'),

    path('stats/', views.stats_page, name='stats'),

    path(
        'api/question-stats/<int:day>/',
        views.question_stats_api,
        name='question_stats_api'
    ),

    path(
        'api/user-question/<int:user_id>/<int:question_id>/',
        views.user_question_api,
        name='user_question_api'
    ),

    path(
        "api/compatibility-timeline/<int:user1_id>/<int:user2_id>/",
        views.compatibility_timeline_api,
        name="compatibility_timeline_api"
    ),

    path(
        'api/user-matches/<int:user_id>/',
        views.user_matches_api,
        name='user_matches_api'
    ),
]