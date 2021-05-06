from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import View

from .models import User
from flight.models import Flight


class RegisterView(View):
    template_name = 'account/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('admin-dashboard')
            return redirect('user-dashboard')
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        try:
            user = User.objects.create_user(username=username, password=password,
                                            email=email, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()

        except Exception as e:
            print(e)
            return render(request, self.template_name, {'error': 'Username already exists!'})

        if user:
            login(request, user)
            return redirect('user-dashboard')
        return render(request, self.template_name, {'error': 'Unknown Error!'})


class LoginView(View):
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('admin-dashboard')
            return redirect('user-dashboard')

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, self.template_name, {'error': 'Username/password Invalid'})
        login(request, user)

        if user.is_superuser:
            return redirect('admin-dashboard')
        else:
            return redirect('user-dashboard')


class UserDashboardView(View):
    template_name = 'account/dashboard.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        context = {
            'object_list': Flight.objects.filter(booked_by=request.user, status='booked'),
            'cancelled_list': Flight.objects.filter(booked_by=request.user, status='cancelled'),
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        return redirect('register')


class AdminDashboardView(View):
    template_name = 'account/admin-dashboard.html'

    def get(self, request, *args, **kwargs):
        if not (request.user.is_authenticated or request.user.is_superuser):
            return redirect('home')

        context = {
            'object_list': Flight.objects.all().order_by('-flight_date', '-flight_time', 'status'),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return redirect('register')


@login_required(login_url='login')
def logoutView(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin-dashboard')
    return redirect('user-dashboard')
