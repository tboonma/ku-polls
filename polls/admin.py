"""Module contains config for implementing question in admin site."""
from django.contrib import admin

# Register your models here.
from .models import Question, Choice


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2
    fieldsets = [
        (None, {'fields': ['choice_text']})
    ]


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'is_published', 'can_vote', 'end_date')
    list_filter = ['pub_date', 'end_date']
    search_fields = ['question_text']


class ChoiceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question', {'fields': ['question']}),
        ('Choice information', {'fields': ['choice_text', 'votes']}),
    ]
    list_display = ('choice_text', 'question', 'votes')
    list_filter = ['question']
    search_fields = ['choice_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
