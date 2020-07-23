import pytest
from api.models import Comment


class TestCommentAPI:

    @pytest.mark.django_db(transaction=True)
    def test_comments_not_found(self, user_client, post):
        response = user_client.get(f'/api/v1/posts/{post.id}/comments/')

        assert response.status_code != 404, \
            'The page `/api/v1/posts/{post.id}/comments/` is not found, check it in *urls.py*'

    @pytest.mark.django_db(transaction=True)
    def test_comments_get(self, user_client, post, comment_1_post, comment_2_post, comment_1_another_post):
        response = user_client.get(f'/api/v1/posts/{post.id}/comments/')

        assert response.status_code == 200, \
            'Check that the GET request `/api/v1/posts/{post.id}/comments/` ' \
            'with auth token returns 200'
        test_data = response.json()
        assert type(test_data) == list, \
            'Check that the GET request `/api/v1/posts/{post.id}/comments/` returns a list'
        assert len(test_data) == Comment.objects.filter(post=post).count(), \
            'Check that the GET request `/api/v1/posts/{post.id}/comments/` ' \
            'returns a list with post comments'

        comment = Comment.objects.filter(post=post).first()
        test_comment = test_data[0]
        assert 'id' in test_comment, 'Check that the `fields` of the Comment serializer have an `id` title'
        assert 'text' in test_comment, \
            'Check that the `fields` of the Comment serializer have an `text` title'
        assert 'author' in test_comment, \
            'Check that the `fields` of the Comment serializer have an `author` title'
        assert 'post' in test_comment, \
            'Check that the `fields` of the Comment serializer have an `post` title'
        assert 'created' in test_comment, \
            'Check that the `fields` of the Comment serializer have an `created` title'
        assert test_comment['author'] == comment.author.username, \
            'Check that the `author` field of the Comment serializer returns the username'
        assert test_comment['id'] == comment.id, \
            'Check that the GET request `/api/v1/posts/{post.id}/comments/` returns list of all posts'

    @pytest.mark.django_db(transaction=True)
    def test_comments_create(self, user_client, post, user, another_user):
        comments_count = Comment.objects.count()

        data = {}
        response = user_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        assert response.status_code == 400, \
            'Check that the POST request `/api/v1/posts/{post.id}/comments/` ' \
            'with a wrong data returns 400'

        data = {'author': another_user.id, 'text': 'Новый коммент 1233', 'post': post.id}
        response = user_client.post(f'/api/v1/posts/{post.id}/comments/', data=data)
        assert response.status_code == 201, \
            'Check that the POST request `/api/v1/posts/{post.id}/comments/` ' \
            'returns 201'

        test_data = response.json()
        msg_error = 'Check that the POST request `/api/v1/posts/{post.id}/comments/` ' \
                    'returns a dict with comment data'
        assert type(test_data) == dict, msg_error
        assert test_data.get('text') == data['text'], msg_error

        assert test_data.get('author') == user.username, \
            'Check that the POST request `/api/v1/posts/{post.id}/comments/` ' \
            'a comment from an authorized user is created'
        assert comments_count + 1 == Comment.objects.count(), \
            'Check that the POST request `/api/v1/posts/{post.id}/comments/` comment is created'

    @pytest.mark.django_db(transaction=True)
    def test_comment_get_current(self, user_client, post, comment_1_post, user):
        response = user_client.get(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/')

        assert response.status_code == 200, \
            'The page `/api/v1/posts/{post.id}/comments/{comment.id}/` is not found, ' \
            'check it in *urls.py*'

        test_data = response.json()
        assert test_data.get('text') == comment_1_post.text, \
            'Check that the GET request `/api/v1/posts/{post.id}/comments/{comment.id}/` ' \
            'returns a serialized data. The `text` value is wrong or not found'
        assert test_data.get('author') == user.username, \
            'Check that the GET request `/api/v1/posts/{post.id}/comments/{comment.id}/` ' \
            'returns a serialized data. The `author` value is wrong or not found'
        assert test_data.get('post') == post.id, \
            'Check that the GET request `/api/v1/posts/{post.id}/comments/{comment.id}/` ' \
            'returns a serialized data. The `post` value is wrong or not found'

    @pytest.mark.django_db(transaction=True)
    def test_comment_patch_current(self, user_client, post, comment_1_post, comment_2_post):
        response = user_client.patch(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/',
                                     data={'text': 'Changed the comment'})

        assert response.status_code == 200, \
            'Check that the PATCH request `/api/v1/posts/{post.id}/comments/{comment.id}/` ' \
            'returns 200'

        test_comment = Comment.objects.filter(id=comment_1_post.id).first()

        assert test_comment, \
            "Check that the PATCH request `/api/v1/posts/{post.id}/comments/{comment.id}/` " \
            "hasn't deleted the comment"

        assert test_comment.text == 'Changed the comment', \
            'Check that the PATCH request `/api/v1/posts/{id}/` changes the post'

        response = user_client.patch(f'/api/v1/posts/{post.id}/comments/{comment_2_post.id}/',
                                     data={'text': 'Changed the post'})

        assert response.status_code == 403, \
            'Check that the PATCH request `/api/v1/posts/{post.id}/comments/{comment.id}/` ' \
            "for someone else's posts returns 403"

    @pytest.mark.django_db(transaction=True)
    def test_comment_delete_current(self, user_client, post, comment_1_post, comment_2_post):
        response = user_client.delete(f'/api/v1/posts/{post.id}/comments/{comment_1_post.id}/')

        assert response.status_code == 204, \
            'Check that the DELETE request `/api/v1/posts/{post.id}/comments/{comment.id}/` returns 204'

        test_comment = Comment.objects.filter(id=post.id).first()

        assert not test_comment, \
            'Check that the DELETE request `/api/v1/posts/{post.id}/comments/{comment.id}/` has delete the comment'

        response = user_client.delete(f'/api/v1/posts/{post.id}/comments/{comment_2_post.id}/')

        assert response.status_code == 403, \
            'Check that the DELETE request `/api/v1/posts/{post.id}/comments/{comment.id}/` ' \
            "for someone else's comments returns 403"
