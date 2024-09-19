import secrets
import requests
from django.utils import timezone
from datetime import timedelta
from django.http import HttpRequest
from django.shortcuts import render, redirect
from estimation import settings

from ..services.github_api import GithubApi
from django.shortcuts import render, get_object_or_404

from ..models import EstimationSession, GithubIssue, GithubUser, Vote
from ..view_models.dashboard_view_model import DashboardViewModel
from ..view_models.index_view_model import IndexViewModel


def index(request: HttpRequest):
    github_handle = request.session.get("github_handle")
    print("github_handle from session:", github_handle)

    if github_handle:
        github_user = GithubUser.objects.filter(handle=github_handle).first()

        if github_user:
            print("Found GithubUser:", github_user)
            print("Access Token:", github_user.access_token)
            print("Token Expiration:", github_user.token_expires)

            if (
                github_user.access_token
                and github_user.token_expires
                and github_user.token_expires > timezone.now()
            ):
                print("Token is still valid")
                request.session["avatar_url"] = github_user.avatar_url
                return redirect("dashboard")
            else:
                print("Token is expired or missing")
        else:
            print("GithubUser with handle does not exist")

    # Render the index page if not redirected
    return render(request, "index.html", IndexViewModel())


def dashboard(request):
    # Get user information from the session
    avatar_url = request.session.get("avatar_url")
    github_handle = request.session.get("github_handle")

    estimation_sessions = []

    if github_handle:
        user = get_object_or_404(GithubUser, handle=github_handle)

        votes = Vote.objects.filter(user=user)

        estimation_session_ids = votes.values_list('estimation_session_id', flat=True)

        if estimation_session_ids:
            estimation_sessions_queryset = (
                EstimationSession.objects
                .filter(id__in=estimation_session_ids)
                .select_related('issue')
            )

            # Form the estimation sessions list
            for session in estimation_sessions_queryset:
                estimation_sessions.append(EstimationSession(
                    issue=session.issue,
                    is_open=session.is_open,
                    final_estimate=session.final_estimate
                ))
    return render(
        request,
        "dashboard.html",
        DashboardViewModel(
            estimation_sessions=estimation_sessions,
            user=GithubUser(handle=github_handle, avatar_url=avatar_url),
        ),
    )


def github_login(request: HttpRequest):
    request.session["state"] = secrets.token_urlsafe(16)

    # GitHub OAuth authorization URL
    github_auth_url = (
        "https://github.com/login/oauth/authorize?"
        f"client_id={settings.GITHUB_CLIENT_ID}&"
        f"redirect_uri={settings.GITHUB_REDIRECT_URI}&"
        f"state={request.session['state']}&"
        "scope=repo"
    )

    return redirect(github_auth_url)


def github_callback(request: HttpRequest):
    code = request.GET.get("code")
    state = request.GET.get("state")
    if not code or state != request.session["state"]:
        print("No code or state mismatch!")
        return redirect("index")  # Redirect to the main page if no code is present

    # Exchange the authorization code for an access token
    token_url = "https://github.com/login/oauth/access_token"
    payload = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.GITHUB_REDIRECT_URI,
    }
    headers = {"Accept": "application/json"}

    response = requests.post(token_url, data=payload, headers=headers)
    response_data = response.json()

    access_token = response_data.get("access_token")
    if not access_token:
        return redirect("index")  # Handle the case where token is not retrieved

    # Get user information from GitHub
    user_info_url = "https://api.github.com/user"
    headers = {"Authorization": f"token {access_token}"}
    user_info_response = requests.get(user_info_url, headers=headers)
    user_info = user_info_response.json()

    github_handle = user_info.get("login")
    avatar_url = user_info.get("avatar_url")

    if github_handle:
        # Check if the user already exists in the database
        github_user, created = GithubUser.objects.get_or_create(
            handle=github_handle,
            defaults={"access_token": access_token, "avatar_url": avatar_url},
        )

        if not created:
            # If the user already exists, check if the token is expired
            if github_user.token_expires and github_user.token_expires > timezone.now():
                # Token is still valid, redirect to dashboard
                request.session["avatar_url"] = github_user.avatar_url
                request.session["github_handle"] = github_handle
                return redirect("dashboard")

            # Update the access token and token information
            github_user.access_token = access_token
            github_user.avatar_url = avatar_url
            github_user.token_created = timezone.now()
            github_user.token_expires = github_user.token_created + timedelta(hours=1)
            github_user.save()

    request.session["avatar_url"] = avatar_url
    request.session["github_handle"] = github_handle

    print(request.session)

    return redirect("dashboard")
