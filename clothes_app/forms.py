from django import forms

class RegisterForm(forms.Form):
    password = forms.CharField(label="Hasło", max_length=30, widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Powtórz hasło", max_length=30, widget=forms.PasswordInput)
    mail = forms.EmailField(label="Email", max_length=30)
