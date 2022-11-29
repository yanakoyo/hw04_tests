from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostCreateFormTests(TestCase):
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
        # cls.form = PostForm()

    def setUp(self):
        """Создаем нового клиента для каждого теста."""
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def tearDown(self):
        """Удаляем клиента после теста."""
        del self.authorized_client

    def test_create_post_works(self):
        posts_count = Post.objects.all().count()
        form_data = {
            'text':'test text',
            'group': self.group.pk
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:profile',
                kwargs={'username': self.user.username}))
        self.assertEqual(Post.objects.all().count(), posts_count+1)
        self.assertTrue(
            Post.objects.filter(
                text='test text',
                group= self.group
            ).exists()
        )

    def test_edit_post_works(self):
        posts_count = Post.objects.all().count()
        form_data = {
            'text':'test text modified',
            'group': self.group.pk
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.all().count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                text='test text modified',
                group=self.group.pk
            ).exists()
        )
        self.assertRedirects(response, reverse('posts:post_detail',
                kwargs={'post_id': self.post.pk}))
  