import tempfile
from django.conf import settings
from django.shortcuts import redirect, reverse
from django.test import TestCase
from blog.models import Profile, Category, Post
from model_bakery import baker
from core.models import User


class TestProfile(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        User.objects.create(first_name='a', 
                            last_name='b', 
                            email='c@c.com', 
                            username='ac', 
                            password='p')
        
    def test_profile_created_post_save_signal(self):
        profile = Profile.objects.get(pk=1)
        self.assertIsInstance(profile, Profile)

    def test_post_str(self):
        profile =  Profile.objects.get(pk=1)
        full_name = profile.user.first_name + ' ' + profile.user.last_name
        self.assertEqual(str(profile), full_name)
        self.assertEqual(profile.user.first_name, 'a')
        self.assertEqual(profile.user.last_name, 'b')

    def test_profile_get_absolute_url(self):
        profile = Profile.objects.get(pk=1)
        response = redirect(profile)
        self.assertEqual(response.url, '/profile/')



class TestCategory(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='a')

    def test_category_str(self):
        category = Category.objects.get(pk='1')
        self.assertEqual(str(category), 'a')

    def test_category_save(self):
        category = Category.objects.get(pk='1')
        self.assertEqual(category.slug, 'a')



class TestPost(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = baker.make(Category)
        author = baker.make(settings.AUTH_USER_MODEL)
        post = Post.objects.create(title='a b',
                            header_image = tempfile.NamedTemporaryFile(suffix=".jpg").name,
                            body='b',
                            author=author)
        post.category.add(category.id)

    def test_post_str(self):
        post =  Post.objects.get(pk=1)
        self.assertEqual(str(post), 'a b')

    def test_post_slug(self):
        post = Post.objects.get(pk=1)
        self.assertEqual(post.slug, 'a-b')

    







        