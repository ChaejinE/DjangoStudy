from django import forms
from django.contrib.auth.forms import UserCreationForm
from shortner.models import Users


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=30, required=False, help_text="Optional.", label="이름")
    username = forms.CharField(max_length=30, required=False, help_text="Optional.")
    email = forms.EmailField(max_length=254, help_text="Required. Inform a valid email address.")

    class Meta:
        model = Users
        fields = (
            "username",
            "full_name",
            "email",
            "password1",
            "password2",
        )

class LoginForm(forms.Form):
    email = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "이메일"}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "패스워드"}))
    remeber_me = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "custom-control-input", "id": "_loginRemeberMe"}),
                                    required=False, disabled=False)