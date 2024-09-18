from typing import TypedDict

from ..models import GithubUser


class BaseViewModel(TypedDict):
    user: GithubUser
