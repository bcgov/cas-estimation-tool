from django.http import HttpRequest


def logout(request: HttpRequest):
    return "Logged out!"
