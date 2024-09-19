from django.shortcuts import render
from ..models import EstimationSession
from ..view_models.estimation_session_view_model import (
    EstimationSessionViewModel,
)


def reveal_estimates(request, session_id: int):

    estimation_session = EstimationSession.objects.get(id=session_id)

    view_model = EstimationSessionViewModel(
        session_id=session_id,
        issue=estimation_session.issue,
        issue_url=estimation_session.issue.url(),
        votes=estimation_session.votes.all(),
        estimate_options=[1, 2, 3, 5, 8],
    )

    return render(request, "reveal_estimates.html", view_model)
