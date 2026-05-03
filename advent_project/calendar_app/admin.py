from django.contrib import admin
from .models import Question, Choice, Answer, SingleChoiceAnswer, OrderAnswer, OrderAnswerItem


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class OrderAnswerItemInline(admin.TabularInline):
    model = OrderAnswerItem
    extra = 0

class OrderAnswerAdmin(admin.ModelAdmin):
    inlines = [OrderAnswerItemInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(SingleChoiceAnswer)
admin.site.register(OrderAnswer, OrderAnswerAdmin)