from django.http import HttpRequest
from django.shortcuts import render
import markdown

from ..view_models.estimation_session_view_model import EstimationSessionViewModel
from ..services.github_api import GithubApi


def estimation_session(request: HttpRequest):

    gh_api = GithubApi(request.session.get("github_handle"))
    team_members = gh_api.get_team_members("bcgov", "cas")

    issue = gh_api.get_issue("bcgov", "cas-reporting", 346)

    view_model = EstimationSessionViewModel(
        issue=issue,
        team_members=team_members,
        markdown_description=markdown.markdown(issue.body),
    )

    return render(request, "estimation_session.html", view_model)
