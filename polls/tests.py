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
        """Setting up all necessary questions."""
        self.recent_question = create_question(question_text="Question1", days=0)
        self.ended_question = create_question(question_text="Question2", days=-10, end_day=-5)
        self.future_question = create_question(question_text="Question3", days=10)


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

    def test_question_txt_display(self):
        """Test that question model can display text correctly."""
        question = create_question(question_text="How do you go to the university.", days=0)
        self.assertEqual("How do you go to the university.", question.__str__())


class QuestionIndexViewTests(TestCase):
    """Test for Question queries."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question'], [])

    def test_past_question(self):
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

    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed."""
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question'],
            [question],
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question'],
            [question2, question1],
        )


class QuestionDetailViewTests(QuestionTests):
    """Test for viewing each question detail."""

    def test_view_recent_question(self):
        """View the available question."""
        response = self.client.get(reverse('polls:detail', kwargs={'pk': self.recent_question.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_ended_question(self):
        """View ended poll should return error 404."""
        response = self.client.get(reverse('polls:detail', kwargs={'pk': self.ended_question.id}))
        self.assertEqual(response.status_code, 404)

    def test_view_future_question(self):
        """View the question that gonna be available in the future."""
        response = self.client.get(reverse('polls:detail', kwargs={'pk': self.future_question.id}))
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

    def test_choice_displayed(self):
        """Test that all choice displayed correctly."""
        choice1 = Choice.objects.create(choice_text="1", question=self.recent_question)
        choice2 = Choice.objects.create(choice_text="2", question=self.recent_question)
        response = self.client.get(reverse('polls:results', kwargs={'pk': self.recent_question.id}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['labels'], ["1", "2"])
        self.assertQuerysetEqual(response.context['data'], [0, 0])


class QuestionVoteTests(QuestionTests):
    """Test for voting a question."""

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
        choice1 = Choice.objects.create(choice_text="7", question=self.recent_question)
        response = self.client.post(reverse('polls:vote', kwargs={'question_id': self.recent_question.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please select a choice")


class ChoiceModelTests(TestCase):
    """Test methods in Choice Model."""

    def test_choice_display_correctly(self):
        """Test that choice can be displayed correctly including question."""
        question = create_question(question_text="How do you go to the university.", days=0)
        choice = Choice.objects.create(choice_text="BTS", question=question)
        self.assertEqual("How do you go to the university. - BTS", choice.__str__())
