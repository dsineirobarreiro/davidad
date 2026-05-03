from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.utils import timezone

from .forms import SignUpForm
from .models import Question, Answer
from .utils import get_next_question_for_user
from .services.answer_service import AnswerService

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
    today = (timezone.now().date() - settings.ADVENT_START_DATE).days + 1

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
            return redirect('home')

        except ValidationError as e:
            error = str(e)

    return render(request, 'answer.html', {
        'question': question,
        'error': error
    })