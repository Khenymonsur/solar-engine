from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render


def login_view(request):
    """
    User Login
    """

    if request.user.is_authenticated:
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
                f"Welcome back, {user.username}!",
            )

            return redirect("dashboard:index")

        messages.error(
            request,
            "❌ Invalid username or password.",
        )

        print("LOGIN ERROR MESSAGE ADDED")

    return render(
        request,
        "accounts/login.html",
    )


def logout_view(request):
    """
    Logout
    """

    logout(request)

    messages.success(
        request,
        "You have been logged out.",
    )

    return redirect("accounts:login")
