from django.http import HttpRequest, HttpResponseRedirect
from django.contrib import messages


def logout(request: HttpRequest):
    if request.method == "POST":
        messages.add_message(request, messages.INFO, "You have been logged out!")

        request.session.pop("github_handle")
        request.session.pop("avatar_url")

    return HttpResponseRedirect("/")
