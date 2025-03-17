from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db import connection

from .models import Choice, Question, Vote
# from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'polls/login.html')


@login_required
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


@login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


# A01: 2021 - Broken Access Control Fix: Ensure only authenticated users can vote
# This ensures only logged-in users can access this view


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    choice_id = request.POST['choice']
    sql_query = f"UPDATE polls_choice SET votes = votes + 1 WHERE id = {choice_id};"

    with connection.cursor() as cursor:
        cursor.execute(sql_query)  # Executes raw SQL with user input
    # Save the user's vote to prevent multiple votes

    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    # A03:2021-Injection fix
    # try:
    #     selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the question voting form.
    #     return render(request, 'polls/detail.html', {
    #         'question': question,
    #         'error_message': "You didn't select a choice.",
    #     })
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
