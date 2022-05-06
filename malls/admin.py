from django.contrib import admin
from malls import models


class GalleryAdmin(admin.TabularInline):
    model = models.Gallery
    extra = 1
    max_num = 100


class AreaAdmin(admin.TabularInline):
    model = models.Area
    extra = 1
    max_num = 100


@admin.register(models.Mall)
class MallAdmin(admin.ModelAdmin):
    inlines = (GalleryAdmin, AreaAdmin)
    list_display = ('name', )
    list_display_links = ('name', )

    class Meta:
        model = models.Mall
