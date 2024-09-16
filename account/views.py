import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from icecream import ic

User = get_user_model()


def login_view(request):
    if request.method == "POST":
        # Get the form data
        email = request.POST["email"]
        password = request.POST["password"]

        # Get the custom user model
        User = get_user_model()

        try:
            # Try to find a user with the provided email
            user = User.objects.get(email=email)

            # Authenticate user
            user = authenticate(request, username=user.email, password=password)

            if user is not None:
                # If the user is valid, log them in
                login(request, user)
                # Redirect to a different page after successful login
                return redirect(
                    "dues:index"
                )  # Change 'dues:index' to the appropriate URL name
            else:
                # Add an error message if authentication fails
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            # Add an error message if the email is not found
            messages.error(request, "Invalid email or password.")

    return render(request, "account/login.html")


# @csrf_protect
def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        terms_accepted = request.POST.get(
            "terms_accepted", "false"
        )  # Default to "false" if not provided

        print(
            f"Data received: {first_name}, {last_name}, {email}, {phone_number}, {password}, {terms_accepted}"
        )

        # Convert to boolean for checking
        terms_accepted = terms_accepted == "true"

        if not terms_accepted:
            print("Terms not accepted")
            messages.error(request, "You must agree to the terms and conditions.")
            return render(request, "account/register.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "account/register.html")

        # Normalize the phone number to start with 233
        if phone_number.startswith("0"):
            phone_number = "233" + phone_number[1:]
        elif phone_number.startswith("+233"):
            phone_number = "233" + phone_number[4:]
        elif not phone_number.startswith("233"):
            phone_number = "233" + phone_number

        # Validate phone number format (optional)
        if not re.match(r"^233\d{9}$", phone_number):
            messages.error(request, "Invalid phone number format.")
            return render(request, "register.html")

        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                password=password,
            )
            messages.success(
                request, "Your account has been created successfully. Login"
            )
            return redirect("account:login")  # Redirect to login page
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return render(request, "account/register.html")

    return render(request, "account/register.html")


@login_required
def sign_out(request):
    """Log out the user and redirect to the home page."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("account:login")
