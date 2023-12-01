from django.test import TestCase
from core.models import User


class UserModelTest(TestCase):

    def setUp(self):    
        User.objects.create(username='u',
                            first_name='f',
                            last_name='l',
                            email='e@cd.com',
                            password='passworld12345')
        
    def test_user_exits(self):
        user = User.objects.get(pk=1)
        self.assertTrue(user)
        self.assertEqual(user.username, 'u')
        self.assertEqual(user.first_name, 'f')
        self.assertEqual(user.last_name, 'l')
        self.assertEqual(user.email, 'e@cd.com')
        self.assertEqual(user.password, 'passworld12345')

    def test_str_user(self):
        user = User.objects.get(pk=1)
        self.assertEqual(str(user), 'f l')