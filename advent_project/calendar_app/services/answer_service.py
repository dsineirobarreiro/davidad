from django.core.exceptions import ValidationError

from calendar_app.models import (
    Answer,
    SingleChoiceAnswer,
    OrderAnswer,
    OrderAnswerItem,
    Choice,
)


class AnswerService:

    @staticmethod
    def create_answer(user, question, data):
        """
        data = request.POST
        """
        print(data)

        # Crear Answer base
        answer = Answer.objects.create(
            user=user,
            question=question  # Guardar valor bruto para referencia
        )

        print(user, question, data)

        qtype = question.question_type

        if qtype == 'MULTI':
            AnswerService._handle_multi(answer, question, data)

        elif qtype == 'ORDER':
            AnswerService._handle_order(answer, question, data)

        else:
            raise ValidationError("Unsupported question type")

        return answer

    # -----------------------
    # MULTI
    # -----------------------
    @staticmethod
    def _handle_multi(answer, question, data):
        choice_id = data.get('choice')

        if not choice_id:
            raise ValidationError("Debes seleccionar una opción")

        try:
            choice = Choice.objects.get(
                id=choice_id,
                question=question
            )
        except Choice.DoesNotExist:
            raise ValidationError("Opción inválida")

        SingleChoiceAnswer.objects.create(answer=answer, choice=choice)

    # -----------------------
    # ORDER
    # -----------------------
    @staticmethod
    def _handle_order(answer, question, data):

        raw_order = data.get('order')

        if not raw_order:
            raise ValidationError("No order provided")

        order_ids = raw_order.split(',')

        expected_count = question.choices.count()

        if len(order_ids) != expected_count:
            raise ValidationError("Must include all choices")

        if len(set(order_ids)) != len(order_ids):
            raise ValidationError("Duplicate choices")

        valid_choices = set(
            Choice.objects.filter(
                id__in=order_ids,
                question=question
            ).values_list('id', flat=True)
        )

        if valid_choices != set(map(int, order_ids)):
            raise ValidationError("Invalid choices")

        order_answer = OrderAnswer.objects.create(answer=answer)

        for index, choice_id in enumerate(order_ids):
            OrderAnswerItem.objects.create(
                order_answer=order_answer,
                choice_id=choice_id,
                position=index + 1
            )