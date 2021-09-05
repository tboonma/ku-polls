from django.test import TestCase
from polls.models import Question, Choice
from django.utils import timezone


# Create your tests here.
class QuestionTestCase(TestCase):
    def setUp(self):
        Question.objects.create(question_text="What's your most used transportation?", pub_date=timezone.now())

    def test_question_title(self):
        transport = Question.objects.get(question_text="What's your most used transportation?")
        self.assertEqual(transport.question_text, "What's your most used transportation?")


class ChoiceTestCase(TestCase):
    def setUp(self):
        self.question = Question.objects.create(question_text="What's your most used transportation?", pub_date=timezone.now())
        self.choice = Choice("BTS", question=self.question)

    def test_choice_link(self):
        self.assertEqual(self.choice.question.question_text, "What's your most used transportation?")
