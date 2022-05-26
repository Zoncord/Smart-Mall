from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint


class BaseRating(models.Model):
    class Feeling(models.IntegerChoices):
        Hatred = 1, 'Ненависть'
        Dislike = 2, 'Неприязнь'
        Neutral = 3, 'Нейтрально'
        Adoration = 4, 'Обожание'
        Love = 5, 'Любовь'

    star = models.PositiveSmallIntegerField(verbose_name='кол-во звезд', choices=Feeling.choices, null=True, blank=True)

    class Meta:
        abstract = True


class MallRating(BaseRating):
    user = models.ForeignKey(to=get_user_model(), verbose_name='пользователь', on_delete=models.CASCADE,
                             related_name='mall_rating')
    mall = models.ForeignKey(to='malls.Mall', verbose_name='тц', on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return str(self.user) + ' ' + str(self.mall) + ' ' + str(self.star)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'mall'], name='mall_rating_unique')
        ]
        verbose_name = 'оценка тц'
        verbose_name_plural = 'оценки тц'


class AreaRating(BaseRating):
    user = models.ForeignKey(to=get_user_model(), verbose_name='пользователь', on_delete=models.CASCADE,
                             related_name='area_rating')
    area = models.ForeignKey(to='malls.Area', verbose_name='площадь для аренды', on_delete=models.CASCADE,
                             related_name='ratings')

    def __str__(self):
        return str(self.user) + ' ' + str(self.area) + ' ' + str(self.star)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'area'], name='area_rating_unique')
        ]
        verbose_name = 'оценка площади'
        verbose_name_plural = 'оценки площадей'


class UserRating(BaseRating):
    user = models.ForeignKey(to=get_user_model(), verbose_name='пользователь', on_delete=models.CASCADE,
                             related_name='user_rating')
    evaluated_user = models.ForeignKey(to=get_user_model(), verbose_name='Оцениваемый пользователь',
                                       on_delete=models.CASCADE, related_name='ratings')

    def __str__(self):
        return str(self.user) + ' ' + str(self.evaluated_user) + ' ' + str(self.star)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'evaluated_user'], name='user_rating_unique')
        ]
        verbose_name = 'оценка пользователя'
        verbose_name_plural = 'оценки пользователей'
