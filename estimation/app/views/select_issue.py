from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib import messages

from ..services.github_api import GithubApi

from ..view_models.confirm_issue_view_model import ConfirmIssueViewModel

from ..view_models.select_issue_view_model import SelectIssueViewModel


def select_issue(request: HttpRequest):

    if request.method == "POST":
        issue_url = request.POST.get("issue_url")
        # Here goes the Github API request

        # Parse the issue:
        # https://github.com/bcgov/cas-airflow/issues/174

        # Sanity check
        try:
            parts = [part for part in issue_url.split("/") if part]
            if parts[-2] != "issues" or "github.com" not in parts[-5]:
                raise Exception()

            issue_number = parts[-1]  # Last element
            repo = parts[-3]
            org = parts[-4]

            print(issue_number, repo, org)

        except Exception:
            messages.add_message(
                request, messages.ERROR, "The URL is not a valid GitHub issue URL"
            )
            return render(
                request, "select_issue.html", SelectIssueViewModel(issue_url=issue_url)
            )

        api_client = GithubApi(request.session["github_handle"])

        gh_issue = api_client.get_issue(org, repo, issue_number)
        gh_issue.save()

        return redirect("confirm_issue", issue_id=gh_issue.id)

        return render(
            request,
            "confirm_issue.html",
            ConfirmIssueViewModel(issue=gh_issue, issue_url=issue_url),
        )
    else:
        return render(request, "select_issue.html", SelectIssueViewModel())
