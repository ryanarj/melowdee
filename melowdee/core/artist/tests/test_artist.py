from django.test import TestCase
from rest_framework.test import APIRequestFactory

from melowdee.core.artist.models import Artist
from melowdee.core.artist.views import ArtistViewSet


class ArtistTestCase(TestCase):

    def test_add_artist(self):
        factory = APIRequestFactory()
        artist = 'The Strokes'
        about = 'Greatness'
        request = factory.post('/artists/', {
            'name': artist,
            'about': about,
        }, format='json')
        response = ArtistViewSet().artists(request)

        art = Artist.objects.filter(name=artist)
        assert art.exists() is True
        assert art.count() == 1
        assert response.status_code == 201

    def test_all_artists(self):
        factory = APIRequestFactory()
        artist = 'Biggie Smalls'
        about = 'Greatness'

        request = factory.post('/artists/', {
            'name': artist,
            'about': about,
        }, format='json')
        ArtistViewSet().artists(request)

        request = factory.get('/artists/all', format='json')
        response = ArtistViewSet().all_artists(request)

        assert response.status_code == 200
        assert artist in str(response._container)
