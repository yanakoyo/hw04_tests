from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostsURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auchh')
        cls.group = Group.objects.create(
            title='test group',
            slug='slug',
            description='test description',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='test text',
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Тестирование доступности страниц неавто пользователю - привести к циклу
    def test_pages_availability(self):
        """Страница не доступна пользователю"""
        post_id = self.post.id
        username = self.user.username
        pages_list_guest = [
            '/',
            f'/posts/{post_id}/',
            '/group/slug/',
            f'/profile/{username}/'
        ]
        pages_list_auth = [
            '/create/',
            f'/posts/{post_id}/edit/',
        ]

        for address in pages_list_guest:
            response = self.guest_client.get(address)
            with self.subTest(response=response):
                self.assertEqual(response.status_code, 200)

        for address in pages_list_auth:
            response = self.authorized_client.get(address)
            with self.subTest(response=response):
                self.assertEqual(response.status_code, 200)

    # Проверяем редиректы для неавторизованного пользователя
    def test_create_url_redirect_anonymous(self):
        """Страница /create/ перенаправляет анонимного пользователя."""
        response = self.guest_client.get('/create/', follow=True)
        self.assertRedirects(
            response, '/auth/login/?next=/create/'
        )

    def test_edit_url_redirect_anonymous(self):
        """Страница /post_id/edit/ перенаправляет анонимного
        пользователя.
        """
        response = self.guest_client.get(
            f'/posts/{self.post.id}/edit/',
            follow=True)
        self.assertRedirects(
            response, f'/auth/login/?next=/posts/{self.post.id}/edit/'
        )

    # Проверка шаблонов
    def test_pages_use_correct_templates(self):
        user_name = self.user.username
        post_id = self.post.id
        slug = self.group.slug
        templates_page_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': slug}): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': user_name}): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': post_id}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/post_create.html',
            reverse(
                'posts:post_edit', 
                kwargs={'post_id': post_id}): 'posts/post_create.html',
        }

        for reverse_address, template in templates_page_names.items():
            response = self.authorized_client.get(reverse_address)
            error_message = (f'Для адресной строки {reverse_address} ;'
                           f'ожидается шаблон: {template}')

            with self.subTest(template=template, response=response):
                self.assertTemplateUsed(response, template, error_message)

    def test_404_url(self):
        response_url = {
            self.guest_client: '/unexisting_page/',
            self.authorized_client: '/unexisting_page/',
        }
        for client, url in response_url.items():
            with self.subTest(client=client):
                response = client.get(url)
                self.assertEqual(
                    response.status_code, HTTPStatus.NOT_FOUND
                )
