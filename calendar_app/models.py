from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    class QuestionType(models.TextChoices):
        MULTI = 'MULTI', 'Multiple choice'
        ORDER = 'ORDER', 'Order preferences'

    day = models.PositiveIntegerField(unique=True)
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QuestionType.choices)

    def __str__(self):
        return f"Day {self.day}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')
    
    def __str__(self):
        return f"{self.question.text}"

class SingleChoiceAnswer(models.Model):
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.choice.text}"

class OrderAnswer(models.Model):
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE, related_name='order')

    def __str__(self):
        return f"{self.answer.question.text}"

class OrderAnswerItem(models.Model):
    order_answer = models.ForeignKey(OrderAnswer, on_delete=models.CASCADE, related_name='items')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        unique_together = ('order_answer', 'position')
        ordering = ['position']

class UserMatch(models.Model):

    user_a = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="matches_a"
    )

    user_b = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="matches_b"
    )

    score = models.FloatField()

    max_score = models.FloatField(default=0)

    percentage = models.FloatField(default=0)

    updated_at = models.DateTimeField(auto_now=True)

class UserMatchGuess(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    user_match = models.ForeignKey(
        UserMatch,
        on_delete=models.CASCADE
    )

    guessed_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="received_match_guesses"
    )

    attempts = models.PositiveIntegerField(
        default=0
    )

    is_correct = models.BooleanField(
        null=True,
        blank=True
    )

    is_finished = models.BooleanField(
        default=False
    )

    class Meta:
        unique_together = (
            "user",
            "user_match"
        )

class Gift(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="gifts"
    )

    name = models.CharField(
        max_length=255
    )

    difficulty = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class EthicalProfile(models.Model):

    name = models.CharField(max_length=50)

    total_questions = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class ChoiceEthicalProfile(models.Model):

    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name="ethical_profiles"
    )

    profile = models.ForeignKey(
        EthicalProfile,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("choice", "profile")