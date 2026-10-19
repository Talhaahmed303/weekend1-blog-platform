import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.posts.models import Category, Post
from apps.comments.models import Comment

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def db_setup(db):
    admin = User.objects.create_user(
        username='admin_test',
        email='admin@test.com',
        password='Password@123',
        role='admin',
        is_staff=True
    )
    author1 = User.objects.create_user(
        username='author1_test',
        email='author1@test.com',
        password='Password@123',
        role='author'
    )
    author2 = User.objects.create_user(
        username='author2_test',
        email='author2@test.com',
        password='Password@123',
        role='author'
    )
    category = Category.objects.create(name='Tech', slug='tech', description='Technology topics')
    
    pub_post = Post.objects.create(
        title='Published Post by Author 1',
        content='Deep technical breakdown of microservices and DRF.',
        author=author1,
        category=category,
        status='published'
    )
    
    draft_post = Post.objects.create(
        title='Draft Post by Author 1',
        content='Secret draft not ready for publication.',
        author=author1,
        category=category,
        status='draft'
    )
    
    return {
        'admin': admin,
        'author1': author1,
        'author2': author2,
        'category': category,
        'pub_post': pub_post,
        'draft_post': draft_post
    }

# --- 1. Positive Tests ---

@pytest.mark.django_db
def test_user_registration_success(api_client):
    url = reverse('auth_register')
    payload = {
        'username': 'new_writer',
        'email': 'writer@test.com',
        'password': 'SecurePassword@123',
        'role': 'author',
        'bio': 'Passionate blogger'
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 201
    assert response.data['success'] is True
    assert response.data['data']['username'] == 'new_writer'
    assert User.objects.filter(username='new_writer').exists()

@pytest.mark.django_db
def test_user_registration_with_spaces_in_username(api_client):
    url = reverse('auth_register')
    payload = {
        'username': 'Ahsan khan',
        'password': 'SecurePassword@123',
        'role': 'author'
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 201
    assert response.data['success'] is True
    assert response.data['data']['username'] == 'Ahsan khan'
    assert User.objects.filter(username='Ahsan khan').exists()

    # Also verify login works with the username
    login_url = reverse('auth_login')
    login_res = api_client.post(login_url, {'username': 'Ahsan khan', 'password': 'SecurePassword@123'}, format='json')
    assert login_res.status_code == 200
    assert 'access' in login_res.data

@pytest.mark.django_db
def test_user_login_and_jwt_tokens(api_client, db_setup):
    url = reverse('auth_login')
    payload = {
        'username': 'author1_test',
        'password': 'Password@123'
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert response.data['user']['role'] == 'author'

@pytest.mark.django_db
def test_create_published_post_success(api_client, db_setup):
    api_client.force_authenticate(user=db_setup['author1'])
    url = reverse('post-list')
    payload = {
        'title': 'New Architectural Guide',
        'content': 'This post details distributed caching and transactions.',
        'category': db_setup['category'].id,
        'status': 'published'
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 201
    assert response.data['status'] == 'published'
    assert Post.objects.filter(title='New Architectural Guide').exists()

@pytest.mark.django_db
def test_public_feed_returns_published_posts(api_client, db_setup):
    url = reverse('post-list')
    response = api_client.get(url)
    assert response.status_code == 200
    results = response.data['results'] if 'results' in response.data else response.data
    assert len(results) >= 1
    # Check that published post is present
    titles = [p['title'] for p in results]
    assert 'Published Post by Author 1' in titles
    assert 'Draft Post by Author 1' not in titles

@pytest.mark.django_db
def test_search_posts_by_keyword(api_client, db_setup):
    url = f"{reverse('post-list')}?search=microservices"
    response = api_client.get(url)
    assert response.status_code == 200
    results = response.data['results'] if 'results' in response.data else response.data
    assert len(results) == 1
    assert results[0]['title'] == 'Published Post by Author 1'

@pytest.mark.django_db
def test_comment_on_published_post_success(api_client, db_setup):
    api_client.force_authenticate(user=db_setup['author2'])
    url = reverse('comment-list')
    payload = {
        'post': db_setup['pub_post'].id,
        'content': 'Outstanding analysis, very helpful!'
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 201
    assert Comment.objects.filter(content='Outstanding analysis, very helpful!').exists()

# --- 2. Negative Tests ---

@pytest.mark.django_db
def test_registration_with_short_password(api_client):
    url = reverse('auth_register')
    payload = {
        'username': 'bad_user',
        'password': '123'
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_login_with_invalid_credentials(api_client, db_setup):
    url = reverse('auth_login')
    payload = {
        'username': 'author1_test',
        'password': 'WrongPassword123'
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 401

@pytest.mark.django_db
def test_comment_on_draft_post_rejected(api_client, db_setup):
    api_client.force_authenticate(user=db_setup['author2'])
    url = reverse('comment-list')
    payload = {
        'post': db_setup['draft_post'].id,
        'content': 'Attempting to comment on a draft post.'
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 400
    assert 'Cannot add comments to unpublished draft posts' in str(response.data)

# --- 3. Boundary Tests ---

@pytest.mark.django_db
def test_empty_search_returns_all_published(api_client, db_setup):
    url = f"{reverse('post-list')}?search="
    response = api_client.get(url)
    assert response.status_code == 200
    results = response.data['results'] if 'results' in response.data else response.data
    assert len(results) >= 1

@pytest.mark.django_db
def test_search_with_zero_results(api_client, db_setup):
    url = f"{reverse('post-list')}?search=nonexistent_xyz_keyword"
    response = api_client.get(url)
    assert response.status_code == 200
    results = response.data['results'] if 'results' in response.data else response.data
    assert len(results) == 0

@pytest.mark.django_db
def test_blank_title_rejected(api_client, db_setup):
    api_client.force_authenticate(user=db_setup['author1'])
    url = reverse('post-list')
    payload = {
        'title': '   ',
        'content': 'Valid content'
    }
    response = api_client.post(url, payload, format='json')
    assert response.status_code == 400

# --- 4. Permission & Authorization Tests ---

@pytest.mark.django_db
def test_unauthenticated_cannot_see_draft_post(api_client, db_setup):
    url = reverse('post-detail', kwargs={'id': db_setup['draft_post'].id})
    response = api_client.get(url)
    # Draft is hidden from anonymous public -> returns 404
    assert response.status_code == 404

@pytest.mark.django_db
def test_peer_author_cannot_see_other_author_draft(api_client, db_setup):
    api_client.force_authenticate(user=db_setup['author2'])
    url = reverse('post-detail', kwargs={'id': db_setup['draft_post'].id})
    response = api_client.get(url)
    # Hidden from peer author -> 404
    assert response.status_code == 404

@pytest.mark.django_db
def test_author_can_see_own_draft(api_client, db_setup):
    api_client.force_authenticate(user=db_setup['author1'])
    url = reverse('post-detail', kwargs={'id': db_setup['draft_post'].id})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['title'] == 'Draft Post by Author 1'

@pytest.mark.django_db
def test_author_cannot_edit_other_author_post(api_client, db_setup):
    api_client.force_authenticate(user=db_setup['author2'])
    url = reverse('post-detail', kwargs={'id': db_setup['pub_post'].id})
    payload = {'title': 'Hacked Title by Author 2'}
    response = api_client.patch(url, payload, format='json')
    assert response.status_code == 403

@pytest.mark.django_db
def test_admin_can_edit_or_delete_any_post(api_client, db_setup):
    api_client.force_authenticate(user=db_setup['admin'])
    url = reverse('post-detail', kwargs={'id': db_setup['pub_post'].id})
    payload = {'title': 'Moderated Title by Admin'}
    response = api_client.patch(url, payload, format='json')
    assert response.status_code == 200
    assert response.data['title'] == 'Moderated Title by Admin'

# --- 5. Regression & Workflow Tests ---

@pytest.mark.django_db
def test_publish_workflow_action(api_client, db_setup):
    api_client.force_authenticate(user=db_setup['author1'])
    url = reverse('post-publish', kwargs={'id': db_setup['draft_post'].id})
    response = api_client.post(url)
    assert response.status_code == 200
    assert response.data['success'] is True
    assert response.data['data']['status'] == 'published'
    assert response.data['data']['published_at'] is not None

@pytest.mark.django_db
def test_comment_deletion_permissions(api_client, db_setup):
    comment = Comment.objects.create(
        post=db_setup['pub_post'],
        author=db_setup['author2'],
        content='Comment to delete'
    )
    # Unauthenticated user cannot delete
    url = reverse('comment-detail', kwargs={'id': comment.id})
    res_anon = api_client.delete(url)
    assert res_anon.status_code == 401

    # Non-author, non-admin user cannot delete
    other_user = User.objects.create_user(username='rando', password='Password@123')
    api_client.force_authenticate(user=other_user)
    res_rando = api_client.delete(url)
    assert res_rando.status_code == 403

    # Comment author can delete
    api_client.force_authenticate(user=db_setup['author2'])
    res_del = api_client.delete(url)
    assert res_del.status_code == 200
    assert not Comment.objects.filter(id=comment.id).exists()
