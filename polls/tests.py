import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User, AnonymousUser
from .models import Question, Choice, Vote

def create_question(question_text, days, private=False):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(
        question_text=question_text, 
        pub_date=time, 
        private=private
     )

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_private_question(self):
        """
        Private questions are not displaed when logged out
        """
        create_question(question_text="Private question", days=-30, private=True)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Private question")

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionDetailViewTests(TestCase):
    def test_private_question(self):
        """
        Private questions are not displaed when logged out
        """
        private_question = create_question(
            question_text="Private question", 
            days=-30, 
            private=True
        )
        url = reverse('polls:detail', args=(private_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionModelTests(TestCase):
    def test_published(self):
        """
        published() returns questions whose pub_date is in the past
        """
        future_time = timezone.now() + datetime.timedelta(days=30)
        past_time = timezone.now() + datetime.timedelta(days=-30)
        future_question = Question.objects.create(pub_date=future_time)
        past_question = Question.objects.create(pub_date=past_time)
        published_questions = Question.objects.published()
        self.assertIn(past_question, published_questions)
        self.assertNotIn(future_question, published_questions)

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class ChoiceModelTests(TestCase):
    def test_votes_for_user(self):
        """
        votes_for_user() returns number of votes for a given user
        """
        time = timezone.now() - datetime.timedelta(days=10)
        past_question = Question.objects.create(
            pub_date=time, 
            question_text="Question"
        )
        choice_1 = Choice.objects.create(
            question=past_question, 
            choice_text="Choice 1"
        )
        choice_2 = Choice.objects.create(
            question=past_question, 
            choice_text="Choice 2"
        )
        user_1 = User.objects.create_user(
            username='bm', 
            first_name="Bob", 
            last_name="Marley"
        )
        user_2 = User.objects.create_user(
            username="ck",
            first_name="Carole", 
            last_name="King"
        )
        user_3 = User.objects.create_user(
            username="dr",
            first_name="Daniel", 
            last_name="Radcliff"
        )
        user_1.vote(choice_1)
        user_1.vote(choice_1)
        user_2.vote(choice_2)
        self.assertIs(choice_1.num_votes_by_user(user_1), 2)
        self.assertIs(choice_1.num_votes_by_user(user_2), 0)
        self.assertIs(choice_1.num_votes_by_user(user_3), 0)
        self.assertIs(choice_2.num_votes_by_user(user_1), 0)
        self.assertIs(choice_2.num_votes_by_user(user_2), 1)
        self.assertIs(choice_2.num_votes_by_user(user_3), 0)

class AnonymousUserVote(TestCase):
    def test_vote(self):
        """
        vote() receives a choice, ups the votes integer for the choice and adds
        a vote record
        """
        time = timezone.now() - datetime.timedelta(days=10)
        past_question = Question.objects.create(pub_date=time, question_text="How are you?")
        choice = Choice.objects.create(question=past_question, choice_text="Awesome")
        # TODO: figure out if there is a better way to assert changes
        self.assertIs(choice.votes, 0)
        self.assertIs(Vote.objects.count(), 0)
        user = AnonymousUser()
        vote = user.vote(choice)
        self.assertIs(choice.votes, 1)
        self.assertIs(Vote.objects.count(), 1)
        self.assertIs(vote.choice, choice)

class UserModelTests(TestCase):
    def test_vote(self):
        """
        vote() receives a choice, ups the votes integer for the choice and adds
        a vote record
        """
        time = timezone.now() - datetime.timedelta(days=10)
        past_question = Question.objects.create(pub_date=time, question_text="How are you?")
        choice = Choice.objects.create(question=past_question, choice_text="Awesome")
        user = User.objects.create(first_name="Bob", last_name="Marley")
        # TODO: figure out if there is a better way to assert changes
        self.assertIs(choice.votes, 0)
        self.assertIs(Vote.objects.count(), 0)
        vote = user.vote(choice)
        self.assertIs(choice.votes, 1)
        self.assertIs(Vote.objects.count(), 1)
        self.assertIs(vote.choice, choice)
        self.assertIs(vote.user, user)

        new_vote = user.vote(choice)
        self.assertIs(Vote.objects.count(), 2)
        self.assertIs(choice.votes, 2)
        self.assertIsNot(new_vote.id, vote.id)
