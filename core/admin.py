from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline

from blog.models import Post
from .models import User
from blog.admin import PostAdmin
from tags.models import TaggedItem


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", 'first_name', "last_name"),
            },
        ),
    )


class TagInline(GenericTabularInline):
    model = TaggedItem
    extra = 0
    autocomplete_fields = ['tag']


class CustomPostAdmin(PostAdmin):
    inlines = [TagInline]


admin.site.unregister(Post)
admin.site.register(Post, CustomPostAdmin)