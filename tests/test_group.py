import pytest
from api.models import Group


class TestGroupAPI:

    @pytest.mark.django_db(transaction=True)
    def test_group_not_found(self, client, post, group_1):
        response = client.get('/api/v1/group/')

        assert response.status_code != 404, 'The page `/api/v1/group/` is not found, check it in *urls.py*'

    @pytest.mark.django_db(transaction=True)
    def test_group_not_auth(self, client, post, group_1):
        response = client.get('/api/v1/group/')
        assert response.status_code == 200,\
            'Check that the GET request `/api/v1/group/` without token returns 200'

    @pytest.mark.django_db(transaction=True)
    def test_group_get(self, user_client, post, another_post, group_1, group_2):
        response = user_client.get('/api/v1/group/')
        assert response.status_code == 200, \
            'Check that the GET request `/api/v1/group/` with token returns 200'

        test_data = response.json()

        assert type(test_data) == list, 'Check that the GET request `/api/v1/group/` returns a list'

        assert len(test_data) == Group.objects.count(), \
            'Check that the GET request `/api/v1/group/` returns a list of all groups'

        group = Group.objects.all()[0]
        test_group = test_data[0]
        assert 'id' in test_group, 'Check that the `fields` of the Group serializer have an `id` title'
        assert 'title' in test_group, \
            'Check that the `fields` of the Group serializer have an `title` title'

        assert test_group['id'] == group.id, \
            'Check that the GET request `/api/v1/group/` returns a list fo all groups'

    @pytest.mark.django_db(transaction=True)
    def test_group_create(self, user_client, group_1, group_2):
        group_count = Group.objects.count()

        data = {}
        response = user_client.post('/api/v1/group/', data=data)
        assert response.status_code == 400, \
            'Check that the POST request `/api/v1/group/` with the wrong data returns 400'

        data = {'title': 'Group number 3'}
        response = user_client.post('/api/v1/group/', data=data)
        assert response.status_code == 201, \
            'Check that the POST request `/api/v1/group/` returns 200'

        test_data = response.json()

        msg_error = 'Check that the POST request `/api/v1/group/` returns a dict with a group data'
        assert type(test_data) == dict, msg_error
        assert test_data.get('title') == data['title'], msg_error

        assert group_count + 1 == Group.objects.count(), \
            'Check that the POST request `/api/v1/group/` create a group'

    @pytest.mark.django_db(transaction=True)
    def test_group_get_post(self, user_client, post, post_2, another_post, group_1, group_2):
        response = user_client.get(f'/api/v1/posts/')
        assert response.status_code == 200, \
            'The page `/api/v1/posts/` is not found, check it in *urls.py*'
        test_data = response.json()
        assert len(test_data) == 3, \
            'Check that the GET request `/api/v1/posts/` returns a list of posts'

        response = user_client.get(f'/api/v1/posts/?group={group_2.id}')
        assert len(response.json()) == 1, \
            'Check that the GET request with the `group` query on `/api/v1/posts/` ' \
            'returns a group posts'

        response = user_client.get(f'/api/v1/posts/?group={group_1.id}')
        assert len(response.json()) == 2, \
            'Check that the GET request with the `group` query on `/api/v1/posts/` ' \
            'returns a group posts'