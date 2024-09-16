from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.shortcuts import redirect, render


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
