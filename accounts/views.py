from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import StaffLoginForm

@login_required
def keep_alive(request):
    return JsonResponse({"status": "ok"})


def login_view(request):
    """
    Staff Login
    """

    if request.user.is_authenticated:

        if hasattr(request.user, "customer_profile"):
            return redirect("customer_portal:dashboard")

        return redirect("dashboard:index")

    form = StaffLoginForm(request.POST or None)

    if request.method == "POST":

        username = form.data.get("username")
        password = form.data.get("password")

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

            if hasattr(user, "customer_profile"):
                return redirect("customer_portal:dashboard")

            return redirect("dashboard:index")

        messages.error(
            request,
            "Invalid email address or password.",
        )

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
        },
    )





def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out.",
    )

    return redirect("accounts:login")
