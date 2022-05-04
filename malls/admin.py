from django.contrib import admin
from malls import models


class GalleryAdmin(admin.TabularInline):
    model = models.Gallery
    can_delete = False
    extra = 1
    max_num = 100


@admin.register(models.Mall)
class MallAdmin(admin.ModelAdmin):
    inlines = (GalleryAdmin, )
    list_display = ('name', )
    list_display_links = ('name', )

    class Meta:
        model = models.Mall
