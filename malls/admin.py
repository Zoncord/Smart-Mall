from django.contrib import admin
from malls import models
from rating.admin import MallRatingInline


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
    inlines = [GalleryAdmin, AreaAdmin, MallRatingInline]
    list_display = ['name', ]
    list_display_links = ['name', ]

    class Meta:
        model = models.Mall


# Площадь

class RentInline(admin.TabularInline):
    model = models.Rent
    extra = 1
    max_num = 100


@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    inlines = [RentInline]
    list_display = ['mall', 'available']
    exclude = ('decore_string',)

    class Meta:
        model = models.Area


# Аренда
@admin.register(models.Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ['area', 'tenant']

    class Meta:
        model = models.Rent
