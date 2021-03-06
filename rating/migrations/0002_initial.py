# Generated by Django 3.2.13 on 2022-05-25 04:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rating', '0001_initial'),
        ('malls', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userrating',
            name='evaluated_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL, verbose_name='Оцениваемый пользователь'),
        ),
        migrations.AddField(
            model_name='userrating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_rating', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='mallrating',
            name='mall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='malls.mall', verbose_name='тц'),
        ),
        migrations.AddField(
            model_name='mallrating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mall_rating', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='arearating',
            name='area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='malls.area', verbose_name='площадь для аренды'),
        ),
        migrations.AddField(
            model_name='arearating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='area_rating', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddConstraint(
            model_name='userrating',
            constraint=models.UniqueConstraint(fields=('user', 'evaluated_user'), name='user_rating_unique'),
        ),
        migrations.AddConstraint(
            model_name='mallrating',
            constraint=models.UniqueConstraint(fields=('user', 'mall'), name='mall_rating_unique'),
        ),
        migrations.AddConstraint(
            model_name='arearating',
            constraint=models.UniqueConstraint(fields=('user', 'area'), name='area_rating_unique'),
        ),
    ]
