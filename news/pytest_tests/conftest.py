
import pytest

from datetime import datetime, timedelta

from django.conf import settings
from django.test.client import Client
from django.urls import reverse

from news.models import News, Comment


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def anonymous_client():
    client = Client()
    return client


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(author):
    news = News.objects.create(
        title='Тестовая новость',
        text='Просто текст.',
    )
    return news


@pytest.fixture
def news_factory():
    today = datetime.today()
    all_news = [
        News(
            title=f'Тестовая новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария'
    )
    return comment


@pytest.fixture
def comment_form_data(author, news):
    return {
        'news': news,
        'author': author,
        'text': 'Новый текст',
    }


@pytest.fixture
def comment_factory(author, news):
    today = datetime.today()
    all_comments = [
        Comment(
            news=news,
            author=author,
            text='Текст комментария',
            created=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    Comment.objects.bulk_create(all_comments)


@pytest.fixture
def news_id_for_args(news):
    return (news.id,)


@pytest.fixture
def comment_id_for_args(comment):
    return (comment.id,)


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def comment_del_url(comment):
    return reverse('news:delete', args=(comment.id,))


@pytest.fixture
def comment_edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def comments_url(detail_url):
    return detail_url + '#comments'
