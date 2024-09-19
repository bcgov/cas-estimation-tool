from typing import List
from ..models import GithubIssue, GithubUser
from ..view_models.base_view_model import BaseViewModel


class EstimationSessionViewModel(BaseViewModel):
    issue: GithubIssue
    markdown_description: str
    team_members: List[GithubUser]
