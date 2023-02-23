from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import SignupForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username',)


class AppCustomSignupForm(SignupForm):
    
    first_name = forms.CharField(max_length=25, label='First Name')
    last_name = forms.CharField(max_length=25, label='Last Name')

    field_order = ["first_name", "last_name", "email", "password1", "password2"]

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user