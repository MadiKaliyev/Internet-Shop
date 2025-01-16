from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, FormView
from carts.models import Cart
from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            auth_login(self.request, user)
            messages.success(self.request, 'Вы вошли в аккаунт.')

            redirect_page = self.request.POST.get('next', None)
            if redirect_page and redirect_page != reverse('user:logout'):
                return HttpResponseRedirect(redirect_page)

            return HttpResponseRedirect(reverse('shop:index'))
        else:
            messages.error(self.request, 'Неправильное имя пользователя или пароль.')
        return super().form_invalid(form)


class RegistrationView(FormView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Вы успешно зарегистрировались! Добро пожаловать в систему.')
        auth_login(self.request, user)
        return redirect('shop:index')

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class ProfileView(LoginRequiredMixin, FormView):
    template_name = 'users/profile.html'
    form_class = ProfileForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user  
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, 'Ваш профиль был успешно обновлен.')
        return redirect('users:profile')

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        messages.success(request, f'{request.user.username}, Вы вышли из аккаунта')
        auth_logout(request)
        return redirect(reverse('shop:index'))


class UsersCartView(LoginRequiredMixin, TemplateView):
    template_name = 'users/users_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = Cart.objects.filter(user=self.request.user)
        context['cart_items'] = cart_items
        context['total_price'] = sum(item.product_price() for item in cart_items)
        context['total_quantity'] = sum(item.quantity for item in cart_items)
        return context
