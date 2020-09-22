from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse

from Forms.forms import CreateUserForm, ToiletForm, RatingForm
from toilet.models import Toilet
from rating.models import Rating
from django.contrib.auth.models import User
from django.db.models import Avg

from django.contrib.auth.decorators import login_required


def home_view(request, *args, **kwargs):
    context = {}
    best_toilets = Toilet.objects.order_by('-overal_rating')[:5]
    is_rated = {}
    if request.user.is_authenticated:
        for i in range(len(best_toilets)):
            try:
                rating = Rating.objects.get(user=request.user, toilet_id=best_toilets[i])
                is_rated[best_toilets[i].id] = rating
            except Rating.DoesNotExist:
                pass

    context['is_rated'] = is_rated
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

            current_user = request.user
            upk = current_user.id
            current_toilet = Toilet.objects.latest('id')
            tpk = current_toilet.id
            return HttpResponseRedirect(reverse("rate_toilet", args=[upk, tpk]))

    context = {'form': form}
    return render(request, 'pages/create_toilet_form.html', context)


@login_required(login_url='login')
def rate_toilet_view(request, upk, tpk, *args, **kwargs):

    toilet  = Toilet.objects.get(id=tpk)
    user    = User.objects.get(id=upk)

    needs_creation = False
    try:
        rating = Rating.objects.get(user_id=upk, toilet_id=tpk)
    except Rating.DoesNotExist:
        needs_creation = True
        pass
    finally:
        if needs_creation:
            rating = Rating.objects.create(toilet_id=tpk, user_id=upk)

    form = RatingForm(instance=rating)

    if request.method == "POST":
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            rating.rating = (rating.tidiness + rating.smell + rating.design + rating.space)/4
            rating.save()

            toilet = Toilet.objects.get(id=tpk)
            relevant_ratings = Rating.objects.filter(toilet_id=tpk)

            smell       = relevant_ratings.aggregate(Avg('smell'))
            design      = relevant_ratings.aggregate(Avg('design'))
            space       = relevant_ratings.aggregate(Avg('space'))
            tidiness    = relevant_ratings.aggregate(Avg('tidiness'))

            toilet.overal_smell     = smell['smell__avg']
            toilet.overal_design    = design['design__avg']
            toilet.overal_space     = space['space__avg']
            toilet.overal_tidiness  = tidiness['tidiness__avg']

            toilet.overal_rating = (toilet.overal_design + toilet.overal_space + toilet.overal_tidiness
                                    + toilet.overal_smell)/4  # avg
            toilet.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'pages/rate_toilet_form.html', context)
