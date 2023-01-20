from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View

from clothes_app.forms import RegisterForm, LoginForm
from clothes_app.models import Donation, Institution, Category


class LandingPageView(View):
    def get(self, request):
        bags = 0
        bags_list = Donation.objects.values_list('quantity', flat=True)
        for q in bags_list:
            bags += q
        institutions = 0
        institutions_list = Institution.objects.values_list('name', flat=True)
        for _ in institutions_list:
            institutions += 1
        foundations = Donation.objects.filter(institution__type=1)
        ngo = Donation.objects.filter(institution__type=2)
        local_collections = Donation.objects.filter(institution__type=3)
        ctx = {
            'bags': bags,
            'institutions': institutions,
            'foundations': foundations,
            'ngo': ngo,
            'local_collections': local_collections,
        }
        return render(request, 'index.html', ctx)


class AddDonationView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {
            'categories': categories,
            'institutions': institutions,
        }
        return render(request, 'form.html', ctx)


class LoginView(View):
    def get(self, request):
        form = LoginForm
        ctx = {
            'form': form,
        }
        return render(request, 'login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            username = form.cleaned_data.get('mail')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('index')

            else:
                msg = "Zły login, lub hasło"
                form = LoginForm
                ctx = {
                    'form': form,
                    'msg': msg,
                }
                return render(request, 'login.html', ctx)
        return redirect('register')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm
        ctx = {
            'form': form,
        }
        return render(request, 'register.html', ctx)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            password_repeat = form.cleaned_data.get('password_repeat')
            mail = form.cleaned_data.get('mail')
            if User.objects.filter(username=mail).exists():
                msg = 'Użytkownik już istnieje w bazie'
                form = RegisterForm
                ctx = {
                    'form': form,
                    'msg': msg,
                }
                return render(request, 'register.html', ctx)
            if password != password_repeat:
                msg = 'Wprowadzone różne hasła'
                form = RegisterForm
                ctx = {
                    'form': form,
                    'msg': msg,
                }
                return render(request, 'register.html', ctx)
            new_user = User.objects.create_user(username=mail, password=password, email=mail)
            new_user.save()
            return redirect('login')
        return redirect('register')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            donations = Donation.objects.filter(user=request.user)
            ctx = {
                'user': user,
                'donations': donations,
            }
            return render(request, 'profile.html', ctx)
        else:
            ctx = {
                'msg': 'Widok tylko dla zalogowanych',
            }
            return render(request, 'profile.html', ctx)
