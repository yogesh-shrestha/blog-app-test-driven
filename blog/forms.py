from django import forms
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget

from .models import Profile, Post, Comment
from .customs import MultiTagField


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic', 'fb_url', 'twitter_url', 'insta_url']

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'fb_url': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-control'}),
            'insta_url': forms.URLInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'profile_pic': 'Profile Picture',
            'fb_url': 'Facebook URL',
            'twitter_url': 'Twitter URL',
            'insta_url': 'Instagram URL'
        }



class AddPostForm(forms.ModelForm):
    tags = MultiTagField(
                required=False,
                widget=forms.TextInput(
                    attrs={'class': 'form-control', 
                        'placeholder': 'separate tags by a comma',
                        'maxlength': 100})) 
    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'header_image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body' : CKEditorWidget(attrs={'class': 'form-control'}),
            'tags' : forms.TextInput(attrs={'class': 'form-control', 
                                   'placeholder': 'separate tags by a comma',
                                   'maxlength': 100}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'header_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'category': _('you can select more than one category'),
            'header_image': _('image size must be less than 2 MB.'),
        }
        labels = {
            'body': _('Content')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].help_text = _('separate tags with comma. Only tags with a single word are accepted.')



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))





