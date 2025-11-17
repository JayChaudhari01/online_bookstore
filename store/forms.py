from django import forms
from .models import Book
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()  

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 
                  'address', 'city', 'state', 'pincode', 'age', 'profile_picture')

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 
                  'address', 'city', 'state', 'pincode', 'age', 'profile_picture', 
                  'is_staff', 'is_active')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "description", "price", "isbn", "category", "image"]


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
