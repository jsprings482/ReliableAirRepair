from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NewUserForm, RequestForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import service_call
from datetime import datetime
import os, requests, json
from django.urls import reverse

# Create your views here.
def index(request):
   return render(request, 'reliable/index.html')

def pricing(request):
    return render(request, 'reliable/pricing.html')

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            passw=form.cleaned_data.get('password1')
            auser = User(username = uname, email = email, password = passw)
            auser.save()
            login(request, auser)
            message = "Registration successful."
            return render(request, "reliable/index.html", { 'msg' : message })
        message = "Registration unsuccessful, please check your information and try again."
        return render(request, "reliable/register.html", { 'msg' : message })
    form = NewUserForm()
    return render(request=request, template_name="reliable/register.html", context={"register_form":form})

def logon(request):
    if request.method == "POST":
        form = AuthenticationForm(None, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                message = f"You are now logged in as [ {username} ]."
                return render(request, "reliable/index.html", { 'msg' : message })
            else:
                message =  "Invalid username or password."
                return render(request, "reliable/login.html", { 'msg' : message })
        else:
            message =  "Invalid username or password."
            return render(request, "reliable/login.html", { 'msg' : message})
    form = AuthenticationForm()
    return render(request, 'reliable/login.html', {'form': form})

def logout(request):
    auth.logout(request)
    message = "You have successfully logged out."
    return render(request, "reliable/index.html", { 'msg' : message})

def user_dashboard(request):
    return render(request, 'reliable/user.html')

def service(request):
    TILL_URL = os.environ.get("TILL_URL")
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            service_call.first_name = form.cleaned_data.get('first_name')
            service_call.last_name = form.cleaned_data.get('last_name')
            service_call.phone = form.cleaned_data.get('phone')
            service_call.address = form.cleaned_data.get('address')
            service_call.details = form.cleaned_data.get('details')
            sc = service_call(first_name = service_call.firstname, last_name = service_call.last_name, phone = service_call.phone, address = service_call.address, details = service_call.details)
            sc.save()
            resp = requests.post(TILL_URL, json={
            "phone": ["14695921148"],
            "method": "SMS",
            "tag" : "alert",
            "text": f'{service_call.phone}: {service_call.first_name} - {service_call.details}',
            })
            message = "A service call has been submitted and a text has been sent to the Technician on duty. We should be contacting you by phone shortly to confirm."
            return render(request, 'reliable/index.html', {'msg' : message })
    form = RequestForm()
    return render(request, 'reliable/service.html', {
        "form": form,
        })
