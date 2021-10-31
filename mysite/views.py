"""Module contains functions for link url to the page."""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest
from django.dispatch import receiver
import logging


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_passwd = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
        return redirect('polls')
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def get_ip_address(request: HttpRequest):
    """Get the visitor's IP address using request headers.

    Returns:
        If request is forwarded, returns IP address (separated by ,).
        else, take the whole header as IP address.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


logger = logging.getLogger("mysite")


@receiver(user_logged_in)
def logged_in(request, user, **kwargs):
    """Log for logged in."""
    logger.info(f"{user} logged in with IP address: {get_ip_address(request)}")


@receiver(user_login_failed)
def login_failed(credentials, request, **kwargs):
    """Log for unsuccessful login."""
    logger.warning(f"An attempt to access {credentials.get('username')}"
                   f" failed with IP address: {get_ip_address(request)}")


@receiver(user_logged_out)
def logged_out(request, user, **kwargs):
    """Log for logged out."""
    logger.info(f"{user} with IP address: {get_ip_address(request)} has logged out.")
