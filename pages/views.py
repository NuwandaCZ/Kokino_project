from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from Forms.forms import CreateUserForm, ToiletForm
from toilet.models import Toilet
from django.contrib.auth.decorators import login_required


# @login_required(login_url='login') == nejses loglej, tak te to redirectne na url v uvozovkach
def home_view(request, *args, **kwargs):
    context = {}
    best_toilets = Toilet.objects.order_by('-rating')[:5]  # -rating = descending order_by; :5 = first five
    context['best_toilets'] = best_toilets

    return render(request, "pages/home.html", context)


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
            messages.info(request, 'Username or password is incorrect')
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


@login_required(login_url='login')
def create_toilet_view(request, *args, **kwargs):
    form = ToiletForm()
    if request.method == "POST":
        form = ToiletForm(request.POST)
        if form.is_valid():
            form.save()
            # count rating from all 4 attributes of toilet
            toilet = Toilet.objects.all().order_by("-id")[0]
            toilet.rating = (toilet.design + toilet.space + toilet.tidiness + toilet.smell)/4  # avg
            toilet.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'pages/create_toilet_form.html', context)
