from django.test import TestCase
from rest_framework.test import APIRequestFactory

from melowdee.core.album.models import Album
from melowdee.core.album.views import AlbumViewSet
from melowdee.core.artist.models import Artist


class AlbumTestCase(TestCase):

    def test_add_album(self):
        factory = APIRequestFactory()
        album_name = 'Ride the lighting'
        about = 'Greatness'
        artist = Artist.objects.create(name='Metallica')
        request = factory.post('/albums/', {
                'name': album_name,
                'about': about,
                'artist_id': artist.id
            }, format='json'
        )
        response = AlbumViewSet().albums(request)

        album = Album.objects.filter(name=album_name)
        assert album.exists() is True
        assert album.count() == 1
        assert album.first().name == album_name
        assert album.first().about == about
        assert response.status_code == 201

    def test_all_artist_albums(self):
        factory = APIRequestFactory()
        album = 'Ride the lighting'
        about = 'Greatness'
        artist = Artist.objects.create(name='Metallica')
        request = factory.post('/albums/', {
                'name': album,
                'about': about,
                'artist_id': artist.id
            }, format='json'
        )

        AlbumViewSet().albums(request)

        request = factory.get(
            f'/albums?artist_id={artist.id}',
            format='json'
        )
        response = AlbumViewSet().albums(request)
        assert response.status_code == 200
        print(response._container)
        assert album in str(response._container)
