from ..models import GithubIssue
from ..view_models.base_view_model import BaseViewModel


class ConfirmIssueViewModel(BaseViewModel):
    issue: GithubIssue
    issue_url: str
