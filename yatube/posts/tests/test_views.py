from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostsViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testUser')
        cls.group = Group.objects.create(
            title='test group',
            slug='slug',
            description='test description',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='test text',
            group=cls.group
        )
        cls.templates_pages_names = {
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
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_use_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        for reverse_name, template in self.templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author.username
        post_text_0 = first_object.text
        post_group_0 = first_object.group.title
        self.assertEqual(post_author_0, self.user.username)
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_group_0, self.group.title)

    def test_group_list_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author.username
        post_text_0 = first_object.text
        post_group_0 = first_object.group.title
        post_group_slug_0 = first_object.group.slug
        post_group_description_0 = first_object.group.description
        self.assertEqual(post_author_0, self.user.username)
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_group_0, self.group.title)
        self.assertEqual(post_group_slug_0, self.group.slug)
        self.assertEqual(post_group_description_0, self.group.description)

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user})
        )
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author.username
        post_text_0 = first_object.text
        post_group_0 = first_object.group.title
        self.assertEqual(post_author_0, self.user.username)
        self.assertEqual(post_text_0, self.post.text)
        self.assertEqual(post_group_0, self.group.title)

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={
                'post_id': PostsViewsTests.post.id})
        )
        self.assertEqual(
            response.context.get('post').author, PostsViewsTests.user)
        self.assertEqual(response.context.get('post').text, self.post.text)
        self.assertEqual(
            response.context.get('post').group, PostsViewsTests.group)

    def test_post_create_or_edit_show_correct_context(self):
        """Шаблон post_create/post_edit сформирован с правильным контекстом."""

        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        response_0 = self.authorized_client.get(
            reverse('posts:post_create')
        )
        response_1 = self.authorized_client.get(
            reverse(
                'posts:post_edit', kwargs={'post_id': PostsViewsTests.post.id})
        )
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field_0 = response_0.context.get('form').fields.get(value)
                form_field_1 = response_1.context.get('form').fields.get(value)
                self.assertIsInstance(form_field_0, expected)
                self.assertIsInstance(form_field_1, expected)
