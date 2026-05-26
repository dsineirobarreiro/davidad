from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/register/', views.register, name='register'),
    path('question/<int:question_id>/', views.answer_question, name='answer_question'),
    path('matches/', views.matches_page, name='matches'),

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

    path(
        "api/user-ethical-profile/<int:user_id>/",
        views.user_ethical_profile_api,
        name="user_ethical_profile_api"
    ),

    path(
        "api/check-match-guesses/",
        views.check_match_guesses_api,
        name="check_match_guesses_api"
    ),

    path(
        "api/save-match-guess/",
        views.save_match_guess_api,
        name="save_match_guess_api"
    ),
]