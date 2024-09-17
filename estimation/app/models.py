from django.db import models


class GithubUser(models.Model):
    handle = models.CharField(
        max_length=1000,
        db_comment="The github handle for the user, without the '@github' part.",
    )


class GithubIssue(models.Model):
    org = models.CharField(max_length=1000, db_comment="The org this issue belongs to.")
    repo = models.CharField(
        max_length=1000, db_comment="The repository this issue belongs to."
    )
    issue_id = models.IntegerField(db_comment="The issue number.")

    def url(self):
        return f"https://github.com/{self.org}/{self.repo}/issues/{self.issue_id}"


class EstimationSession(models.Model):
    issue = models.ForeignKey(GithubIssue)
    final_estimate = models.IntegerField(null=True, blank=True)
    is_open = models.BooleanField(default=True)


class Vote(models.Model):
    user = models.ForeignKey(GithubUser)
    estimation_session = models.ForeignKey(EstimationSession)
    vote = models.IntegerField(null=True, blank=True)
