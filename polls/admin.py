"""Module contains config for implementing question in admin site."""
from django.contrib import admin

# Register your models here.
from .models import Question, Choice, Vote


class ChoiceInline(admin.StackedInline):
    """Display inline in create question page."""

    model = Choice
    extra = 2
    fieldsets = [
        (None, {'fields': ['choice_text']})
    ]


class QuestionAdmin(admin.ModelAdmin):
    """Custom question list in admin page."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'is_published', 'can_vote', 'end_date')
    list_filter = ['pub_date', 'end_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
