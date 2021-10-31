"""Test with polls pub_date and end_date."""
from django.test import TestCase
from polls.models import Question
from django.utils import timezone
import datetime
from django.urls import reverse
from .test_questions import QuestionTests


def create_question(question_text, days, end_day=None):
    """Create a question with the given `question_text` and published the \
    given number of `days` offset to now (negative for questions published \
    in the past, positive for questions that have yet to be published)."""
    time = timezone.now() + datetime.timedelta(days=days)
    if end_day is not None:
        end_time = timezone.now() + datetime.timedelta(days=end_day)
        return Question.objects.create(question_text=question_text, pub_date=time, end_date=end_time)
    else:
        return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    """Test methods in Question Model."""

    def test_is_published_with_future_question(self):
        """is_published() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.is_published())

    def test_is_published_with_recent_question(self):
        """is_published() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.is_published())

    def test_can_vote_with_future_question(self):
        """can_vote() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.can_vote())

    def test_can_vote_with_old_question(self):
        """can_vote() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=2, seconds=1)
        old_question = Question(pub_date=timezone.now(), end_date=time)
        self.assertFalse(old_question.can_vote())

    def test_can_vote_with_recent_question(self):
        """can_vote() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertTrue(recent_question.can_vote())


class QuestionIndexViewTests(TestCase):
    """Test for Question queries."""

    def test_recent_question(self):
        """Questions with a pub_date in the past are displayed on the index page."""
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question'],
            [question],
        )

    def test_future_question(self):
        """Questions with a pub_date in the future aren't displayed on the index page."""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question'], [])


class QuestionDetailViewTests(QuestionTests):
    """Test for viewing each question detail."""

    def test_view_recent_question(self):
        """View the available question."""
        response = self.client.get(reverse('polls:detail', kwargs={'question_id': self.recent_question.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_ended_question(self):
        """View ended poll should return error 404."""
        response = self.client.get(reverse('polls:detail', kwargs={'question_id': self.ended_question.id}))
        self.assertEqual(response.status_code, 404)

    def test_view_future_question(self):
        """View the question that gonna be available in the future."""
        response = self.client.get(reverse('polls:detail', kwargs={'question_id': self.future_question.id}))
        self.assertEqual(response.status_code, 404)


class QuestionResultViewTests(QuestionTests):
    """Test for viewing result in each question."""

    def test_view_recent_result(self):
        """Test for viewing available poll result."""
        response = self.client.get(reverse('polls:results', kwargs={'pk': self.recent_question.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_ended_result(self):
        """Test for viewing ended poll result."""
        response = self.client.get(reverse('polls:results', kwargs={'pk': self.ended_question.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_future_result(self):
        """Test for viewing future poll, this shouldn’t be appeared."""
        response = self.client.get(reverse('polls:results', kwargs={'pk': self.future_question.id}))
        self.assertEqual(response.status_code, 404)
