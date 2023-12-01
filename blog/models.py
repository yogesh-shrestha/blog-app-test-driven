from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from .customs import validate_file_size



class Category(models.Model):
    name = models.CharField(max_length=50,
                            null=True,
                            blank=False)
    slug = models.SlugField(max_length=255, 
                            editable=False)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)




class Post(models.Model):
    title = models.CharField(max_length=255,
                             unique=True,
                             null=True,
                             blank=False)
    slug = models.SlugField(max_length=255,
                            editable=False,
                            unique=True)
    category = models.ManyToManyField(Category,
                                default=[1],
                                related_name='posts')
    body = RichTextField()
    header_image = models.ImageField(upload_to="images/post",
                                     validators=[validate_file_size])
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, 
                               on_delete=models.PROTECT,
                               related_name='posts')
    status_published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-published_date']



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE, 
                                related_name='profile')
    bio = models.TextField(max_length=500,
                           null=True,
                           blank=True)
    profile_pic = models.ImageField(null=True, 
                                    blank=True, 
                                    upload_to='images/profile/',
                                    validators=[validate_file_size])
    fb_url = models.URLField(max_length=255,
                            null=True, 
                            blank=True,)
    twitter_url = models.URLField(max_length=255,
                                null=True, 
                                blank=True,)
    insta_url = models.URLField(max_length=255,
                                 null=True, 
                                blank=True,)
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def get_absolute_url(self):
        return reverse('blog:show_profile_page')


class Comment(models.Model):
    name = models.CharField(max_length=64,
                            null=False,
                            blank=False)
    email = models.EmailField(max_length=64,
                              null=False,
                            blank=False)
    comment = models.TextField(max_length=512,
                            null=False,
                            blank=False)
    published_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post,
                             models.CASCADE,
                             related_name='comments')
    

class Stats(models.Model):
    name = models.CharField(max_length=50)
    os_data = models.JSONField()

    def __str__(self):
        return self.name
