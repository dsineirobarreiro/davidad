from django.contrib import admin
from .models import Question, Choice, Answer, SingleChoiceAnswer, OrderAnswer, OrderAnswerItem, UserMatch, EthicalProfile, ChoiceEthicalProfile


# =========================
# QUESTION
# =========================

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    list_display = (
        "day",
        "question_type",
        "short_text"
    )

    inlines = [ChoiceInline]

    ordering = ("day",)

    def short_text(self, obj):
        return obj.text[:50]


# =========================
# ANSWER
# =========================

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "question_day",
        "question_text",
        "created_at"
    )

    list_filter = (
        "question__day",
        "question__question_type"
    )

    search_fields = (
        "user__username",
        "question__text"
    )

    def question_day(self, obj):
        return obj.question.day

    question_day.short_description = "Day"

    def question_text(self, obj):
        return obj.question.text[:50]

    question_text.short_description = "Question"


# =========================
# SINGLE CHOICE
# =========================

@admin.register(SingleChoiceAnswer)
class SingleChoiceAnswerAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "day",
        "question",
        "selected_choice"
    )

    list_filter = (
        "answer__question__day",
    )

    search_fields = (
        "answer__user__username",
        "answer__question__text",
        "choice__text"
    )

    ordering = (
        "answer__question__day",
    )

    def user(self, obj):
        return obj.answer.user.username

    def day(self, obj):
        return obj.answer.question.day

    def question(self, obj):
        return obj.answer.question.text[:50]

    def selected_choice(self, obj):
        return obj.choice.text


# =========================
# ORDER ANSWER
# =========================

class OrderAnswerItemInline(admin.TabularInline):
    model = OrderAnswerItem
    extra = 0


@admin.register(OrderAnswer)
class OrderAnswerAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "day",
        "question"
    )

    inlines = [OrderAnswerItemInline]

    def user(self, obj):
        return obj.answer.user.username

    def day(self, obj):
        return obj.answer.question.day

    def question(self, obj):
        return obj.answer.question.text[:50]


# =========================
# USER MATCH
# =========================

@admin.register(UserMatch)
class UserMatchAdmin(admin.ModelAdmin):

    list_display = (
        "user_a",
        "user_b",
        "score",
        "percentage",
        "updated_at"
    )

    search_fields = (
        "user_a__username",
        "user_b__username"
    )

    ordering = (
        "-percentage",
    )

# =====================
# ETHICAL PROFILES
# =====================

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):

    list_display = (
        "text",
        "question"
    )

    search_fields = (
        "text",
    )

    list_filter = (
        "question__day",
    )

@admin.register(EthicalProfile)
class EthicalProfileAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "total_questions"
    )

    search_fields = (
        "name",
    )


@admin.register(ChoiceEthicalProfile)
class ChoiceEthicalProfileAdmin(admin.ModelAdmin):

    list_display = (
        "choice",
        "question_day",
        "profile"
    )

    list_filter = (
        "profile",
    )

    search_fields = (
        "choice__text",
        "profile__name"
    )

    autocomplete_fields = (
        "choice",
        "profile"
    )

    def question_day(self, obj):
        return obj.choice.question.day