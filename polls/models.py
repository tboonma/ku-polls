"""Module contains models for polls app (similar to database)."""
from django.db import models
from django.utils import timezone
import django.contrib.auth.models


class Question(models.Model):
    """Model for Question, composed of question text, publish date, and end date."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published')
    end_date = models.DateTimeField('End date', default=None, blank=True, null=True)

    def __str__(self):
        """Generate output for question object."""
        return self.question_text

    def is_published(self):
        """Check that question can be displayed."""
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """Check that question still can be vote."""
        now = timezone.now()
        if self.end_date is None:
            return self.pub_date < now
        return self.pub_date <= now < self.end_date


class Choice(models.Model):
    """Model for Choice, composed of choice text, amount of votes, and question object."""

    choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        """Generate output for choice object."""
        return f"{self.question.question_text} - {self.choice_text}"

    @property
    def votes(self) -> int:
        """Get all votes for choice."""
        return Vote.objects.filter(choice=self).count()


class Vote(models.Model):
    """Model for conducting user voted in each choice."""

    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        """Return value of choice selected."""
        return self.choice.choice_text