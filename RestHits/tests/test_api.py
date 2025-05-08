import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from hits.models import Hit, Artist


def print_title(message):
    print(f'\n*** {message} ***')


# @pytest.fixture
# def api_client():
#     return APIClient()
#
#
# @pytest.fixture
# def create_artist():
#     return Artist.objects.create(first_name="Robert", last_name="Winek")
#
#
# @pytest.fixture
# def create_hit(create_artist):
#     return Hit.objects.create(title="Create Hit", artist_id=create_artist, title_url="create-hit")


@pytest.mark.django_db
def test_start():
    api_client = APIClient()
    print_title('test_get_hits')
    call_get_hits(api_client)

    artist = Artist.objects.create(first_name="Witold", last_name="Rybak")
    print_title('test_create_hit')
    call_create_hit(api_client, artist, 'Muchy')

    artist = Artist.objects.create(first_name="Robert", last_name="Winek")
    print_title('test_create_hit')
    hit = call_create_hit(api_client, artist, 'Osy')

    # odświeżenie danych
    hit.refresh_from_db()

    print_title('test_get_hits')
    call_get_hits(api_client)

    print_title('test_get_hit_detail')
    call_get_hit_detail(api_client, hit)
    
    print_title('test_update_hit')
    call_update_hit(api_client, hit)

    print_title('test_get_hits')
    call_get_hits(api_client)

    hit.refresh_from_db()
    
    print_title('test_delete_hit')
    _test_delete_hit(api_client, hit)

    print_title('test_get_hits')
    call_get_hits(api_client)
    

# test [GET] /api/v1/hits
@pytest.mark.django_db
def call_get_hits(api_client):
    url = reverse('hits-list')
    response = api_client.get(url)
    print('test_get_hits:', response.data)
    print('length:', len(response.data))
    print('status_code:', response.status_code)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) <= 20


# test [GET] /api/v1/hits/{title_url}
@pytest.mark.django_db
def call_get_hit_detail(api_client, hit):
    url = reverse('hit-detail', kwargs={'title_url': hit.title_url})
    response = api_client.get(url)
    print('test_get_hit_detail:', response.data)  # Wyświetl szczegółów
    print('status_code:', response.status_code)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == hit.title
    artist = response.data.get('artist')
    assert artist is not None, "Missing 'artist' field in the response"
    assert 'first_name' in artist, "Missing 'first_name' inside 'artist'"
    assert 'last_name' in artist, "Missing 'last_name' inside 'artist'"
    assert artist['first_name'] == hit.artist_id.first_name
    assert artist['last_name'] == hit.artist_id.last_name


# test [POST] /api/v1/hits
@pytest.mark.django_db
def call_create_hit(api_client, artist, title):
    url = reverse('hits-list')

    data = {
        'artist_id': artist.id,
        'title': title
    }
    
    response = api_client.post(url, data, format='json')
    print('test_create_hit:', response.data)  # Wyświetl szczegółów
    print('status_code:', response.status_code)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == title

    hit = Hit.objects.select_related('artist_id').get(id=response.data['id'])

    return hit


# test [PUT] /api/v1/hits/{title_url}
@pytest.mark.django_db
def call_update_hit(api_client, hit):
    url = reverse('hit-detail', kwargs={'title_url': hit.title_url})

    data = {
        'artist_id': hit.artist_id.id,
        'title': 'Updated Hit'
    }

    response = api_client.put(url, data, format='json')
    print('test_update_hit:', response.data)  # Wyświetl szczegółów
    print('status_code:', response.status_code)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'Updated Hit'


# test  [DELETE] /api/v1/hits/{title_url}
@pytest.mark.django_db
def _test_delete_hit(api_client, hit):
    url = reverse('hit-detail', kwargs={'title_url': hit.title_url})
    response = api_client.delete(url)
    print('test_delete_hit:', response.data)  # Wyświetl szczegółów
    print('status_code:', response.status_code)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    with pytest.raises(Hit.DoesNotExist):
        hit.refresh_from_db()  # Sprawdź, czy będzie wyjątek dla usuniętego obiektu


@pytest.mark.django_db
def test_error_create_hit():
    print_title('error_test_create_hit')
    api_client = APIClient()

    # Brak danych: 'artist_id' i 'title'
    response = api_client.post(reverse('hits-list'), {}, format='json')
    print('error_test_create_hit:', response.data)
    print('status_code:', response.status_code)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'artist_id' in response.data
    assert 'title' in response.data


@pytest.mark.django_db
def test_error_get_hit_detail():
    print_title('error_test_get_hit_detail')
    api_client = APIClient()

    url = reverse('hit-detail', kwargs={'title_url': 'non-existent-hit'})
    response = api_client.get(url)
    print('error_test_get_hit_detail:', response.data)
    print('status_code:', response.status_code)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_error_update_hit():
    print_title('error_test_update_hit')
    api_client = APIClient()

    url = reverse('hit-detail', kwargs={'title_url': 'non-existent-hit'})
    data = {
        'title': 'Invalid Update',
        'artist_id': 9999
    }

    response = api_client.put(url, data, format='json')
    print('error_test_update_hit:', response.data)
    print('status_code:', response.status_code)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_error_delete_hit():
    print_title('error_test_delete_hit')
    api_client = APIClient()

    url = reverse('hit-detail', kwargs={'title_url': 'non-existent-hit'})
    response = api_client.delete(url)
    print('error_test_delete_hit:', response.data)
    print('status_code:', response.status_code)
    assert response.status_code == status.HTTP_404_NOT_FOUND
