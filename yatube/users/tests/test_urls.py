# from django.contrib.auth import get_user_model
# from django.test import TestCase, Client
# from http import HTTPStatus

# from django.urls import reverse

# from posts.models import Post, Group

# User = get_user_model()

# def test_urls_uses_correct_template(self):
#     """URL - адрес использует соответствующий шаблон."""
#     for url, template in (
#         UserURLTests.unauth_urls
#         | UserURLTests.auth_urls
#     ).items():
#         with self.subTest(url=url):
#             response = self.authorized_client.get(url)
#             self.assertTemplateUsed(response, template)


# cls.unauth_urls = {
#             '/auth/login/': 'users/login.html',
#             '/auth/logout/': 'users/logged_out.html',
#             '/auth/signup/': 'users/signup.html',
#             '/auth/password_reset/': 'users/password_reset_form.html',
#             '/auth/password_reset/done/': 'users/password_reset_done.html',
#             '/auth/reset/done/': 'users/password_reset_complete.html',
#         }
# cls.auth_urls = {
#             '/auth/password_change/': 'users/password_change_form.html',
#             '/auth/password_change/done/': 'users/password_change_done.html',
#         }