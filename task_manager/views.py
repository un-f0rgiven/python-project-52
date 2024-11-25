from django.shortcuts import render
from django.utils import translation
from django.http import HttpResponse


def dashboard_view(request):
    user_language = 'ru'
    translation.activate(user_language)
    request.LANGUAGE_CODE = user_language

    return render(request, 'task_manager/dashboard.html')


def index(request):
    # a = None
    # a.hello() # Creating an error with an invalid line of code
    return HttpResponse("Hello, world. You're at the pollapp index.")


