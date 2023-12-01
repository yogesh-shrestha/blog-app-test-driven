from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from django.test import TestCase
from model_bakery import baker
from core.forms import (SignUpForm, 
                        SignInForm, 
                        UserPasswordChangeForm,
                        UserPasswordResetForm,
                        UserPasswordConfirmForm)
from core.models import User


class TestSignUpForm(TestCase):

    @classmethod
    def setUp(self):
        self.data = {'username': 'testuser',
                    'first_name':'testfirst',
                    'last_name': 'testlast',
                    'email': 'test@test.com',
                    'password1': 'testpassword12345$$$',
                    'password2': 'testpassword12345$$$'}
        
    def test_subclassof(self):
        self.assertTrue(issubclass(SignUpForm, UserCreationForm))

    def test_empty_form(self):
        form = SignUpForm()
        self.assertIn('username', form.fields)
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('password1', form.fields)
        self.assertIn('password2', form.fields)

    def test_valid_form(self):
        form = SignUpForm(self.data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        self.data['email'] = 'invalidemail'
        form = SignUpForm(self.data)
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValueError):
            form.save()

    def test_password_missmatch(self):
        self.data['password2'] = 'sdjkfj12456'
        form = SignUpForm(self.data)
        with self.assertRaises(ValueError):
            form.save()

    def test_existing_username(self):
        user = baker.make(User)
        self.data['username'] = user.username
        form = SignUpForm(self.data)
        with self.assertRaises(ValueError):
            form.save()



class TestSignInForm(TestCase):

    def test_empty_sign_in_form(self):
        form = SignInForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)


class TestChangePasswordForm(TestCase):
    
    def setUp(self):
        self.username = 'testuser'
        self.email = 'test@test.com'
        self.password = 'testpassword12345$$$'
        self.user = User.objects.create_user(
            username = self.username,
            email=self.email,
            password=self.password
        )
        self.old_password = 'pass1234$$',
        self.new_password1 = '1234$$pass',
        self.new_password2 = '1234$$pass',

    def test_empty_change_pw_form(self):
        user = User.objects.get(pk=1)
        form = UserPasswordChangeForm(user)
        self.assertIn('old_password', form.fields)
        self.assertIn('new_password1', form.fields)
        self.assertIn('new_password2', form.fields)

    def test_valid_data_cpw_form(self):
        user = User.objects.get(pk=1)
        form = UserPasswordChangeForm(user, 
                                    {
                                    'old_password': self.password,
                                    'new_password1': self.new_password1,
                                    'new_password2': self.new_password2
                                    })
        self.assertTrue(form.is_valid())


class TestPasswordResetForms(TestCase):
    
    def setUp(self):
        self.username = 'testuser'
        self.email = 'test@test.com'
        self.password = 'testpassword12345$$$'
        User.objects.create_user(
            username = self.username,
            email=self.email,
            password=self.password
        )
    
    def test_user_password_reset_form_valid(self):
        form = UserPasswordResetForm({'email': 'a@b.com'})
        self.assertTrue(form.is_valid())

    def test_user_password_reset_form_invalid(self):
        form = UserPasswordResetForm({'email': 'a'})
        self.assertFalse(form.is_valid())

    def test_user_password_reset_confirm_valid(self):
        user = User.objects.get(pk=1)
        form = UserPasswordConfirmForm(user, {'new_password1': 'abcde12345$$',
                                        'new_password2': 'abcde12345$$'})
        self.assertTrue(form.is_valid())

    def test_user_password_reset_confirm_valid(self):
        user = User.objects.get(pk=1)
        form = UserPasswordConfirmForm(user, {'new_password1': 'abcde12345$$',
                                        'new_password2': 'abcde12345'})
        self.assertFalse(form.is_valid())


    




            



    