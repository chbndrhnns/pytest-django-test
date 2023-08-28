import datetime
from http import HTTPStatus

import pytest
from django.test import Client
from django.urls import reverse
from django.utils import timezone

from .models import Question

pytestmark = pytest.mark.anyio


@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"


@pytest.fixture
def client():
    return Client()


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


@pytest.mark.django_db
class TestView:
    async def test_no_question(self, async_client):
        res = await async_client.get(reverse("polls:index"))
        assert res.status_code == HTTPStatus.OK
        assert "No questions are available" in str(res.content)
        assert len(res.context["latest_question_list"]) == 0
