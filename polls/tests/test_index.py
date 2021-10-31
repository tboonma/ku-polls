"""Test index view of polls app."""
from django.test import TestCase
from django.urls import reverse
from .test_questions import create_question


class QuestionIndexViewTests(TestCase):
    """Test for Question queries."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question'], [])

    def test_one_questions(self):
        """Test that the page showing 1 poll."""
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question'],
            [question],
        )

    def test_two_questions(self):
        """Test that the page can show more than 1 poll."""
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question'],
            [question2, question1],
        )
