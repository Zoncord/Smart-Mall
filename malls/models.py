from django.db import models
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from PIL import Image
from django.contrib.auth import get_user_model


class Mall(models.Model):
    name = models.CharField('Название', max_length=50, help_text='Название ТЦ, максимум 50 символов')
    owner = models.ForeignKey(get_user_model(), verbose_name='Владелец', on_delete=models.CASCADE, related_name='malls', help_text='Владелец ТЦ')
    description = models.TextField('Описание', help_text='Описание ТЦ')
    address = models.CharField('Адрес', max_length=150, help_text='Адрес ТЦ, максимум 150 символов')
    # Заглушка для рейтинга
    # rating = None

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

    mall = models.ForeignKey(Mall, on_delete=models.DO_NOTHING, related_name='areas', verbose_name='Торговый центр')
    price = models.PositiveIntegerField('Цена')
    available = models.BooleanField('Доступность', choices=AVAILABLE_CHOICES, default=True)
    square = models.PositiveIntegerField('Площадь в кв. метрах')

    class Meta:
        verbose_name = 'Площадь'
        verbose_name_plural = 'Площади'

    def __str__(self):
        return f'{self.mall} - площадь №{self.pk}'
