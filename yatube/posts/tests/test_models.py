from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг' * 10,
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""

        post = PostModelTest.post
        field_verboses_post = {
            'text': 'Текст поста:',
            'pub_date': 'Дата публикации',
            'group': 'Выберите группу:',
        }

        for value, expected in field_verboses_post.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected)

        expected_object_name_post = post.text
        self.assertEqual(expected_object_name_post, str(post))

        group = PostModelTest.group
        field_verboses_group = {
            'title': 'group name',
            'slug': 'group url',
            'description': 'Описание',
        }

        for value, expected in field_verboses_group.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected)

        expected_object_name_group = group.title
        self.assertEqual(expected_object_name_group, str(group))
