from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

class LoginForm(AuthenticationForm):
    
    class Meta:
        model = User
        fields = ("username", "password1")

    def login(self):
        user = super(LoginForm, self)
        user.username = self.cleaned_data['username']
        user.password = self.cleaned_data['password1']
        return user = authenticate(user.username, user.password)
