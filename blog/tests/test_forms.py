from django.test import TestCase
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from blog.forms import EditProfileForm, AddPostForm, CommentForm
from blog.models import Category,Post
from core.models import User



class TestProfileForm(TestCase):

    def setUp(self):
        self.image_valid = SimpleUploadedFile(name='django.jpg', 
                            content=open('./test_images/django.jpg', 'rb').read(),
                            content_type='image/jpg')
        self.image_invalid = SimpleUploadedFile(name='django.jpg', 
                            content=open('./test_images/river.jpg', 'rb').read(),
                            content_type='image/jpg')
        self.data = {'bio': 'b', 
                    'fb_url': 'http://a.com',
                    'twitter_url': 'http://t.com',
                    'insta_url': 'http://i.com'}

    def test_empty_profile_form(self):
        form = EditProfileForm()
        self.assertIn('bio', form.fields)
        self.assertIn('profile_pic', form.fields)
        self.assertIn('fb_url', form.fields)
        self.assertIn('twitter_url', form.fields)
        self.assertIn('insta_url', form.fields)

    def test_profile_form_valid_pic(self):
        form = EditProfileForm(self.data, {'profile_pic': self.image_valid})
        self.assertTrue(form.is_valid())

    def test_profile_form_invalid_pic(self):
        form = EditProfileForm(self.data, {'profile_pic': self.image_invalid})
        self.assertFalse(form.is_valid())



class TestAddPostForm(TestCase):

    def setUp(self):
        self.user = baker.make(settings.AUTH_USER_MODEL)
        self.category = baker.make(Category)
        self.header_image_valid = SimpleUploadedFile(name='django.jpg', 
                                        content=open('./test_images/django.jpg', 'rb').read(),
                                        content_type='image/png')
        self.header_image_invalid = SimpleUploadedFile(name='river.jpg', 
                                        content=open('./test_images/river.jpg', 'rb').read(),
                                        content_type='image/png')

    def test_empty_form(self):
        form = AddPostForm()
        self.assertIn('title', form.fields)
        self.assertIn('body', form.fields)
        self.assertIn('category', form.fields)
        self.assertIn('header_image', form.fields)

    def test_post_valid_all_form_data(self):
        form = AddPostForm({'title': 'a',
                            'body': 'b',
                            'tags': 'a, b',
                            'category': [self.category]},
                            {'header_image': self.header_image_valid})
        self.assertTrue(form.is_valid())

    def test_post_invalid_tag_form_data(self):
        form = AddPostForm({'title': 'a',
                            'body': 'b',
                            'tags': 'a b, c',
                            'category': [self.category]},
                            {'header_image': self.header_image_valid})
        self.assertFalse(form.is_valid())

    def test_post_invalid_image_form_data(self):
        form = AddPostForm({'title': 'a',
                            'body': 'b',
                            'tags': 'b, c',
                            'category': [self.category]},
                            {'header_image': self.header_image_invalid})
        self.assertFalse(form.is_valid())



class TestCommentForm(TestCase):
    
    def setUp(self):
        self.user = baker.make(User)
        self.category1 = Category.objects.create(name='c1')
        self.category2 = Category.objects.create(name='c2')
        self.header_image_valid = SimpleUploadedFile(name='django.jpg', 
                                        content=open('./test_images/django.jpg', 'rb').read(),
                                        content_type='image/jpg')
        self.post = Post.objects.create(title='a',
                                body='bbbbbb',
                                author = self.user,
                                header_image=self.header_image_valid,
                                status_published=True)
        self.data = {
            'name': 'n',
            'email': 'a@b.com',
            'comment': 'abc',
            'post': self.post
        }
    def test_valid_comment_form(self):
        form = CommentForm(self.data)
        self.assertTrue(form.is_valid())

    def test_invalid_comment_form(self):
        self.data['name'] = ''
        form = CommentForm(self.data)
        self.assertFalse(form.is_valid())

    def test_invalid_email_comment_form(self):
        self.data['email'] = 'aa.com'
        form = CommentForm(self.data)
        self.assertFalse(form.is_valid())


    

   