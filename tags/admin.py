from django.contrib import admin

from .models import Tag, TaggedItem

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['label']
    search_fields = ['label']

@admin.register(TaggedItem)
class TaggedItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_type', 'object_id']

