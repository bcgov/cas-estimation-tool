from django.db import models
from django.utils import timezone


class GithubUser(models.Model):
    handle = models.CharField(
        max_length=1000,
        db_comment="The github handle for the user, without the '@github' part.",
        primary_key=True,
    )
    access_token = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_comment="GitHub access token for OAuth authentication.",
    )

    avatar_url = models.URLField(blank=True, null=True)
    token_expires = models.DateTimeField(null=True, blank=True)
    token_created = models.DateTimeField(null=True, blank=True, default=timezone.now)


def __str__(self):
    return self.handle


class GithubIssue(models.Model):
    org = models.CharField(max_length=1000, db_comment="The org this issue belongs to.")
    repo = models.CharField(
        max_length=1000, db_comment="The repository this issue belongs to."
    )
    issue_number = models.IntegerField(db_comment="The issue number.")

    title = models.CharField(
        max_length=1000,
        db_comment="The issue title when fetched from the GH API",
        null=True,
        blank=True,
    )
    body = models.CharField(
        max_length=10000,
        db_comment="The issue body when fetched from the github API, in markdown format",
        null=True,
        blank=True,
    )

    def url(self):
        return f"https://github.com/{self.org}/{self.repo}/issues/{self.issue_number}"


class EstimationSession(models.Model):
    issue = models.ForeignKey(GithubIssue, on_delete=models.CASCADE)
    final_estimate = models.IntegerField(null=True, blank=True)
    is_open = models.BooleanField(default=True)


class Vote(models.Model):
    user = models.ForeignKey(GithubUser, on_delete=models.CASCADE, related_name="votes")
    estimation_session = models.ForeignKey(
        EstimationSession, on_delete=models.CASCADE, related_name="votes"
    )
    vote = models.IntegerField(null=True, blank=True, db_comment="The voted estimate.")
