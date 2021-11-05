"""Tests of authentication."""
import django.test
from django.urls import reverse
from django.contrib.auth.models import User


class UserAuthTest(django.test.TestCase):
    """Testing for authentication."""

    def setUp(self):
        """Set up for testing."""
        super().setUp()
        self.username = "testuser"
        self.password = "HelloIamhere!"
        self.user1 = User.objects.create_user(
            username=self.username,
            email="testuser@mail.com",
            password=self.password)
        self.user1.first_name = "Tester"
        self.user1.save()

    def test_login_view(self):
        """Test that a user can login via the login view."""
        login_url = reverse("login")
        # Can get the login page
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        # Can login using POST
        # usage: client.post(url, {'key1': "value", 'key2': "value"})
        form_data = {'username': self.username, 'password': self.password}
        response = self.client.post(login_url, form_data)
        self.assertEqual(302, response.status_code)
        # should redirect us to the polls index page ("polls:index")
        self.assertRedirects(response, reverse("polls:index"))

    def test_signup_view(self):
        """Test that user can signup using signup view."""
        signup_url = reverse("signup")
        # Can get the signup page
        response = self.client.get(signup_url)
        self.assertEqual(200, response.status_code)
        # Can signup using POST
        # usage: client.post(url, {'key1': "value", 'key2': "value"})
        form_data = {'username': "Mark",
                     'password1': "Iamhere1234",
                     'password2': "Iamhere1234"}
        response = self.client.post(signup_url, form_data)
        self.assertEqual(302, response.status_code)
        # should redirect us to the polls index page ("polls:index")
        self.assertRedirects(response, reverse("polls:index"))

    def test_signup_view_authenticated(self):
        """Test accessing signup view when logged in."""
        # Login first
        form_data = {'username': self.username, 'password': self.password}
        self.client.post(reverse("login"), form_data)
        # Go to signup page.
        signup_url = reverse("signup")
        # Can get the signup page
        response = self.client.get(signup_url)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse("polls:index"))  # Should redirect to home page.

    def test_invalid_signup(self):
        """Test signup with duplicate username"""
        # Signup using POST with duplicated username.
        # usage: client.post(url, {'key1': "value", 'key2': "value"})
        form_data = {'username': self.username,
                     'password1': "Iamhere1234",
                     'password2': "Iamhere1234"}
        response = self.client.post(reverse("signup"), form_data)
        self.assertEqual(200, response.status_code)
        # should contains error message
        self.assertContains(response, "A user with that username already exists.")
