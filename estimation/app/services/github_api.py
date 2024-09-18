import requests

from ..models import GithubIssue, GithubUser


class GithubApi:

    user_handle = None

    def __init__(self, user_handle):
        self.user_handle = user_handle

    def get_issue(self, org, repo, issue_number):
        github_user = GithubUser.objects.get(pk=self.user_handle)

        issue_api_url = (
            f"https://api.github.com/repos/{org}/{repo}/issues/{issue_number}"
        )
        headers = {
            "Authorization": f"Bearer {github_user.access_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        response = requests.get(issue_api_url, headers=headers)
        title = response.json().get("title")

        return GithubIssue(org=org, repo=repo, issue_id=issue_number, title=title)
