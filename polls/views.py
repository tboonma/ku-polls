"""Module contains functions for link in polls app url to the page."""
from django.shortcuts import render, get_object_or_404
from .models import Question, Vote
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from itertools import chain
from django.contrib.auth.decorators import login_required
import logging


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

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


def detail(request, question_id):
    """Render details page for individual question."""
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    if request.user.is_authenticated:
        voted = Vote.objects.filter(choice__question=question, user=request.user)
        if voted:
            context['voted'] = voted[0].choice
    return render(request, "polls/details.html", context)


@login_required(login_url='/accounts/login/')
def vote(request, question_id):
    """Vote page that process vote privately and return to result page if success."""
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        return HttpResponseNotFound("This poll cannot be voted.")
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except Exception:
        return render(request, "polls/details.html", {'question': question, 'error_message': "Please select a choice"})
    voted_before = Vote.objects.filter(choice__question=question, user=request.user)
    if voted_before:
        voted = voted_before[0]
        voted.choice = selected_choice
    else:
        voted = Vote.objects.create(choice=selected_choice, user=request.user)
    logger = logging.getLogger("polls")
    logger.info(f"{request.user} votes for {selected_choice.choice_text} in {question.question_text}.")
    voted.save()
    return HttpResponseRedirect(reverse('polls:results', args=[question.id],))
