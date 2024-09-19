from django.http import HttpRequest
from django.shortcuts import redirect, render
import markdown

from ..models import EstimationSession, GithubUser, Vote

from ..view_models.estimation_session_view_model import EstimationSessionViewModel
from ..services.github_api import GithubApi


def estimation_session(request: HttpRequest, session_id: int):
    logged_in_handle = request.session.get("github_handle")

    gh_api = GithubApi(logged_in_handle)
    team_members = gh_api.get_team_members("bcgov", "cas")

    estimation_session = EstimationSession.objects.get(id=session_id)

    votes = list(estimation_session.votes.all())
    votes.sort(key=lambda v: v.user.handle.lower())

    team_members = list(set(team_members) - set([v.user for v in votes]))
    team_members.sort(key=lambda u: u.handle.lower())

    current_vote = (
        Vote.objects.filter(
            estimation_session__id=session_id,
            user__handle=logged_in_handle,
        )
        .values("vote")
        .first()
    )
    print(current_vote)

    view_model = EstimationSessionViewModel(
        issue=estimation_session.issue,
        team_members=team_members,
        markdown_description=markdown.markdown(estimation_session.issue.body),
        votes=votes,
        allow_estimation=any(v.user.handle == logged_in_handle for v in votes),
        estimate_options=[1, 2, 3, 5, 8],
        current_vote=None if current_vote is None else current_vote["vote"],
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


def toggle_vote(request, session_id: int, vote: int):
    logged_in_handle = request.session.get("github_handle")

    if not logged_in_handle:
        raise Exception("User must be logged in")

    vote_model = Vote.objects.get(
        estimation_session__id=session_id, user__handle=logged_in_handle
    )

    if vote_model.vote == vote:
        vote_model.vote = None
    else:
        vote_model.vote = vote

    vote_model.save()
    return redirect("estimation_session", session_id=session_id)
