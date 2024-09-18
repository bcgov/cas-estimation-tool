from typing import List

from ..models import EstimationSession
from ..view_models.base_view_model import BaseViewModel


class DashboardViewModel(BaseViewModel):
    estimation_sessions: List[EstimationSession]
