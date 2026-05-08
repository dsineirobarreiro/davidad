from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.http import JsonResponse
from django.utils import timezone

from .forms import SignUpForm
from .models import Question, Answer, SingleChoiceAnswer, UserMatch
from .utils import get_next_question_for_user
from .services.answer_service import AnswerService
from .services.match_service import recalculate_matches_for_user

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # login automático tras registro
            login(request, user)

            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'registration/register.html', {
        'form': form
    })

@login_required
def home(request):
    today = (timezone.localtime().date() - settings.ADVENT_START_DATE).days + 1

    questions = Question.objects.all().order_by('day')
    answered_days = set(
        Answer.objects.filter(user=request.user)
        .values_list('question__day', flat=True)
    )

    calendar_days = []

    for q in questions:
        if q.day > today:
            status = 'locked'
        elif q.day in answered_days:
            status = 'completed'
        else:
            # comprobar si es el siguiente que le toca
            previous_answered = all(
                d in answered_days for d in range(1, q.day)
            )
            status = 'available' if previous_answered else 'blocked'

        calendar_days.append({
            'day': q.day,
            'question_id': q.id,
            'status': status
        })

    return render(request, 'home.html', {
        'calendar_days': calendar_days
    })


@login_required
def answer_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    # 🔒 Validación de flujo
    next_question = get_next_question_for_user(request.user)

    if not next_question or question.id != next_question.id:
        return redirect('home')

    error = None

    if request.method == 'POST':
        try:
            AnswerService.create_answer(
                user=request.user,
                question=question,
                data=request.POST
            )

            print(request.user)
            recalculate_matches_for_user(request.user)

            return redirect('home')

        except ValidationError as e:
            error = str(e)

    return render(request, 'answer.html', {
        'question': question,
        'error': error
    })

@staff_member_required
def stats_page(request):

    return render(request, "stats.html", {
        "users": User.objects.all(),
        "days": range(1, 25)
    })

@staff_member_required
def question_stats_api(request, day):

    question = Question.objects.get(day=day)

    data = []

    total_answers = Answer.objects.filter(
        question=question
    ).count()

    # MULTI
    if question.question_type == "MULTI":

        for choice in question.choices.all():

            count = SingleChoiceAnswer.objects.filter(
                answer__question=question,
                choice=choice
            ).count()

            data.append({
                "label": choice.text,
                "count": count,
                "percentage": (
                    round((count / total_answers) * 100, 1)
                    if total_answers > 0 else 0
                )
            })

    return JsonResponse({
        "question": question.text,
        "type": question.question_type,
        "data": data
    })

@staff_member_required
def user_matches_api(request, user_id):

    user = User.objects.get(id=user_id)

    matches = []

    user_matches = UserMatch.objects.filter(
        models.Q(user_a=user) |
        models.Q(user_b=user)
    )

    for match in user_matches:

        other_user = (
            match.user_b
            if match.user_a == user
            else match.user_a
        )

        matches.append({

            "username": other_user.username,

            "score": match.score,

            "max_score": match.max_score,

            "percentage": match.percentage
        })

    matches.sort(
        key=lambda x: x["percentage"],
        reverse=True
    )

    return JsonResponse({
        "matches": matches
    })