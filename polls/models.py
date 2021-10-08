"""Module contains models for polls app (similar to database)."""
from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    """Model for Question, composed of question text, publish date, and end date."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published')
    end_date = models.DateTimeField('End date', default=None, blank=True, null=True)

    def __str__(self):
        """Generate output for question object."""
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
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
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        """Generate output for choice object."""
        return self.choice_text
