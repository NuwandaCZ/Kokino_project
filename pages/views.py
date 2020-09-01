from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from pages.models import CreateUserForm
from django.contrib.auth.decorators import login_required


# @login_required(login_url='login') == nejses loglej, tak te to redirectne na url v uvozovkach
def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1>Hello World </h1>")
    return render(request, "pages/home.html", {})


def contact_view(request, *args, **kwargs):
    return render(request, "pages/contact.html", {})


def login_view(request, *args, **kwargs):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username OR password is incorrect')
            return render(request, "pages/login.html", context)
    return render(request, "pages/login.html", context)


def logout_view(request):
    logout(request)
    return redirect('login')


def signup_view(request, *args, **kwargs):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created' + user)

            return redirect('login')

    context = {'form': form}
    return render(request, "pages/signup.html", context)

