from django.http import HttpResponse
from django.shortcuts import render


def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World </h1>")
    return render(request, "pages/home.html", {})


def contact_view(request, *args, **kwargs):
    return render(request, "pages/contact.html", {})
