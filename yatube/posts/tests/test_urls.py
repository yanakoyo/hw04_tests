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
        cls.public_urls = (
            ('/', 'index.html'),
            (f'/group/{cls.group.slug}/', 'group.html'),
            (f'/profile/{cls.user.username}/', 'profile.html'),
            (f'/posts/{cls.post.pk}/', 'post_detail.html')
        )
        cls.private_urls = (
            ('/create/', 'post_create.html'),
            (f'/posts/{cls.post.pk}/edit/', 'post_create.html')
        )
        cls.templates_page_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': cls.group.slug}): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': cls.user.username}): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': cls.post.pk}): 'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/post_create.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': cls.post.pk}): 'posts/post_create.html',
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_availability(self):
        """Страница не доступна пользователю"""
        for address in self.public_urls:
            response = self.guest_client.get(address[0])
            with self.subTest(response=response):
                self.assertEqual(response.status_code, HTTPStatus.OK)

        for address in self.private_urls:
            response = self.authorized_client.get(address[0])
            with self.subTest(response=response):
                self.assertEqual(response.status_code, HTTPStatus.OK)

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

    def test_pages_use_correct_templates(self):
        """Проверка использования правильных шаблонов."""
        for reverse_address, template in self.templates_page_names.items():
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
