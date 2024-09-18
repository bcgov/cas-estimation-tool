from django.http import HttpRequest, HttpResponseRedirect


def logout(request: HttpRequest):
    if request.method == "POST":
        request.session.pop("github_handle")
        request.session.pop("avatar_url")

    return HttpResponseRedirect("/")
