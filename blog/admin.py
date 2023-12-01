from django.contrib import messages
from django.urls import reverse
from django.utils.translation import ngettext
from django.contrib import admin
from django.utils.html import format_html, urlencode
from django.db.models import Count
from . import models
from .models import Post

admin.site.site_header = 'Blogger'
admin.site.index_title = 'Admin'


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'posts_count']
    search_fields = ['__str__']

    def posts_count(self, profile):
        url = (reverse('admin:blog_post_changelist')
                + '?'
                + urlencode({
                    'author__id': str(profile.user.id)
                })
                )
        counts = Post.objects.filter(author=profile.user.id).count()
        return format_html("<a href='{}'>{}</a>", url, counts)



@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'posts_count']
    search_fields = ['name']

    @admin.display(ordering='posts_count')
    def posts_count(self, category):
        url = (reverse('admin:blog_post_changelist')
               + '?'
               + urlencode({
                   'category__id': str(category.id)
               }))
        return format_html('<a href="{}">{}</a>', url, category.posts_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(posts_count=Count('posts'))



@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status_published']
    list_per_page = 20
    list_filter = ['category']
    autocomplete_fields = ['category']
    actions = ['make_published']

    @admin.action(description='publish selected posts')
    def make_published(self, request, queryset):
        updated = queryset.update(status_published=True)
        self.message_user(
            request,
            ngettext(
                f"{updated} Post was successfully marked as published.",
                f"{updated} Posts were successfully marked as published.",
                updated,
            ),
            messages.SUCCESS,
        )


@admin.register(models.Stats)
class StartsAdmin(admin.ModelAdmin):
    editable_fields = None

    def changelist_view(self, request, extra_context=None):
        os_data = models.Stats.objects.get(pk=1).os_data

        extra_context = extra_context or {"os_data": os_data}
        return super().changelist_view(request, extra_context=extra_context)