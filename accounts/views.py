from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from customers.models import Customer


def login_view(request):
    """
    Staff Login
    """

    if request.user.is_authenticated:

        if hasattr(request.user, "customer_profile"):
            return redirect("customer_portal:dashboard")

        return redirect("dashboard:index")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user:

            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.first_name or user.username}!",
            )

            # Customer account
            if hasattr(user, "customer_profile"):
                return redirect("customer_portal:dashboard")

            # Staff account
            return redirect("dashboard:index")

        messages.error(
            request,
            "Invalid username or password.",
        )

    return render(
        request,
        "accounts/login.html",
    )


def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out.",
    )

    return redirect("accounts:login")
