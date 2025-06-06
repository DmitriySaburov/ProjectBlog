from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin


from .forms import SignUpForm, LoginForm, UpdateUserForm, UpdateProfileForm



class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    initial = None   # принимает {"key": "value"}
    template_name = "registration/signup.html"

    def dispatch(self, request, *args, **kwargs):
        # перенаправит на домашнюю страницу, если пользователь попытается получить доступ к странице регистрации после авторизации
        if request.user.is_authenticated:
            return redirect(to="/")
        
        return super(SignUpView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {"form": form}
        return render(request,
                      template_name=self.template_name,
                      context=context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}")
            # редирект на страницу логина после регистрации
            return redirect(to="login")
        
        context = {"form": form}
        return render(request,
                      template_name=self.template_name,
                      context=context)


class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            # Установим время истечения сеанса равным 0 секундам. Таким образом, он автоматически закроет сеанс после закрытия браузера. И обновим данные.
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        
        # В противном случае сеанс браузера будет таким же как время сеанса cookie "SESSION_COOKIE_AGE", определенное в settings.py
        return super(CustomLoginView, self).form_valid(form)


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UpdateUserForm(
            request.POST, instance=request.user
        )
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "your profile is updated successfully")
            return redirect(to="users-profile")
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    
    context = {"user_form": user_form, "profile_form": profile_form}
    return render(request,
                  template_name="registration/profile.html",
                  context=context)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = "registration/change_password.html"
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy("users-profile")
