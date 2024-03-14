from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].widget.attrs.pop('maxlength', None)
            self.fields[field_name].widget.attrs.pop('minlength', None)
            self.fields[field_name].help_text = None

        self.fields['username'].widget.attrs['class'] = 'form-username'
        self.fields['password1'].widget.attrs['class'] = 'form-password1'
        self.fields['password2'].widget.attrs['class'] = 'form-password2'

class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)


        self.fields['username'].widget.attrs['class'] = 'form-username'

        self.fields['password'].widget.attrs['class'] = 'form-password1'

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        return cleaned_data