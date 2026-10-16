from django.db import models


class Faculty(models.Model):
    name = models.CharField('название', max_length=200, unique=True)
    short_name = models.CharField('сокращённое название', max_length=20, unique=True)
    dean = models.CharField('декан', max_length=200, blank=True)

    class Meta:
        verbose_name = 'факультет'
        verbose_name_plural = 'факультеты'
        ordering = ['name']

    def __str__(self):
        return self.short_name


class Direction(models.Model):
    code = models.CharField('код', max_length=20, unique=True)
    name = models.CharField('название', max_length=200)
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.PROTECT,
        related_name='directions',
        verbose_name='факультет',
    )
    duration_years = models.PositiveSmallIntegerField('срок обучения (лет)', default=4)

    class Meta:
        verbose_name = 'направление'
        verbose_name_plural = 'направления'
        ordering = ['code']

    def __str__(self):
        return f'{self.code} {self.name}'


class Group(models.Model):
    name = models.CharField('название', max_length=20, unique=True)
    direction = models.ForeignKey(
        Direction,
        on_delete=models.PROTECT,
        related_name='groups',
        verbose_name='направление',
    )
    admission_year = models.PositiveSmallIntegerField('год набора')
    is_active = models.BooleanField('активна', default=True)

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'
        ordering = ['name']

    def __str__(self):
        return self.name
