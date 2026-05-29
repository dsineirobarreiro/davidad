from collections import defaultdict

from calendar_app.models import (
    EthicalProfile,
    ChoiceEthicalProfile,
    SingleChoiceAnswer
)


def calculate_user_ethical_profile(user):

    profile_matches = defaultdict(int)

    answers = SingleChoiceAnswer.objects.filter(
        answer__user=user
    ).select_related(
        "choice"
    )

    # =====================
    # CONTAR MATCHES
    # =====================

    for answer in answers:

        relations = ChoiceEthicalProfile.objects.filter(
            choice=answer.choice
        ).select_related("profile")

        for relation in relations:

            profile_matches[
                relation.profile.id
            ] += 1

    # =====================
    # NORMALIZAR
    # =====================

    result = []

    profiles = EthicalProfile.objects.all()

    for profile in profiles:

        count = profile_matches.get(profile.id, 0)

        percentage = (
            count / profile.total_questions
        ) * 100

        result.append({

            "profile": profile.name,

            "matches": count,

            "total_questions": profile.total_questions,

            "score": round(percentage, 2)
        })

    result.sort(
        key=lambda x: x["profile"]
    )

    return result