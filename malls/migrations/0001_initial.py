# Generated by Django 3.2.13 on 2022-05-18 08:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('available', models.BooleanField(choices=[(True, 'Свободно'), (False, 'Занято')], default=True, verbose_name='Доступность')),
                ('square', models.PositiveIntegerField(verbose_name='Площадь в кв. метрах')),
                ('decore_string', models.CharField(blank=True, max_length=100, verbose_name='костыль для оптимизации')),
            ],
            options={
                'verbose_name': 'Площадь',
                'verbose_name_plural': 'Площади',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='uploads/', verbose_name='Изображения ТЦ')),
            ],
            options={
                'verbose_name': 'Изображение',
                'verbose_name_plural': 'Галерея',
            },
        ),
        migrations.CreateModel(
            name='Mall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название ТЦ, максимум 50 символов', max_length=50, verbose_name='Название')),
                ('description', models.TextField(help_text='Описание ТЦ', verbose_name='Описание')),
                ('address', models.CharField(help_text='Адрес ТЦ, максимум 150 символов', max_length=150, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Торговый центр',
                'verbose_name_plural': 'Торговые центры',
            },
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rental_start_date_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время начала аренды')),
                ('balance', models.BigIntegerField(verbose_name='Баланс')),
                ('status', models.BooleanField(choices=[(True, 'Активна'), (False, 'Закончилась')], default=True, verbose_name='Статус аренды')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='rents', to='malls.area', verbose_name='Площадь')),
            ],
            options={
                'verbose_name': 'Аренда',
                'verbose_name_plural': 'Аренды',
            },
        ),
    ]
