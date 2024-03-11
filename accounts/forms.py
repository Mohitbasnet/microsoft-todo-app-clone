from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import PasswordInput
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

        self.fields['password1'].widget = PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter a strong password!'}
        )
        self.fields['password2'].widget = PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password confirmation!'}
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = UserChangeForm.Meta.fields

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set placeholders for username and password fields
        self.fields['username'].widget.attrs = {'placeholder':'Enter your username', 'class':'form-control'}
        self.fields['password'].widget.attrs = {'placeholder':'Enter your password', 'class':'form-control'}