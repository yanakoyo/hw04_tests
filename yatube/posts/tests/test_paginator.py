from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from posts.models import Group, Post
from posts.views import POSTS_PER_PAGE

User = get_user_model()

TEST_POSTS_PER_PAGE = 3


class PaginatorViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testUser')
        cls.group = Group.objects.create(
            title='test group',
            slug='slug',
            description='test description',
        )
        post_list = []
        for i in range(0, (POSTS_PER_PAGE + TEST_POSTS_PER_PAGE)):
            post_list.append(
                Post.objects.create(
                    author=cls.user,
                    text=f'test text {i}',
                    group=cls.group
                )
            )

    def test_paginator(self):
        user_name = self.user.username
        slug = self.group.slug
        number_of_posts_per_page = {
            reverse('posts:index'): POSTS_PER_PAGE,
            reverse('posts:index') + '?page=2': TEST_POSTS_PER_PAGE,
            reverse(
                'posts:group_list',
                kwargs={'slug': slug}): POSTS_PER_PAGE,
            reverse(
                'posts:group_list',
                kwargs={'slug': slug}) + '?page=2': TEST_POSTS_PER_PAGE,
            reverse(
                'posts:profile',
                kwargs={'username': user_name}): POSTS_PER_PAGE,
            reverse(
                'posts:profile',
                kwargs={'username': user_name}) +
                '?page=2': TEST_POSTS_PER_PAGE,
        }

        for rev_name, post_count in number_of_posts_per_page.items():
            with self.subTest(reverse_name=rev_name):
                response = self.client.get(rev_name)
                self.assertEqual(len(response.context['page_obj']), post_count)
