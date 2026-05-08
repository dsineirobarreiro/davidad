from django.utils import timezone

from calendar_app.models import *


ORDER_WEIGHTS = [3, 2, 1, 0]


def get_current_max_score():

    today_day = timezone.now().day

    questions = Question.objects.filter(
        day__lte=today_day
    )

    max_score = 0

    for question in questions:

        if question.question_type == "MULTI":
            max_score += 3

        elif question.question_type == "ORDER":
            max_score += 6

    return max_score

def calculate_match(user_a, user_b):

    total_score = 0

    answers_a = {
        a.question_id: a
        for a in Answer.objects.filter(user=user_a)
    }

    answers_b = {
        a.question_id: a
        for a in Answer.objects.filter(user=user_b)
    }

    today_day = timezone.now().day

    questions = Question.objects.filter(
        day__lte=today_day
    )

    for question in questions:

        answer_a = answers_a.get(question.id)
        answer_b = answers_b.get(question.id)

        # si alguno no respondió:
        # simplemente 0 puntos
        if not answer_a or not answer_b:
            continue

        # =====================
        # MULTI
        # =====================

        if question.question_type == "MULTI":

            choice_a = SingleChoiceAnswer.objects.get(
                answer=answer_a
            ).choice_id

            choice_b = SingleChoiceAnswer.objects.get(
                answer=answer_b
            ).choice_id

            if choice_a == choice_b:
                total_score += 3

        # =====================
        # ORDER
        # =====================

        elif question.question_type == "ORDER":

            items_a = list(
                OrderAnswerItem.objects.filter(
                    order_answer__answer=answer_a
                ).order_by("position")
            )

            items_b = list(
                OrderAnswerItem.objects.filter(
                    order_answer__answer=answer_b
                ).order_by("position")
            )

            for i in range(4):

                if items_a[i].choice_id == items_b[i].choice_id:
                    total_score += ORDER_WEIGHTS[i]

    max_score = get_current_max_score()

    percentage = (
        round((total_score / max_score) * 100, 1)
        if max_score > 0 else 0
    )

    return {

        "score": total_score,

        "max_score": max_score,

        "percentage": percentage
    }

def recalculate_matches_for_user(user):

    users = User.objects.exclude(id=user.id)

    for other_user in users:

        user_a = user
        user_b = other_user

        # evitar duplicados
        if user_a.id > user_b.id:
            user_a, user_b = user_b, user_a

        result = calculate_match(
            user_a,
            user_b
        )

        UserMatch.objects.update_or_create(

            user_a=user_a,
            user_b=user_b,

            defaults={

                "score": result["score"],

                "max_score": result["max_score"],

                "percentage": result["percentage"]
            }
        )