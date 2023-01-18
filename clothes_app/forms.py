from django import forms


class RegisterForm(forms.Form):
    mail = forms.EmailField(label="Email", max_length=30)
    password = forms.CharField(label="Hasło", max_length=30, widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Powtórz hasło", max_length=30, widget=forms.PasswordInput)


class LoginForm(forms.Form):
    mail = forms.EmailField(label='Email', max_length=30)
    password = forms.CharField(label='Hasło', max_length=30, widget=forms.PasswordInput)
