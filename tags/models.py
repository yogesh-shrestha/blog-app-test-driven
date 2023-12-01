from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



# Custom Manager
class TaggedItemManager(models.Manager):
    def get_tags_for(self, object_type, object_id):
        """ Return tagged items for a generic contenttype """
        content_type = ContentType.objects.get_for_model(object_type)
        queryset = TaggedItem.objects \
                            .select_related('tag') \
                            .filter(
                                content_type=content_type,
                                object_id=object_id
                            )
        return queryset

    def save_tags_for(self, object_type, object_id, tag_labels):
        """ Saves tagged Item for a generic contenttype"""
        content_type = ContentType.objects.get_for_model(object_type)
        for tag_label in tag_labels:
            if not Tag.objects.filter(label=tag_label).exists():
                tag = Tag(label=tag_label)
                tag.save()
            else:
                tag = Tag.objects.get(label=tag_label)

            if not TaggedItem.objects.filter(object_id=object_id, tag_id=tag.id).exists():
                tagged_item = TaggedItem(tag=tag,
                                        content_type=content_type,
                                        object_id=object_id)
                tagged_item.save()

    def get_objects_for(self, object_type, tag_id):
        content_type = ContentType.objects.get_for_model(object_type)
        queryset = TaggedItem.objects \
                        .filter(
                            content_type=content_type,
                            tag_id = tag_id
                        ).values('object_id')
        return queryset




class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label



class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, 
                            on_delete=models.CASCADE) 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()




