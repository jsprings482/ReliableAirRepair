from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NewUserForm, RequestForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .models import service_call
from datetime import datetime
import os, requests, json, uuid
from django.urls import reverse
from flask import Flask, render_template, jsonify, request
from pusher import Pusher

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
            passw=form.cleaned_data.get('password')
            user = User.objects.create_user(uname, email, passw)
            login(request, user)
            messages.success(request, "Registation successful.")
            return HttpResponseRedirect(reverse("reliable:index"), {
            "message": "Registration successful."
                })
        messages.error(request, "Registration unsuccessful, please check your information and try again.")
        return HttpResponseRedirect(reverse("reliable:register"), {
        "message": "Registration unsuccessful, please check your information and try again."
            })
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
                messages.info(request, f"You are now logged in as {username}.")
                return HttpResponseRedirect(reverse("reliable:index"), {
                "message": "You are now logged in as {username}."
                    })
            else:
                messages.error(request, "Invalid username or password.")
                return HttpResponseRedirect(reverse("reliable:logon"), {
                "message": "Invalid username or password."
                    })
        else:
            messages.error(request, "Invalid username or password.")
            return HttpResponseRedirect(reverse("reliable:logon"), {
            "message": "Invalid username or password."
                })
    form = AuthenticationForm()
    return render(request, 'reliable/login.html', {'form': form})

def logout(request):
    auth.logout(request)
    messages.info(request, "You have successfully logged out. Goodbye.")
    return HttpResponseRedirect(reverse("reliable:index"), {
    "message": "You have successfully logged out."
        })

def password_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = 'reliable/password_reset_email.txt'
                    c = {
                            "email": user.email,
                            "domain": 'sandbox8a5127e16fc94bffa137de60a7f181ca.mailgun.org',
                            "site_name": 'reliableairrepair.herokuapp.com',
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "user": user,
                            "token": default_token_generator.make_token(user),
                            "protocol": 'smtp',
                            }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'postmaster@sandbox8a5127e16fc94bffa137de60a7f181ca.mailgun.org', [user.email], fail_silently=False)
                    except:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, "A message with reset password instructions has been sent to your inbox.")
                    return redirect("reliable:password_reset/done")
                messages.error(request, "An invalid email has been entered.")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="reliable/password_reset.html", context={"password_reset_form":password_reset_form})

def user_dashboard(request):
    return render(request, 'reliable/user.html')

def service(request):
    TILL_URL = os.environ.get("TILL_URL")
    PUSHER_URL = os.environ.get("PUSHER_URL")
    PUSHER_URL_CHUNKS = PUSHER_URL.split("http://")[1].split(":")
    PUSHER_KEY = PUSHER_URL_CHUNKS[0]
    PUSHER_SECRET = PUSHER_URL_CHUNKS[1].split("@")[0]
    PUSHER_APP_ID = PUSHER_URL_CHUNKS[1].split("@")[1].split("/")[2]
    app = Flask(__name__)
    pusher = Pusher(app_id=PUSHER_APP_ID, key=PUSHER_KEY, secret=PUSHER_SECRET)
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            service_call.first_name = form.cleaned_data.get('first_name')
            service_call.last_name = form.cleaned_data.get('last_name')
            service_call.phone = form.cleaned_data.get('phone')
            service_call.address = form.cleaned_data.get('address')
            service_call.details = form.cleaned_data.get('details')
            form.save()
            resp = requests.post(TILL_URL, json={
            "phone": ["14695921148"],
            "method": "SMS",
            "text" : f"{service_call.first_name} : {service_call.phone}|{service_call.address}---{service_call.details}",
            "tag": "New Service Call",
            "responses": ["Received", "Ignore"],
            "webhook": "https://reliableairrepair.herokuapp.com",
            })
            messages.info(request, "Service call has been submitted and a text has been sent to the Technician on-duty. We should be contacting you by phone shortly.")
            return HttpResponseRedirect(reverse('reliable:index'), {
            "message": "A service call has been submitted and a text has been sent to the Technician on duty. We should be contacting you by phone shortly."
                })
    form = RequestForm()
    return render(request, 'reliable/service.html', {
        "form": form,
        "uuid": str(uuid.uuid4()),
        "pusher_token": PUSHER_KEY
        })
