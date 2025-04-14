from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db import connection

from .models import Choice, Question, Vote
# from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'polls/login.html')


# A01:2021 - Broken Authentication Fix: Ensure only authenticated users can view questions
# @login_required
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# A01:2021 - Broken Authentication Fix: Ensure only authenticated users can view question details
# @login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

# A01:2021 - Broken Authentication Fix: Ensure only authenticated users can view results
# @login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


# A01: 2021 - Broken Access Control Fix: Ensure only authenticated users can vote
# @login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # A03:2021 - Injection: Unsafe SQL using user input!
    choice_id = request.POST['choice']
    sql_query = f"UPDATE polls_choice SET votes = votes + 1 WHERE id = {choice_id};"

    with connection.cursor() as cursor:
        cursor.execute(sql_query)

    # A04:2021 - Insecure Design: Users can vote multiple times
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    # # This part (lines 54 - 74) contains fixes for A03 and A04 vunerabilities
    # # FIX for A04:2021 - Insecure Design
    # if Vote.objects.filter(user=request.user, question=question).exists():
    #     return render(request, 'polls/detail.html', {
    #         'question': question,
    #         'error_message': "You've already voted on this question..",
    #     })

    # try:
    #     # FIX for A03:2021 - Injection
    #     choice = question.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     return render(request, 'polls/detail.html', {
    #         'question': question,
    #         'error_message': "You didn't select a valid choice.",
    #     })

    # choice.votes += 1
    # choice.save()

    # Vote.objects.create(user=request.user, question=question, choice=choice)

    # return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
