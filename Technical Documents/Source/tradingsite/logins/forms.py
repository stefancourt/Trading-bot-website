from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        # Calls the constructor of the parent class
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        # Removes lengths and help text from fields
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].widget.attrs.pop('maxlength', None)
            self.fields[field_name].widget.attrs.pop('minlength', None)
            self.fields[field_name].help_text = None

        # Adds classes to each field
        self.fields['username'].widget.attrs['class'] = 'form-username'
        self.fields['password1'].widget.attrs['class'] = 'form-password1'
        self.fields['password2'].widget.attrs['class'] = 'form-password2'

class CustomAuthenticationForm(AuthenticationForm):

    error_css_class = 'error'

    def __init__(self, *args, **kwargs):
        # Calls the constructor of the parent class
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

        # Adds classes to each field
        self.fields['username'].widget.attrs['class'] = 'form-username'
        self.fields['password'].widget.attrs['class'] = 'form-password1'


    def clean(self):
        # Cleans the data to be used in the model
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        return cleaned_data