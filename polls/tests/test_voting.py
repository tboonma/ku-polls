"""Test for voting poll."""
from django.test import TestCase
from polls.models import Choice
from django.urls import reverse
from .test_questions import create_question
from django.contrib.auth.models import User


class QuestionVoteTests(TestCase):
    """Test for voting a question."""

    def setUp(self):
        """Initialize all necessary questions."""
        self.recent_question = create_question(question_text="Question1", days=0)
        self.ended_question = create_question(question_text="Question2", days=-10, end_day=-5)
        self.future_question = create_question(question_text="Question3", days=10)
        self.username = "testuser"
        self.password = "HelloIamhere!"
        self.user1 = User.objects.create_user(
            username=self.username,
            email="testuser@mail.com",
            password=self.password)
        self.user1.save()
        # login
        form_data = {'username': self.username, 'password': self.password}
        self.client.post(reverse("login"), form_data)

    def test_vote_recent_question(self):
        """After voting the available poll, the result should increase."""
        choice1 = Choice.objects.create(choice_text="1", question=self.recent_question)
        choice2 = Choice.objects.create(choice_text="2", question=self.recent_question)
        response = self.client.post(reverse('polls:vote', kwargs={'question_id': self.recent_question.id}),
                                    {'choice': choice1.id})
        self.assertEqual(response.status_code, 302)
        choice1 = Choice.objects.get(id=choice1.id)
        choice2 = Choice.objects.get(id=choice2.id)
        self.assertEqual(1, choice1.votes)
        self.assertEqual(0, choice2.votes)

    def test_vote_ended_question(self):
        """After voting ended question (can be access by hacking), the result should still the same."""
        choice1 = Choice.objects.create(choice_text="3", question=self.ended_question)
        choice2 = Choice.objects.create(choice_text="4", question=self.ended_question)
        response = self.client.post(reverse('polls:vote', kwargs={'question_id': self.ended_question.id}),
                                    {'choice': choice1.id})
        self.assertEqual(response.status_code, 404)
        choice1 = Choice.objects.get(id=choice1.id)
        choice2 = Choice.objects.get(id=choice2.id)
        self.assertEqual(0, choice1.votes)
        self.assertEqual(0, choice2.votes)

    def test_vote_future_question(self):
        """Test that the poll that is not published cannot be voted."""
        choice1 = Choice.objects.create(choice_text="5", question=self.future_question)
        choice2 = Choice.objects.create(choice_text="6", question=self.future_question)
        response = self.client.post(reverse('polls:vote', kwargs={'question_id': self.future_question.id}),
                                    {'choice': choice1.id})
        self.assertEqual(response.status_code, 404)
        choice1 = Choice.objects.get(id=choice1.id)
        choice2 = Choice.objects.get(id=choice2.id)
        self.assertEqual(0, choice1.votes)
        self.assertEqual(0, choice2.votes)

    def test_vote_with_no_choice_selected(self):
        """Test submit vote with no choice selected, should get error message."""
        Choice.objects.create(choice_text="7", question=self.recent_question)
        response = self.client.post(reverse('polls:vote', kwargs={'question_id': self.recent_question.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please select a choice")

    def test_vote_when_not_logged_in(self):
        """Test submit vote without login."""
        self.client.post(reverse("logout"))
        choice1 = Choice.objects.create(choice_text="3", question=self.ended_question)
        Choice.objects.create(choice_text="4", question=self.ended_question)
        response = self.client.post(reverse('polls:vote', kwargs={'question_id': self.ended_question.id}),
                                    {'choice': choice1.id})
        self.assertEqual(response.status_code, 302)
