from typing import List, TypedDict

from ..models import EstimationSession
from ..view_models.base_view_model import BaseViewModel


class EstimationSessionDescription(TypedDict):
    has_voted: bool
    estimation_session: EstimationSession


class DashboardViewModel(BaseViewModel):
    estimation_sessions: List[EstimationSessionDescription]
