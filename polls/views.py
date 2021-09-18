from django.shortcuts import render, get_object_or_404
from .models import Question
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from itertools import chain

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question'

    def get_queryset(self):
        """Return the published questions."""
        questions = Question.objects.filter(pub_date__lte=timezone.now()).exclude(end_date__lte=timezone.now()).order_by('-pub_date')
        ended_questions = Question.objects.filter(end_date__lte=timezone.now()).order_by('-pub_date')
        result_list = list(chain(questions, ended_questions))
        return result_list

    def get_available_question(self):
        return Question.objects.is_published()


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/details.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).exclude(end_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except:
        return render(request, "polls/details.html", {'question': question, 'error_message': "Please select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=[question.id],))
