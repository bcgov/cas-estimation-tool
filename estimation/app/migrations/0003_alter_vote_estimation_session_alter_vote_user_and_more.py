# Generated by Django 5.1.1 on 2024-09-19 01:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_rename_issue_id_githubissue_issue_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vote",
            name="estimation_session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="votes",
                to="app.estimationsession",
            ),
        ),
        migrations.AlterField(
            model_name="vote",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="votes",
                to="app.githubuser",
            ),
        ),
        migrations.AlterField(
            model_name="vote",
            name="vote",
            field=models.IntegerField(
                blank=True, db_comment="The voted estimate.", null=True
            ),
        ),
    ]