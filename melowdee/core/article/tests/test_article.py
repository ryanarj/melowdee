from django.test import TestCase
from rest_framework.test import APIRequestFactory

from melowdee.core.article.models import Article
from melowdee.core.article.views import add_article
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
        request = factory.post('/add_article/', {
                'title': title,
                'description': description,
                'artist_id': artist.id
            }, format='json'
        )
        response = add_article(request)

        article = Article.objects.filter(title=title, artist_id=artist.id)
        assert article.exists() is True
        assert article.count() == 1
        assert article.first().title == title
        assert article.first().description == description
        assert response.status_code == 201