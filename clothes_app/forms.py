from django import forms


class RegisterForm(forms.Form):
    mail = forms.EmailField(label="Email", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password_old = forms.CharField(label="Stare hasło", max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password_repeat = forms.CharField(label="Powtórz hasło", max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

class LoginForm(forms.Form):
    mail = forms.EmailField(label='Email', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='Hasło', max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


class EditProfileForm(forms.Form):
    mail = forms.EmailField(label="Email", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(label="Imię", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(label="Nazwisko", max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    password = forms.CharField(label="Hasło", max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))

class ResetPasswordForm(forms.Form):
    password_old = forms.CharField(label="Wprowadź stare hasło", max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Stare Hasło'}))
    password_new = forms.CharField(label="Wprowadź nowe hasło", max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Nowe Hasło'}))
    password_new_repeat = forms.CharField(label="Ponownie wprowadź nowe hasło", max_length=30, widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz nowe hasło'}))

