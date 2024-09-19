from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect, render

from ..models import EstimationSession, GithubIssue
from ..view_models.confirm_issue_view_model import ConfirmIssueViewModel


def confirm_issue(request: HttpRequest, issue_id: int):
    issue = GithubIssue.objects.get(id=issue_id)

    if request.method == "POST":
        # Here we'll create the database stuff

        return HttpResponseRedirect("estimation_session")

    return render(
        request,
        "confirm_issue.html",
        ConfirmIssueViewModel(issue=issue, issue_url=issue.url()),
    )


def start_estimation_session(request: HttpRequest, issue_id: int):
    if request.method != "POST":
        raise Exception("This endpoint only accepts POST requests")

    issue = GithubIssue.objects.get(id=issue_id)

    # Create the estimation session
    estimation_session = EstimationSession(issue=issue)
    estimation_session.save()

    # Redirect to the estimation session with the allow_estimation parameter
    return redirect("estimation_session", session_id=estimation_session.id)


