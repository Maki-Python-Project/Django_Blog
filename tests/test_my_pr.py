import pytest
from articles.models import Article
from users.models import CustomUser
from django.urls import reverse


@pytest.fixture()
def create_user(django_user_model):
    user = django_user_model.objects.create(
        username='someone', password='password'
    )
    return user


@pytest.fixture
def test_password():
    return 'super-mega-hardcore-password'


@pytest.mark.django_db
def test_check_title():
    article = Article(title='test', body='body', author=CustomUser())
    assert article.title == 'test'


@pytest.mark.django_db
def test_signup_page_status_code(client):
    url = reverse('signup')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_article(create_user):
    Article.objects.create(
        title='john', body='gg', author=CustomUser(create_user.id)
    )
    assert Article.objects.all().count() == 1


@pytest.mark.django_db
def test_detail_page_status_code(client, create_user):
    url = reverse('article_detail', kwargs={'pk': create_user.pk})
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_auth_view(client, create_user, test_password):
    user = create_user
    url = reverse('login')
    client.login(
        username=user.username, password=test_password
    )
    response = client.get(url)
    assert response.status_code == 200
