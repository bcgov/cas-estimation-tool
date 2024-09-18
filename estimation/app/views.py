import requests
from django.http import HttpRequest
from django.shortcuts import render, redirect
from app.models import EstimationSession, GithubIssue, GithubUser
from estimation import settings


from estimation.app.view_models.dashboard_view_model import DashboardViewModel
from estimation.app.view_models.index_view_model import IndexViewModel


def index(request: HttpRequest):
    return render(request, "index.html", IndexViewModel())


def dashboard(request):
    avatar_url = request.session.get("avatar_url")
    github_handle = request.session.get("github_handle")

    # Clear session variables if necessary
    request.session.pop("avatar_url", None)
    request.session.pop("github_handle", None)

    sample_estimation_sessions = [
        EstimationSession(
            issue=GithubIssue(org="bcgov", repo="cas-estimation-tool", issue_id=1),
            is_open=True,
        ),
        EstimationSession(
            issue=GithubIssue(org="bcgov", repo="cas-estimation-tool", issue_id=155),
            is_open=True,
        ),
        EstimationSession(
            issue=GithubIssue(org="bcgov", repo="cas-estimation-tool", issue_id=65554),
            is_open=False,
        ),
    ]

    return render(
        request,
        "dashboard.html",
        DashboardViewModel(
            estimation_sessions=sample_estimation_sessions,
            user=GithubUser(handle=github_handle, avatar_url=avatar_url),
        ),
    )


def github_login(request):
    # GitHub OAuth authorization URL
    github_auth_url = (
        "https://github.com/login/oauth/authorize?"
        f"client_id={settings.GITHUB_CLIENT_ID}&"
        f"redirect_uri={settings.GITHUB_REDIRECT_URI}&"
        "scope=repo"
    )
    return redirect(github_auth_url)


def github_callback(request):
    code = request.GET.get("code")
    if not code:
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
            handle=github_handle, defaults={"access_token": access_token}
        )

        if not created:
            # If the user already exists, update the access token
            github_user.access_token = access_token
            github_user.avatar_url = avatar_url
            github_user.save()

    print(user_info)  # Optional: You can log user info for debugging

    # Example values for demonstration purposes
    project_url = "https://github.com/users/ayeshmcg/projects/1"
    issue_url = "https://github.com/ayeshmcg/testRepo/issues/1"
    story_points = 5

    result = update_story_points_for_issue_card(
        project_url, issue_url, story_points, access_token
    )
    print(result)  # Log the result for debugging
    request.session["avatar_url"] = avatar_url
    request.session["github_handle"] = github_handle

    return redirect("dashboard")


def update_story_points_for_issue_card(
    project_url, issue_url, story_points, access_token
):
    # Extract project ID from the URL
    # project_match = re.match(r'https://github.com/orgs/[^/]+/projects/(\d+)', project_url)
    # if not project_match:
    #     return {'error': 'Invalid project URL format'}
    #
    # project_id = project_match.group(1)

    # Extract issue number from the URL
    # issue_match = re.match(r'https://github.com/[^/]+/[^/]+/issues/(\d+)', issue_url)
    # if not issue_match:
    #     return {'error': 'Invalid issue URL format'}
    #
    # issue_number = issue_match.group(1)

    # Retrieve the project columns
    columns_url = f"https://api.github.com/projects/1/columns"
    headers = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github+json",
    }
    columns_response = requests.get(columns_url, headers=headers)
    if columns_response.status_code != 200:
        return {
            "error": f"Unable to retrieve columns: {columns_response.status_code}, {columns_response.text}"
        }

    columns = columns_response.json()

    # Find the card in a column
    card_id = None
    for column in columns:
        cards_url = f'https://api.github.com/projects/columns/{column["id"]}/cards'
        cards_response = requests.get(cards_url, headers=headers)
        if cards_response.status_code != 200:
            return {
                "error": f"Unable to retrieve cards: {cards_response.status_code}, {cards_response.text}"
            }

        cards = cards_response.json()
        for card in cards:
            if card.get("content_url") == issue_url:
                card_id = card["id"]
                break
        if card_id:
            break

    if not card_id:
        return {"error": "No card found for the specified issue URL"}

    # Update the card with Story Points
    card_url = f"https://api.github.com/projects/columns/cards/{card_id}"
    card_response = requests.get(card_url, headers=headers)
    if card_response.status_code != 200:
        return {
            "error": f"Unable to retrieve card details: {card_response.status_code}, {card_response.text}"
        }

    card_data = card_response.json()

    print("card_data", card_data)
    print("story_points", story_points)

    # If the card is a note card, append the story points
    # if 'note' in card_data:
    #     updated_note = f"{card_data['note']}\n\nStory Points: {story_points}"
    #     update_data = {'note': updated_note}
    # else:
    #     return {'error': 'This card is not a note card and cannot be updated'}
    #
    # update_response = requests.patch(card_url, json=update_data, headers=headers)
    # if update_response.status_code == 200:
    #     return {'success': 'Story Points added successfully'}
    # else:
    #     return {'error': f'Failed to add Story Points: {update_response.status_code}'}
