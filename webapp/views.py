from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import *
from django.urls import reverse 
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegisterForm

# Create your views here.
def index(request):
    context = {
        "flights" : Flight.objects.all()
    }

    return render(request, "webapp/home.html", context)

def flight(request, flight_id):
    try:
        flight = Flight.objects.get(pk=flight_id)

    except Flight.DoesNotExist:
        raise Http404("Flight does not exist.")
    context = {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
    }
    return render(request, "webapp/flight.html", context)

def book(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=passenger_id)
    except KeyError:
        return render(request, "flights/error.html", {"message": "No selection."})
    except Flight.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No flight."})
    except Passenger.DoesNotExist:
        return render(request, "flights/error.html", {"message": "No passenger."})
    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("webapp:flight", args=(flight_id,)))

def cancle(request, flight_id):
    try:
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        passenger.delete()
    except Passenger.DoesNotExist:
        return render(request, "error.html", {"messege": "No passenger."})
    except Flight.DoesNotExist:
        return render(request, "error.html", {"messege": "No flight."})
    except KeyError:
        return render(request, "error.html", {"messege": "No selection."})
    return HttpResponseRedirect(reverse("webapp:flight", args=(flight_id,)))

def login_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("webapp:index"))
    else:
        return render(request, "webapp/login.html", {"message": "Invalid credentials."})

def logout_view(request):
    logout(request)
    return render(request, "webapp/login.html", {"message": "Logged out."})

def signup_view(request):
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }
    return render(request, "webapp/signup.html", context)