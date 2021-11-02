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

    def test_invalid_login(self):
        """Test that a user login with incorrect password should get error message."""
        login_url = reverse("login")
        form_data = {'username': self.username, 'password': "1234"}
        response = self.client.post(login_url, form_data)
        self.assertContains(response, "Please enter a correct username and password.")

    def test_signup_view(self):
        """Test that user can signup correctly."""
        signup_url = reverse("signup")
        # Can get the signup page
        response = self.client.get(signup_url)
        self.assertEqual(200, response.status_code)
        # Can signup using POST
        # usage: client.post(url, {'key1': "value", 'key2': "value"})
        form_data = {'username': "Mark",
                     'password1': "Vote4me!",
                     'password2': "Vote4me!"}
        response = self.client.post(signup_url, form_data)
        self.assertEqual(302, response.status_code)
        # should redirect us to the polls index page ("polls:index")
        self.assertRedirects(response, reverse("polls:index"))

    def test_signup_with_invalid_pass_cf(self):
        """Test that signup with invalid password confirmation."""
        signup_url = reverse("signup")
        # signup using POST
        # usage: client.post(url, {'key1': "value", 'key2': "value"})
        form_data = {'username': "Mark",
                     'password1': "Vote4me!",
                     'password2': "Vote4m"}
        response = self.client.post(signup_url, form_data)
        self.assertContains(response, "The two password fields didn’t match.")

    def test_signup_with_easy_password(self):
        """Test that signup with too easy to guess password."""
        signup_url = reverse("signup")
        # signup using POST
        # usage: client.post(url, {'key1': "value", 'key2': "value"})
        form_data = {'username': "Mark",
                     'password1': "1234",
                     'password2': "1234"}
        response = self.client.post(signup_url, form_data)
        self.assertContains(response, "This password is")
