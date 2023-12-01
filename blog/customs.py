import re
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.decorators import user_passes_test


def validate_file_size(file):
    max_file_size_mb = 2 
    if file.size > max_file_size_mb * 1024 * 1024:
        raise ValidationError(f'file size can not be larger than {max_file_size_mb} MB !')
    

class MultiTagField(forms.Field):
    def to_python(self, value):
        if not value:
            return []
        tags = value.split(',')
        tags = [tag.strip() for tag in tags if tag !='']
        return tags
    
    def validate(self, tags):
        super().validate(tags)
        for tag in tags:
            tag = tag.strip()
            if re.findall(' +', tag):
                raise ValidationError("Tags can not have space !")
            


def staff_required(login_url=None):
    return user_passes_test(lambda user: user.is_staff, login_url=login_url)


    