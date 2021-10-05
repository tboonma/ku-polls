"""Module contains config for polls app."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """Config for polls app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
