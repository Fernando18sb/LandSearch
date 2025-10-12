import uuid

from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, EmailVerifyForm
from .encryption_program import encryption, decryption



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            generated_code = uuid.uuid4().hex[:5]
            path_code = uuid.uuid4().hex[:6]
            user_email = form.cleaned_data.get('email')

            send_mail(
                "HouseFinder Register",
                f"The Code : {generated_code}",
                f"{settings.EMAIL_HOST_USER}",
                [user_email],
                fail_silently=False,
            )

            context = {
                'code': generated_code,
                'form_data': form.cleaned_data,
                'path': path_code
            }

            #encrypted_data = encryption(context)

            return render(request, f'users/verify_email.html', {
                'verify_form': EmailVerifyForm(),
                'context': context,
                #'user_email': user_email,
            })
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})

def verify_email(request, path_code):
    if request.method == 'POST':
        user_code = request.POST.get('code')


        try:
            context = request.POST.get('context')
            #context = decryption(encrypted_data)
        except Exception:
            messages.error(request, "Invalid verification data.")
            return redirect('register')

        if user_code == context['code']:
            form_data = context['form_data']
            form = UserRegisterForm(form_data)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Your account has been created Mr. {username}! You are now able to log in.')
                return redirect('login')
            else:
                messages.error(request, "Form data invalid during verification.")
        else:
            messages.error(request, "Invalid verification code.")
    else:
        verify = EmailVerifyForm()

    return render(request, 'users/verify_email.html', {'verify': verify})

def logout_view(request):

    logout(request)

    return render(request, 'users/logout.html')

@login_required
def profile(request):

    if request.method == 'POST':

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():

            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been Updated")

            return redirect('profile')
    else:

        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)



    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)




class PasswordReset(LoginRequiredMixin, UserPassesTestMixin, PasswordResetView):
    pass

class PasswordResetConfirm(LoginRequiredMixin, PasswordResetConfirmView):
    pass

class PasswordResetComplete(LoginRequiredMixin, PasswordResetCompleteView):
    pass

class PasswordResetDone(LoginRequiredMixin, PasswordResetDoneView):
    pass

