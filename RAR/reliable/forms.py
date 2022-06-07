from django import forms
from .models import service_call
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, ButtonHolder

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
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
                Field('fname', placeholder="First Name"),
                Field('lname', placeholder="Last Name"),
                Field('phone', placeholder="Phone Number"),
                Field('address', placeholder="Address"),
                Field('details', placeholder="Describe the problem", cols="5"),
                ButtonHolder(
                    Submit('submit', "Submit"),
                    )
                )
