from django import forms


class RegisterForm(forms.Form):
    mail = forms.EmailField(label="Email", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label="Hasło", max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password_repeat = forms.CharField(label="Powtórz hasło", max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))


class LoginForm(forms.Form):
    mail = forms.EmailField(label='Email', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='Hasło', max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
