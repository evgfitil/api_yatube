import pytest
from api.models import Follow


class TestFollowAPI:

    @pytest.mark.django_db(transaction=True)
    def test_follow_not_found(self, client, follow_1, follow_2):
        response = client.get('/api/v1/follow/')

        assert response.status_code != 404, 'The page `/api/v1/follow/` is not found, check it in *urls.py*'

    @pytest.mark.django_db(transaction=True)
    def test_follow_not_auth(self, client, follow_1, follow_2):
        response = client.get('/api/v1/follow/')
        assert response.status_code == 200,\
            'Check that the request `/api/v1/follow/` without token returns 200'

    @pytest.mark.django_db(transaction=True)
    def test_follow_get(self, user_client, follow_1, follow_2, follow_3):
        response = user_client.get('/api/v1/follow/')
        assert response.status_code == 200, \
            'Check that the GET request `/api/v1/follow/` with token returns 200'

        test_data = response.json()

        assert type(test_data) == list, 'Check that the GET request `/api/v1/follow/` returns a list'

        assert len(test_data) == Follow.objects.count(), \
            'Check that the GET request `/api/v1/follow/` returns a followers list'

        follow = Follow.objects.all()[0]
        test_group = test_data[0]
        assert 'user' in test_group, \
            'Check that the `fields` of the Follow serializer have an `user` title'
        assert 'following' in test_group, \
            'Check that the `fields` of the Comment serializer have an `following` title'

        assert test_group['user'] == follow.user.username, \
            'Check that the GET request `/api/v1/follow/` returns a following list '
        assert test_group['following'] == follow.following.username, \
            'Check that the GET request `/api/v1/follow/` returns a following list '

    @pytest.mark.django_db(transaction=True)
    def test_follow_create(self, user_client, follow_2, follow_3, user, user_2, another_user):
        follow_count = Follow.objects.count()

        data = {}
        response = user_client.post('/api/v1/follow/', data=data)
        assert response.status_code == 400, \
            'Check that the POST request `/api/v1/follow/` with a wrong data returns 400'

        data = {'following': another_user.username}
        response = user_client.post('/api/v1/follow/', data=data)
        assert response.status_code == 201, \
            'Check that the POST request `/api/v1/follow/` returns 201'

        test_data = response.json()

        msg_error = 'Check that the POST request `/api/v1/follow/` returns a dict with the following data'
        assert type(test_data) == dict, msg_error
        assert test_data.get('user') == user.username, msg_error
        assert test_data.get('following') == data['following'], msg_error

        assert follow_count + 1 == Follow.objects.count(), \
            'Check that the POST request `/api/v1/group/` creates a group'

        response = user_client.post('/api/v1/follow/', data=data)
        assert response.status_code == 400, \
            'Check that the POST request `/api/v1/follow/` ' \
            'with the resubscription returns 400'

    @pytest.mark.django_db(transaction=True)
    def test_follow_search_filter(self, user_client, follow_1, follow_2, follow_3, follow_4,
                                  user, user_2, another_user):
        follow_count = Follow.objects.count()

        response = user_client.get('/api/v1/follow/')
        assert response.status_code == 200, \
            'The page `/api/v1/follow/` is not found, check it in *urls.py*'
        test_data = response.json()
        assert len(test_data) == 4, \
            'Check that the GET request `/api/v1/follow/` returns the following list'

        response = user_client.get(f'/api/v1/follow/?search={user.username}')
        assert len(response.json()) == 2, \
            'Check that the GET request with a `search` query at `/api/v1/follow/` ' \
            'returns the correct following list'

        response = user_client.get(f'/api/v1/follow/?search={user_2.username}')
        assert len(response.json()) == 3, \
            'Check that the GET request with a `search` query at `/api/v1/follow/` ' \
            'returns the correct following list'
