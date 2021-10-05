"""Module contains functions for link url to the page."""
from django.shortcuts import render, get_object_or_404
from .models import Question
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from itertools import chain


class IndexView(generic.ListView):
    """Index page that shows list of all polls."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question'

    def get_queryset(self):
        """Return the published questions."""
        questions = Question.objects.filter(pub_date__lte=timezone.now())\
            .exclude(end_date__lte=timezone.now())\
            .order_by('-pub_date')
        ended_questions = Question.objects.filter(end_date__lte=timezone.now()).order_by('-pub_date')
        result_list = list(chain(questions, ended_questions))
        return result_list


class DetailView(generic.DetailView):
    """Detail page that can let user vote the poll."""

    model = Question
    template_name = 'polls/details.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now()).exclude(end_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Result page that shows individual question."""

    model = Question
    template_name = 'polls/results.html'

    def get_context_data(self, **kwargs):
        """Prepare data for visualisation in pie chart."""
        context = super().get_context_data(**kwargs)
        q_id = context['question'].id
        choice_set = Question.objects.get(pk=q_id).choice_set.all()
        labels = []
        data = []
        for choice in choice_set:
            data.append(choice.votes)
            labels.append(choice.choice_text)
        context['labels'] = labels
        context['data'] = data
        return context


def vote(request, question_id):
    """Vote page that process vote privately and return to result page if success."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except Exception:
        return render(request, "polls/details.html", {'question': question, 'error_message': "Please select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=[question.id],))
