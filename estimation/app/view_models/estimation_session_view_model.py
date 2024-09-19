from typing import List
from ..models import GithubIssue, GithubUser, Vote
from ..view_models.base_view_model import BaseViewModel


class EstimationSessionViewModel(BaseViewModel):
    session_id: int
    issue: GithubIssue
    markdown_description: str
    team_members: List[GithubUser]
    votes: List[Vote]
    allow_estimation: bool
    estimate_options: List[int]
    current_vote: int
