import pytest
from api.models import Post


class TestPostAPI:

    @pytest.mark.django_db(transaction=True)
    def test_post_not_found(self, client, post):
        response = client.get('/api/v1/posts/')

        assert response.status_code != 404, 'The page `/api/v1/posts/` is not found, check it in *urls.py*'

    @pytest.mark.django_db(transaction=True)
    def test_post_not_auth(self, client, post):
        response = client.get('/api/v1/posts/')

        assert response.status_code == 200,\
            'Check that the GET request `/api/v1/posts/` without token returns 200'

    @pytest.mark.django_db(transaction=True)
    def test_posts_get(self, user_client, post, another_post):
        response = user_client.get('/api/v1/posts/')
        assert response.status_code == 200, \
            'Check that the GET request `/api/v1/posts/` with token returns 200'

        test_data = response.json()

        assert type(test_data) == list, 'Check that the GET request `/api/v1/posts/` returns a list'

        assert len(test_data) == Post.objects.count(), \
            'Check that the GET request `/api/v1/posts/` returns a posts list'

        post = Post.objects.all()[0]
        test_post = test_data[0]
        assert 'id' in test_post, 'Check that the `fields` of the Post serializer have an `id` title'
        assert 'text' in test_post, 'Check that the `fields` of the Post serializer have an `text` title'
        assert 'author' in test_post, \
            'Check that the `fields` of the Post serializer have an `author` title'
        assert 'pub_date' in test_post, \
            'Check that the `fields` of the Post serializer have an `pub_date` title'
        assert test_post['author'] == post.author.username, \
            'Check that the `author` field of the Post serializer returns the username'

        assert test_post['id'] == post.id, \
            'Check that the GET request `/api/v1/posts/` returns posts list'

    @pytest.mark.django_db(transaction=True)
    def test_post_create(self, user_client, user, another_user):
        post_count = Post.objects.count()

        data = {}
        response = user_client.post('/api/v1/posts/', data=data)
        assert response.status_code == 400, \
            'Check that the POST request `/api/v1/posts/` with the wrong data returns 400'

        data = {'author': another_user.id, 'text': 'Статья номер 3'}
        response = user_client.post('/api/v1/posts/', data=data)
        assert response.status_code == 201, \
            'Check that the POST request `/api/v1/posts/` returns 201'

        test_data = response.json()

        msg_error = 'Check that the POST request `/api/v1/posts/` returns a dict with the post data'
        assert type(test_data) == dict, msg_error
        assert test_data.get('text') == data['text'], msg_error

        assert test_data.get('author') == user.username, \
            'Check that the POST request `/api/v1/posts/` post is created'
        assert post_count + 1 == Post.objects.count(), \
            'Check that the POST request `/api/v1/posts/` post is created'

    @pytest.mark.django_db(transaction=True)
    def test_post_get_current(self, user_client, post, user):
        response = user_client.get(f'/api/v1/posts/{post.id}/')

        assert response.status_code == 200, \
            'The page `/api/v1/posts/{id}/` is not found, check it in *urls.py*'

        test_data = response.json()
        assert test_data.get('text') == post.text, \
            'Check that the GET request `/api/v1/posts/{id}/` returns a serialized data, ' \
            '`text` value is wrong or not found'
        assert test_data.get('author') == user.username, \
            'Check that the GET request `/api/v1/posts/{id}/` returns a serialized data, ' \
            '`author` value is wrong or not found'

    @pytest.mark.django_db(transaction=True)
    def test_post_patch_current(self, user_client, post, another_post):
        response = user_client.patch(f'/api/v1/posts/{post.id}/',
                                     data={'text': 'Text is changed'})

        assert response.status_code == 200, \
            'Check that the PATCH request `/api/v1/posts/{id}/` returns 200'

        test_post = Post.objects.filter(id=post.id).first()

        assert test_post, 'Check that the PATCH request `/api/v1/posts/{id}/` does not delete the post'

        assert test_post.text == 'Text is changed', \
            'Check tha the PATCH request `/api/v1/posts/{id}/` changes the post'

        response = user_client.patch(f'/api/v1/posts/{another_post.id}/',
                                     data={'text': 'Text is changed'})

        assert response.status_code == 403, \
            "Check that the PATCH request `/api/v1/posts/{id}/` for someone's post returns 403"

    @pytest.mark.django_db(transaction=True)
    def test_post_delete_current(self, user_client, post, another_post):
        response = user_client.delete(f'/api/v1/posts/{post.id}/')

        assert response.status_code == 204, \
            'Check that the DELETE request `/api/v1/posts/{id}/` returns 204'

        test_post = Post.objects.filter(id=post.id).first()

        assert not test_post, 'Check that the DELETE request `/api/v1/posts/{id}/` delete the post'

        response = user_client.delete(f'/api/v1/posts/{another_post.id}/')

        assert response.status_code == 403, \
            "Check that the DELETE request `/api/v1/posts/{id}/` for someone's post returns 403"
