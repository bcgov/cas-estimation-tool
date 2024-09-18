from django.http import HttpRequest
from django.shortcuts import render

from ..models import GithubIssue
from ..view_models.confirm_issue_view_model import ConfirmIssueViewModel

from ..view_models.select_issue_view_model import SelectIssueViewModel


def select_issue(request: HttpRequest):

    if request.method == "POST":
        issue_url = request.POST.get("issue_url")
        # Here goes the Github API request

        gh_issue = GithubIssue(org="bcgov", repo="cas-estimation-tool", issue_id="1234")

        return render(
            request,
            "confirm_issue.html",
            ConfirmIssueViewModel(issue=gh_issue, issue_url=issue_url),
        )
    else:
        return render(request, "select_issue.html", SelectIssueViewModel())
