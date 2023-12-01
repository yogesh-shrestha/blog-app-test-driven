from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from model_bakery import baker

from core.models import User
from core.forms import UserPasswordResetForm



class TestSignUpView(TestCase):

    def setUp(self):
        self.data = {'username': 'testuser',
                    'first_name':'testfirst',
                    'last_name': 'testlast',
                    'email': 'test@test.com',
                    'password1': 'testpassword12345$$$',
                    'password2': 'testpassword12345$$$'}

    def test_sign_up_page_exists(self):
        response = self.client.get(reverse('core:sign_up_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('core/register.html')

    def test_is_sign_up_form(self):
        response = self.client.get(reverse('core:sign_up_page'))
        form = response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)

    def test_sign_up_valid_data_POST(self):
        response = self.client.post(reverse('core:sign_up_page'), self.data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:sign_in_page'))


class TestSignInView(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.email = 'test@test.com'
        self.password = 'testpassword12345$$$'
        self.user = User.objects.create_user(
            username = self.username,
            email=self.email,
            password=self.password
        )
        
    def test_sign_in_page_exits(self):
        response = self.client.get(reverse('core:sign_in_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('core/login.html')

    def test_is_sign_in_form(self):
        response = self.client.get(reverse('core:sign_in_page'))
        form = response.context.get('form')
        self.assertIsInstance(form, AuthenticationForm)

    def test_user_signed_in(self):
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(reverse('core:sign_in_page'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog:index_page'))



class TestLogout(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.email = 'test@test.com'
        self.password = 'testpassword12345$$$'
        self.user = User.objects.create_user(
            username = self.username,
            email=self.email,
            password=self.password
        )

    def test_logout_view(self):
        self.client.login(username=self.username, password=self.password)
        self.assertTrue('_auth_user_id' in self.client.session)
        self.client.get(reverse('core:logout_page'))
        self.assertFalse('_auth_user_id' in self.client.session)



class TestPasswordResetView(TestCase):

    def test_password_reset_GET(self):
        response = self.client.get(reverse('core:password_reset_page'))
        form = response.context.get('form')
        self.assertTrue(response.status_code, 200)
        self.assertTemplateUsed('core/password_reset.html')
        self.assertIsInstance(form, UserPasswordResetForm)
        

    def test_password_reset_POST(self):
        response = self.client.post(reverse('core:password_reset_page'))
        self.assertTrue(response.status_code, 302)

    
