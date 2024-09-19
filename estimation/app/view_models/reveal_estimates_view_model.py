from typing import List
from ..models import GithubIssue, Vote
from ..view_models.base_view_model import BaseViewModel


class RevealEstimatesViewModel(BaseViewModel):
    session_id: int
    issue: GithubIssue
    issue_url: str
    votes: List[Vote]
    estimate_options: List[int]
