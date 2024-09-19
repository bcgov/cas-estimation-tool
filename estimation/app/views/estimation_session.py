from django.http import HttpRequest
from django.shortcuts import redirect, render
import markdown

from ..models import EstimationSession, GithubUser, Vote

from ..view_models.estimation_session_view_model import EstimationSessionViewModel
from ..services.github_api import GithubApi


def estimation_session(request: HttpRequest, session_id: int):

    gh_api = GithubApi(request.session.get("github_handle"))
    team_members = gh_api.get_team_members("bcgov", "cas")

    estimation_session = EstimationSession.objects.get(id=session_id)

    votes = list(estimation_session.votes.all())
    votes.sort(key=lambda v: v.user.handle.lower())

    team_members = list(set(team_members) - set([v.user for v in votes]))
    team_members.sort(key=lambda u: u.handle.lower())

    view_model = EstimationSessionViewModel(
        issue=estimation_session.issue,
        team_members=team_members,
        markdown_description=markdown.markdown(estimation_session.issue.body),
        votes=votes,
    )

    return render(request, "estimation_session.html", view_model)


def add_member(request, session_id: int, handle: str):
    estimation_session = EstimationSession.objects.get(id=session_id)

    voter, _ = GithubUser.objects.get_or_create(handle=handle)

    vote = Vote(user=voter, estimation_session=estimation_session)
    vote.save()

    return redirect("estimation_session", session_id=session_id)


def remove_member(request, session_id: int, handle: str):
    vote = Vote.objects.get(estimation_session__id=session_id, user__handle=handle)
    vote.delete()

    return redirect("estimation_session", session_id=session_id)
