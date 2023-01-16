from django.shortcuts import render
from django.views import View

from clothes_app.models import Donation, Institution


class LandingPage(View):
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
        cnx = {
            'bags': bags,
            'institutions': institutions,
            'foundations': foundations,
            'ngo': ngo,
            'local_collections': local_collections,
        }
        return render(request, 'index.html', cnx)


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')


class Login(View):
    def get(self, request):
        return render(request, 'login.html')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')



