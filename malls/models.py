from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from PIL import Image
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


class Mall(models.Model):
    name = models.CharField('Название', max_length=50, help_text='Название ТЦ, максимум 50 символов')
    owner = models.ForeignKey(get_user_model(), verbose_name='Владелец', on_delete=models.CASCADE, related_name='malls',
                              help_text='Владелец ТЦ')
    description = models.TextField('Описание', help_text='Описание ТЦ')
    address = models.CharField('Адрес', max_length=150, help_text='Адрес ТЦ, максимум 150 символов')

    class Meta:
        verbose_name = 'Торговый центр'
        verbose_name_plural = 'Торговые центры'

    def __str__(self):
        return self.name


class Gallery(models.Model):
    mall = models.ForeignKey(Mall, on_delete=models.CASCADE, related_name='gallery', verbose_name='Торговый центр')
    image = models.ImageField('Изображения ТЦ', upload_to='uploads/', blank=True)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Галерея'

    def get_image(self):
        return get_thumbnail(self.image, '400x400', upscale=False)

    def __str__(self):
        return mark_safe(f"<img src='{self.image.url}' width='200' height='200'>")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            image = Image.open(self.image.path)
            if image.height > 400 or image.width > 400:
                image.thumbnail((400, 400), Image.ANTIALIAS)
                image.save(self.image.path)


class Area(models.Model):
    AVAILABLE_CHOICES = [
        (True, 'Свободно'),
        (False, 'Занято')
    ]

    mall = models.ForeignKey(Mall, on_delete=models.CASCADE, related_name='areas', verbose_name='Торговый центр')
    price = models.PositiveIntegerField('Цена')
    available = models.BooleanField('Доступность', choices=AVAILABLE_CHOICES, default=True)
    square = models.PositiveIntegerField('Площадь в кв. метрах')
    decore_string = models.CharField('костыль для оптимизации', max_length=100, blank=True)# это действительно сильно прогу оптимизириует нетрогайте пж=)

    class Meta:
        verbose_name = 'Площадь'
        verbose_name_plural = 'Площади'

    def save(self, *args, **kwargs):
        self.decore_string = f'{self.mall}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.decore_string} - площадь №{self.id}'


class Rent(models.Model):
    STATUS_CHOICES = [
        (True, 'Активна'),
        (False, 'Закончилась')
    ]

    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='rents', verbose_name='Площадь')
    tenant = models.ForeignKey(get_user_model(), verbose_name='Арендатор', on_delete=models.CASCADE,
                               related_name='rents', help_text='Арендатор площади')
    rental_start_date_time = models.DateTimeField(verbose_name='Дата и время начала аренды', default=timezone.now)
    balance = models.BigIntegerField(verbose_name='Баланс')
    status = models.BooleanField('Статус аренды', choices=STATUS_CHOICES, default=True)

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'

    def __str__(self):
        return f'{self.tenant} арендует - площадь №{self.area.pk}'
