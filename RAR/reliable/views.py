from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .forms import NewUserForm, RequestForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .models import service
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, 'reliable/index.html')

def pricing(request):
    return render(request, 'reliable/pricing.html')

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registation successful.")
            return redirect("index")
        messages.error(request, "Registration unsuccessful, please check your information and try again.")
    form = NewUserForm()
    return render(request=request, template_name="reliable/create.html", context={"register_form":form})

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
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'reliable/login.html', {'form': form})

def logout(request):
    logout(request)
    message.info(request, "You have successfully logged out. Goodbye.")
    return redirect("index")

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
                    message.success(request, "A message with reset password instructions has been sent to your inbox.")
                    return redirect("password_reset/done")
                message.error(request, "An invalid email has been entered.")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="reliable/password_reset.html", context={"password_reset_form":password_reset_form})

def user_dashboard(request):
    return render(request, 'reliable/user.html')

def service(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            if request.user is not None:
                username = request.user.username
            else:
                username = "Anonymous"
            fname = form.cleaned_data.get('fname')
            lname = form.cleaned_data.get('lname')
            phone = form.cleaned_data.get('phone')
            address = form.cleaned_data.get('address')
            details = form.cleaned_data.get('details')
            now = datetime.now()
            timemade = now.strftime("%m/%d/%Y %H%M%S")
            try:
                service_call.save(username, fname, lname, phone, address, details, timemade)
            except:
                return HttpResponse('Invalid Service Call Request. Please hit back and try again. Or call (469) 592-1148')
            message.info(request, "Service call has been submitted and a text has been sent to the Technician on-duty. We should be contacting you by phone shortly.")
            return redirect('index')
    form = RequestForm()
    return render(request, 'reliable/service.html', {"form":form})
