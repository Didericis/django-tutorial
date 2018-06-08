from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future), and limit to public questions if the user is
        not logged in
        """
        question_set = Question.objects.filter(pub_date__lte=timezone.now())
        if not self.request.user.is_authenticated:
            question_set = question_set.filter(private=False)
        return question_set.order_by('-pub_date')[:5]

class QuestionView(UserPassesTestMixin, generic.DetailView):
    model = Question
    login_url = 'auth_app:login'
    def test_func(self):
        if self.get_object().private and not self.request.user.is_authenticated:
            return False
        return True

class DetailView(QuestionView):
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(QuestionView):
    template_name = 'polls/results.html'

def profile(request):
    return render(request, 'polls/profile.html', {
        'user': request.user,
        'published_questions': Question.objects.published()
    })

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        request.user.vote(selected_choice)
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
