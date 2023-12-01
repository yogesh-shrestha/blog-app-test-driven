from django.db import models
from django.contrib.auth.models import AbstractUser
from tags.models import Tag, TaggedItem


class User(AbstractUser):
    username = models.CharField(max_length=50,
                                unique=True)
    email = models.EmailField(unique=True, 
                              null=False, 
                              blank=False)
    first_name = models.CharField(max_length=50,  
                                  null=False, 
                                  blank=False)
    last_name = models.CharField(max_length=50,  
                                 null=False, 
                                 blank=False)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
