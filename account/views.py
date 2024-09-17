import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from icecream import ic

from .forms import NotificationSettingsForm, ProfileUpdateForm
from .models import Profile

User = get_user_model()

@login_required
def faq_view(request):
    return render(request, "account/faq.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.email, password=password)

            if user is not None:
                login(request, user)
                return redirect("dues:index")
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")

    return render(request, "account/login.html")

@csrf_protect
def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        terms_accepted = request.POST.get("terms_accepted", "false")

        terms_accepted = terms_accepted == "true"

        if not terms_accepted:
            messages.error(request, "You must agree to the terms and conditions.")
            return render(request, "account/register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "account/register.html")

        if phone_number.startswith("0"):
            phone_number = "233" + phone_number[1:]
        elif phone_number.startswith("+233"):
            phone_number = "233" + phone_number[4:]
        elif not phone_number.startswith("233"):
            phone_number = "233" + phone_number

        if not re.match(r"^233\d{9}$", phone_number):
            messages.error(request, "Invalid phone number format.")
            return render(request, "account/register.html")

        try:
            user = User.objects.create_user(
                first_name=first_name.capitalize(),
                last_name=last_name.capitalize(),
                email=email,
                phone_number=phone_number,
                password=password,
            )
            messages.success(request, "Your account has been created successfully. Login")
            return redirect("account:login")
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return render(request, "account/register.html")

    return render(request, "account/register.html")

@login_required
def sign_out(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("account:login")

@login_required
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    # Initialize forms
    profile_form = ProfileUpdateForm(instance=user)
    notifications_form = NotificationSettingsForm(instance=profile)
    password_form = PasswordChangeForm(user)

    if request.method == "POST":
        if "update_profile" in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully!")
                return redirect("account:profile")
            else:
                for error in profile_form.errors:
                    messages.error(request, error)

        elif "update_notifications" in request.POST:
            notifications_form = NotificationSettingsForm(request.POST, instance=profile)
            if notifications_form.is_valid():
                notifications_form.save()
                messages.success(request, "Notification settings updated successfully!")
                return redirect("account:profile")
            else:
                for error in notifications_form.errors:
                    messages.error(request, error)

        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password changed successfully!")
                return redirect("account:profile")
            else:
                for error in password_form.errors:
                    messages.error(request, error)

    return render(
        request,
        "account/profile.html",
        {
            "user": user,
            "profile": profile,
            "profile_form": profile_form,
            "notifications_form": notifications_form,
            "password_form": password_form,
        },
    )
