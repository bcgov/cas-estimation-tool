from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("github/login/", views.github_login, name="github_login"),
    path("github/callback/", views.github_callback, name="github_callback"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout", views.logout, name="logout"),
    path("select_issue", views.select_issue, name="select_issue"),
    path("confirm_issue/<int:issue_id>/", views.confirm_issue, name="confirm_issue"),
    path(
        "start_estimation_session/<int:issue_id>/",
        views.start_estimation_session,
        name="start_estimation_session",
    ),
    path(
        "estimation_session/<int:session_id>/",
        views.estimation_session,
        name="estimation_session",
    ),
    path(
        "estimation_session/<int:session_id>/add_member/<str:handle>/",
        views.add_member,
        name="estimation_session",
    ),
    path(
        "estimation_session/<int:session_id>/remove_member/<str:handle>/",
        views.remove_member,
        name="estimation_session",
    ),
    path(
        "estimation_session/<int:session_id>/toggle_vote/<int:vote>/",
        views.toggle_vote,
        name="estimation_session",
    ),
]
