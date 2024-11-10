import pytest
from django.contrib.auth.models import User
from django.urls import reverse

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.mark.django_db
def test_user_registration(client):
    response = client.post(reverse('user_create'), {
        'username': 'newuser',
        'password': 'newpassword',
        'password_confirm': 'newpassword'
    })
    
    assert response.status_code == 302
    assert User.objects.filter(username='newuser').exists()

@pytest.mark.django_db
def test_user_update(user, client):
    client.login(username='testuser', password='testpassword')

    response = client.post(reverse('user_update', args=[user.id]), {
        'username': 'updateduser',
        'password': 'newpassword',
    })
    
    assert response.status_code == 302
    user.refresh_from_db()
    assert user.username == 'updateduser'

@pytest.mark.django_db
def test_user_deletion(user, client):
    client.login(username='testuser', password='testpassword')

    response = client.post(reverse('user_delete', args=[user.id]))
    
    assert response.status_code == 302
    assert not User.objects.filter(id=user.id).exists()