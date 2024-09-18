from django.http import HttpRequest
from django.shortcuts import render


def estimation_session(request: HttpRequest):
    return render(request, "estimation_session.html", {})
