from django import forms
from .models import service_call
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, ButtonHolder

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
                user.save()
        return user

class RequestForm(forms.ModelForm):

    class Meta:
        model = service_call
        fields = ( "fname", "lname", "phone", "address", "details")

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                Field('fname', label="First Name"),
                Field('lname', label="Last Name"),
                Field('phone', label="Phone Number"),
                Field('address', placeholder="Address"),
                Field('details', cols="5", label="Describe the problem"),
                ButtonHolder(
                    Submit('submit', "Submit"),
                    )
                )
