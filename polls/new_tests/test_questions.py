"""Module used to test polls models."""
from django.test import TestCase
from polls.models import Question, Choice
from django.utils import timezone
import datetime
from django.urls import reverse


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


class QuestionTests(TestCase):
    """Test for Question model."""

    def setUp(self):
        """Initialize all necessary questions."""
        self.recent_question = create_question(question_text="Question1", days=0)
        self.ended_question = create_question(question_text="Question2", days=-10, end_day=-5)
        self.future_question = create_question(question_text="Question3", days=10)


class QuestionModelTests(TestCase):
    """Test methods in Question Model."""

    def test_question_txt_display(self):
        """Test that question model can display text correctly."""
        question = create_question(question_text="How do you go to the university.", days=0)
        self.assertEqual("How do you go to the university.", question.__str__())


class QuestionResultViewTests(QuestionTests):
    """Test for viewing result in each question."""

    def test_choice_displayed(self):
        """Test that all choice displayed correctly."""
        Choice.objects.create(choice_text="1", question=self.recent_question)
        Choice.objects.create(choice_text="2", question=self.recent_question)
        response = self.client.get(reverse('polls:results', kwargs={'pk': self.recent_question.id}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['labels'], ["1", "2"])
        self.assertQuerysetEqual(response.context['data'], [0, 0])


class ChoiceModelTests(TestCase):
    """Test methods in Choice Model."""

    def test_choice_display_correctly(self):
        """Test that choice can be displayed correctly including question."""
        question = create_question(question_text="How do you go to the university.", days=0)
        choice = Choice.objects.create(choice_text="BTS", question=question)
        self.assertEqual("BTS", choice.__str__())
