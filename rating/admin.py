from django.contrib import admin

# Register your models here.
from rating import models


class MallRatingInline(admin.TabularInline):
    model = models.MallRating
    extra = 1
    max_num = 100


class UserRatingInline(admin.TabularInline):
    model = models.UserRating
    extra = 1
    max_num = 100
    fk_name = 'user'
