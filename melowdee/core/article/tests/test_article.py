from django.test import TestCase
from rest_framework.test import APIRequestFactory

from melowdee.core.article.models import Article
from melowdee.core.article.views import articles
from melowdee.core.artist.models import Artist


class AlbumTestCase(TestCase):

    def test_add_album(self):
        factory = APIRequestFactory()
        title = 'Ride the lighting'
        description = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut ' \
                      'labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco ' \
                      'laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in v' \
                      'oluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat ' \
                      'non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'

        artist = Artist.objects.create(name='Metallica')
        request = factory.post('/articles/add/', {
                'title': title,
                'description': description,
                'artist_id': artist.id
            }, format='json'
        )
        response = articles(request)

        article_q = Article.objects.filter(title=title, artist_id=artist.id)
        assert article_q.exists() is True
        assert article_q.count() == 1
        assert article_q.first().title == title
        assert article_q.first().description == description
        assert response.status_code == 201
