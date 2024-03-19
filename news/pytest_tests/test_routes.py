import pytest
from http import HTTPStatus
from news.models import News

from django.urls import reverse


def test_note_exists(news):
    notes_count = News.objects.count()
    # Общее количество заметок в БД равно 1.
    assert notes_count == 1
    # Заголовок объекта, полученного при помощи фикстуры note,
    # совпадает с тем, что указан в фикстуре.
    assert news.title == 'Заголовок'


# Обозначаем, что тесту нужен доступ к БД. 
# Без этой метки тест выдаст ошибку доступа к БД.
@pytest.mark.django_db
def test_empty_db():
    notes_count = News.objects.count()
    # В пустой БД никаких заметок не будет:
    assert notes_count == 0