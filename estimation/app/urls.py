from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("github/login/", views.github_login, name="github_login"),
    path("github/callback/", views.github_callback, name="github_callback"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout", views.logout, name="logout"),
    path("select_issue", views.select_issue, name="select_issue"),
    path("confirm_issue", views.confirm_issue, name="confirm_issue"),
    path("estimation_session", views.estimation_session, name="estimation_session"),
]
