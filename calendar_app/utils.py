from django.conf import settings
from django.utils import timezone
from .models import Question, Answer

def get_next_question_for_user(user):
    answered_questions = Answer.objects.filter(user=user).values_list('question__day', flat=True)

    today = (timezone.now().date() - settings.ADVENT_START_DATE).days + 1

    # Buscar la primera pregunta no respondida en orden
    for day in range(1, today + 1):
        if day not in answered_questions:
            return Question.objects.get(day=day)

    return None  # Ya está al día