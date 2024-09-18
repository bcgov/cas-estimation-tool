from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render

from ..models import GithubIssue
from ..view_models.confirm_issue_view_model import ConfirmIssueViewModel


def confirm_issue(request: HttpRequest):

    if request.method == "POST":
        # Here we'll create the database stuff
        return HttpResponseRedirect("estimation_session")

    issue = GithubIssue(org="bcgov", repo="repo", issue_id=12345)
    return render(
        request,
        "confirm_issue.html",
        ConfirmIssueViewModel(issue=issue, issue_url=issue.url()),
    )
