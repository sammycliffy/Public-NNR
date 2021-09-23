from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class SignUpForm(UserCreationForm):
    companyName = forms.CharField(
        max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    companyAddress = forms.CharField(
        max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contactPerson = forms.CharField(
        max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control', }))
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = None

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['companyName'].label = "Company Name"
        self.fields['companyAddress'].label = "Company Address"
        self.fields['contactPerson'].label = "Contact Person"

    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This Email address is already in use.')

    class Meta:
        model = User
        fields = ('companyName', 'companyAddress',
                  'contactPerson', 'phone', 'email', 'password1', )


class LoginForm(AuthenticationForm):
    email = forms.CharField(label=("Email"), max_length=30,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# class ProfileForm(forms.ModelForm):
#     phone = forms.CharField(max_length=254,widget=forms.TextInput(attrs={'class':'form-control'}))

#     class Meta:
#         model = Profile
#         fields = ("phone")


class RadioActiveSourcesForm(forms.ModelForm):
    sourceCategory = forms.CharField(
        max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sourceName = forms.CharField(
        max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sourceState = forms.CharField(
        max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sourceAddress = forms.CharField(
        max_length=254, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(RadioActiveSourcesForm, self).__init__(*args, **kwargs)
        self.fields['sourceCategory'].label = "Source Category"
        self.fields['sourceName'].label = "Name of Source"
        self.fields['sourceState'].label = "State of Source"
        self.fields['sourceAddress'].label = "Source Address"

    class Meta:
        model = RadioActiveSourcesModel
        fields = ('sourceCategory', 'sourceName',
                  'sourceState', 'sourceAddress')
