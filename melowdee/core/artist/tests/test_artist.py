from django.test import TestCase
from rest_framework.test import APIRequestFactory

from melowdee.core.artist.models import Artist
from melowdee.core.artist.views import add_artist, all_artists


class ArtistTestCase(TestCase):

    def test_add_artist(self):
        factory = APIRequestFactory()
        artist = 'The Strokes'
        about = 'Greatness'
        request = factory.post('/add_artist/', {
            'name': artist,
            'about': about,
        }, format='json')
        response = add_artist(request)

        art = Artist.objects.filter(name=artist)
        assert art.exists() is True
        assert art.count() == 1
        assert response.status_code == 201

    def test_all_artists(self):
        factory = APIRequestFactory()
        artist = 'Biggie Smalls'
        about = 'Greatness'

        request = factory.post('/add_artist/', {
            'name': artist,
            'about': about,
        }, format='json')
        add_artist(request)

        request = factory.get('/all_artists/', format='json')
        response = all_artists(request)

        assert response.status_code == 200
        assert artist in str(response._container)
