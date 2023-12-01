from django.test import Client, TestCase
from django.urls import reverse
from model_bakery import baker
from django.core.files.uploadedfile import SimpleUploadedFile

from blog.forms import EditProfileForm, AddPostForm, CommentForm
from .test_models import Category, Post
from core.models import User, Tag, TaggedItem


class TestProfileView(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = baker.make(User)
        self.user2 = baker.make(User)
        self.profile_data = {'bio': 'b', 
                            'fb_url': 'http://a.com',
                            'twitter_url': 'http://t.com',
                            'insta_url': 'http://i.com'}
        self.image_valid = SimpleUploadedFile(name='django.jpg', 
                            content=open('./test_images/django.jpg', 'rb').read(),
                            content_type='image/jpg')

    def test_show_profile_view_anonymous_GET(self):
        response = self.client.get(reverse('blog:show_profile_page'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:sign_in_page')+'?next=/profile/')

    def test_show_profile_view_logged_in_user_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('blog:show_profile_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog:show_profile.html')

    def test_edit_profile_view_anonymous_GET(self):
        response = self.client.get(reverse('blog:edit_profile_page', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:sign_in_page')+'?next=/edit-profile/1/')

    def test_edit_others_profile_logged_in_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('blog:edit_profile_page', args=[self.user2.id]))
        self.assertEqual(response.status_code, 403)

    def test_edit_profile_logged_in_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('blog:edit_profile_page', args=[self.user.id]))
        form = response.context.get('form')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, EditProfileForm)
        self.assertTemplateUsed('blog/edit_profile.html')

    def test_edit_profile_logged_in_POST(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('blog:edit_profile_page', args=[self.user.id]),
                                    data=self.profile_data, 
                                    FILES={'profile_pic': self.image_valid})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog:show_profile_page'))




class TestPostListView(TestCase):

    def setUp(self):
        self.user1 = baker.make(User)
        self.user2 = baker.make(User, is_staff=True)
        self.category1 = Category.objects.create(name='c1')
        self.category2 = Category.objects.create(name='c2')
        self.header_image_valid = SimpleUploadedFile(name='django.jpg', 
                                        content=open('./test_images/django.jpg', 'rb').read(),
                                        content_type='image/jpg')
        self.header_image_invalid = SimpleUploadedFile(name='river.jpg', 
                                        content=open('./test_images/river.jpg', 'rb').read(),
                                        content_type='image/png')
        self.post = Post.objects.create(title='a',
                        	    body='bbbbbb',
                                author = self.user1,
                                header_image=self.header_image_valid,
                                status_published=True)
        self.tag = Tag.objects.create(label='t')

    def test_index_page_anonymous_GET(self):
        response = self.client.get(reverse('blog:index_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/index.html')

    def test_index_page_logged_in_GET(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse('blog:index_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/index.html')

    def test_index_page_admin_in_GET(self):
        self.client.force_login(user=self.user2)
        response = self.client.get(reverse('blog:index_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/index.html')

    def test_category_posts_list_existing_category_GET(self):
        response = self.client.get(reverse('blog:category_post_page', args=[self.category1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/category_post.html')

    def test_category_posts_list_non_existing_category_GET(self):
        response = self.client.get(reverse('blog:category_post_page', args=[0]))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed('404.html')

    def test_tag_posts_list_existing_tag_GET(self):
        response = self.client.get(reverse('blog:tag_post_page', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/tag_post.html')

    def test_tag_posts_list_non_existing_tag_GET(self):
        response = self.client.get(reverse('blog:tag_post_page', args=[0]))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed('404.html')



class TestPostAddView(TestCase):

    def setUp(self):
        self.user1 = baker.make(User)
        self.user2 = baker.make(User, is_staff=True)
        self.category1 = Category.objects.create(name='c1')
        self.category2 = Category.objects.create(name='c2')
        self.header_image_valid = SimpleUploadedFile(name='django.jpg', 
                                        content=open('./test_images/django.jpg', 'rb').read(),
                                        content_type='image/jpg')
        self.header_image_invalid = SimpleUploadedFile(name='river.jpg', 
                                        content=open('./test_images/river.jpg', 'rb').read(),
                                        content_type='image/png')
        self.data = {
                'title': 'a',
                'body': 'bbbbbb',
                'category': [self.category1.id, self.category2.id],
                'tags': 'a, b',  
                'header_image': self.header_image_valid            
                } 

    def test_add_post_anonymous_GET(self):
        response = self.client.get(reverse('blog:add_post_page'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:sign_in_page')+'?next=/add-post/')

    def test_add_post_logged_in_GET(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse('blog:add_post_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('form'), AddPostForm)
        self.assertTemplateUsed('blog/add_post.html')

    def test_add_post_valid_logged_in_POST(self):
        self.client.force_login(user=self.user1)                 
        response = self.client.post(reverse('blog:add_post_page'), 
                                    data=self.data, 
                                    format='multipart'
                                    )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog:thanks_post_page'))

    def test_add_post_invalid_logged_in_POST(self):
        self.client.force_login(user=self.user1)
        self.data['header_image'] = self.header_image_invalid         
        response = self.client.post(reverse('blog:add_post_page'), 
                                    data=self.data, 
                                    format='multipart'
                                    )
        self.assertEqual(response.status_code, 200)
        self.assertRaises(ValueError)


class TestPostDetailView(TestCase):

    def setUp(self):
        self.user1 = baker.make(User)
        self.user2 = baker.make(User, is_staff=True)
        self.category1 = Category.objects.create(name='c1')
        self.category2 = Category.objects.create(name='c2')
        self.header_image_valid = SimpleUploadedFile(name='django.jpg', 
                                        content=open('./test_images/django.jpg', 'rb').read(),
                                        content_type='image/jpg')
        self.post = Post.objects.create(title='a',
                        	    body='bbbbbb',
                                author = self.user1,
                                header_image=self.header_image_valid,
                                status_published=True)
        self.post.category.add(self.category1)

    def test_post_detail_page_status_published(self):
               
        response = self.client.get(reverse('blog:post_detail_page', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/post_detail.html')

    def test_post_empty_comment_form(self):
        response = self.client.get(reverse('blog:post_detail_page', args=[self.post.id]))
        self.assertIsInstance(response.context.get('form'), CommentForm)

    def test_post_comment_POST(self):
        data = {'name': 'n',
                'email': 'a@b.com',
                'comment': 'abc',
                'post': self.post}
        response = self.client.post(reverse('blog:post_detail_page', args=[self.post.id]),
                                    data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog:post_detail_page', args=[self.post.id]))



class TestPostUpdateView(TestCase):

    def setUp(self):
        self.user1 = baker.make(User)
        self.user2 = baker.make(User, is_staff=True)
        self.user3 = baker.make(User)
        self.category1 = Category.objects.create(name='c1')
        self.category2 = Category.objects.create(name='c2')
        self.header_image_valid = SimpleUploadedFile(name='django.jpg', 
                                        content=open('./test_images/django.jpg', 'rb').read(),
                                        content_type='image/jpg')
        self.header_image_invalid = SimpleUploadedFile(name='river.jpg', 
                                        content=open('./test_images/river.jpg', 'rb').read(),
                                        content_type='image/png')
        self.post = Post.objects.create(title='a',
                            body='bbbbbb',
                            author = self.user1,
                            header_image=self.header_image_valid,
                            status_published=True)
        self.post.category.add(self.category1)
        
    def test_post_update_anonymous_GET(self):
        response = self.client.get(reverse('blog:post_update_page', args=[self.post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:sign_in_page')
                             +f'?next=/update-post/{self.post.id}')
        
    def test_post_update_logged_in_own_post_GET(self):
        self.client.force_login(user=self.user1)
        response = self.client.get(reverse('blog:post_update_page', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)

    def test_post_update_logged_in_not_own_post_GET(self):
        self.client.force_login(user=self.user3)
        response = self.client.get(reverse('blog:post_update_page', args=[self.post.id]))
        self.assertEqual(response.status_code, 403)

    def test_post_update_admin_GET(self):
        self.client.force_login(user=self.user2)
        response = self.client.get(reverse('blog:post_update_page', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('form'), AddPostForm)

    def test_post_update_admin_POST(self):
        self.client.force_login(user=self.user2) 
        self.data = {
                'title': 'a',
                'body': 'bbbbbb',
                'category': [self.category1.id, self.category2.id],
                'tags': 'a, b',               
                }                 
        response = self.client.post(reverse('blog:post_update_page', args=[self.post.id]), 
                                    data=self.data, 
                                    FILES={'header_image': self.header_image_valid}
                                    )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog:post_detail_page', args=[self.post.id]))


    

