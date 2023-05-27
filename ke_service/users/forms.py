from django import forms


class RegisterForm(forms.Form):
    email = forms.EmailField(label='email')
    password = forms.CharField(widget=forms.PasswordInput, label='password')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='confirm_password')
