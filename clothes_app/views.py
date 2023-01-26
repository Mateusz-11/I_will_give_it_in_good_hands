from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from clothes_app.forms import RegisterForm, LoginForm, EditProfileForm, ResetPasswordForm
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
        foundations1 = Donation.objects.filter(institution__type=1)
        paginator = Paginator(foundations1, 5)
        page_number = request.GET.get('page')
        foundations = paginator.get_page(page_number)

        ngo1 = Donation.objects.filter(institution__type=2)
        paginator = Paginator(ngo1, 5)
        page_number = request.GET.get('page')
        ngo = paginator.get_page(page_number)

        local_collections1 = Donation.objects.filter(institution__type=3)
        paginator = Paginator(local_collections1, 5)
        page_number = request.GET.get('page')
        local_collections = paginator.get_page(page_number)

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
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
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
            new_user = User.objects.create_user(username=mail, password=password, email=mail, first_name=first_name,
                                                last_name=last_name)
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


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request,  user_id):
        user = request.user
        form = EditProfileForm(initial={'mail': user.email, "first_name": user.first_name, "last_name": user.last_name})
        ctx = {
            'form': form,
        }
        return render(request, 'edit_profile.html', ctx)

    def post(self, request,  user_id):
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(User, pk=user_id)
            mail = form.cleaned_data.get('mail')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password')
            user_auth = authenticate(username=user.username, password=password)
            if user_auth is not None:
                user.mail = mail
                user.username = mail
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                ctx = {
                    'msg': "Dane zostały zmienione",
                }
                return render(request, 'edit_profile.html', ctx)
            else:
                ctx = {
                    'msg': "Błędne hasło",
                    'form': form,
                }
                return render(request, 'edit_profile.html', ctx)
        return redirect('index')


class ResetPasswordView(LoginRequiredMixin, View):
    def get(self, request,  user_id):
        form = ResetPasswordForm(request.POST)
        ctx = {
            'form': form,
        }
        return render(request, 'reset_password.html', ctx)

    def post(self, request,  user_id):
        form = ResetPasswordForm(request.POST)
        ctx = {
            'form': form,
        }
        if form.is_valid():
            user = get_object_or_404(User, pk=user_id)
            password_old = form.cleaned_data.get('password_old')
            password_new = form.cleaned_data.get('password_new')
            password_new_repeat = form.cleaned_data.get('password_new_repeat')
            user_auth = authenticate(username=user.username, password=password_old)
            if user_auth is not None:
                if password_new != password_new_repeat:
                    ctx = {
                        'msg': "Hasła sie różnią",
                        'form': form,
                    }
                    return render(request, 'reset_password.html', ctx)
                user.set_password(password_new)
                user.save()
                ctx = {
                    'msg': "Hasło zostało zmienione",
                }
                return render(request, 'reset_password.html', ctx)
            ctx = {
                'msg': "Błędne hasło",
                'form': form,
            }
            return render(request, 'reset_password.html', ctx)
        return render(request, 'reset_password.html', ctx)
    