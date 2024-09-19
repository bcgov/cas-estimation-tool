import os
import requests

from ..models import GithubIssue, GithubUser


class GithubApi:

    user_handle = None

    def __init__(self, user_handle):
        if not user_handle:
            print(f"Invalid user handle: {user_handle}")
            raise Exception("Invalid user handle")
        self.user_handle = user_handle

    def get_headers(self):
        github_user = GithubUser.objects.get(pk=self.user_handle)
        return {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def get_issue(self, org, repo, issue_number):

        issue_api_url = (
            f"https://api.github.com/repos/{org}/{repo}/issues/{issue_number}"
        )

        response = requests.get(issue_api_url, headers=self.get_headers())
        issue_data = response.json()

        title = issue_data.get("title")
        body = issue_data.get("body")

        return GithubIssue(
            org=org,
            repo=repo,
            issue_number=issue_number,
            title=title,
            body=body,
        )

    def get_team_members(self, org, team_name):
        # list_team_members_url = (
        #     f"https://api.github.com/orgs/{org}/teams/{team_name}/members"
        # )

        # response = requests.get(list_team_members_url, headers=self.get_headers())
        # member_list = response.json()

        # This is a stopgap to bypass the organization restrictions during the hackathon
        members = os.environ.get("TEAM_MEMBERS").split(",")
        member_list = [GithubUser(handle=member) for member in members]

        return member_list
