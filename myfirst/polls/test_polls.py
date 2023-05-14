import datetime

from django.utils import timezone

from .models import Question


class TestPublished:
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        assert not future_question.was_published_recently()

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        future_question = Question(pub_date=time)
        assert not future_question.was_published_recently()

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(minutes=1)
        future_question = Question(pub_date=time)
        assert future_question.was_published_recently()
