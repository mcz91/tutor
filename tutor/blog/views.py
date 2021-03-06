from asyncio import QueueEmpty
from queue import Empty
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.urls import reverse
from django.views import generic
from blog.models import Choice, Question 
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        output = []
        for question in  Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date'):
            if len(question.choice_set.all()) != 0 and len(output) < 5:
                output.append(question)
        return output

class DetailView(generic.DetailView):
    model = Question
    template_name = 'blog/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'blog/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'blog/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('blog:results', args=(question.id,)))