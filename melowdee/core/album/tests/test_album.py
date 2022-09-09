from django.test import TestCase
from rest_framework.test import APIRequestFactory

from melowdee.core.album.models import Album
from melowdee.core.album.views import add_album, get_albums_for_artist
from melowdee.core.artist.models import Artist


class AlbumTestCase(TestCase):

    def test_add_album(self):
        factory = APIRequestFactory()
        album_name = 'Ride the lighting'
        about = 'Greatness'
        artist = Artist.objects.create(name='Metallica')
        request = factory.post('/add_album/', {
                'name': album_name,
                'about': about,
                'artist_id': artist.id
            }, format='json'
        )
        response = add_album(request)

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
        request = factory.post('/add_album/', {
                'name': album,
                'about': about,
                'artist_id': artist.id
            }, format='json'
        )
        add_album(request)

        request = factory.get(
            f'/get_albums_for_artist?artist_id={artist.id}',
            format='json'
        )
        response = get_albums_for_artist(request)
        assert response.status_code == 200
        assert album in str(response._container)
