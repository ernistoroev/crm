from django.db import models
from django.contrib.auth.models import AbstractUser


class Student(AbstractUser):
    GENDER_CHOICES = [('М', 'Мужской'), ('Ж', 'Женский')]
    COURSE_CHOICES = [(i, f'{i} курс') for i in range(1, 5)]
    EDUCATION_FORM_CHOICES = [
        ('очная', 'Очная'),
        ('заочная', 'Заочная'),
        ('вечерняя', 'Вечерняя'),
    ]
    FUNDING_CHOICES = [('бюджет', 'Бюджет'), ('контракт', 'Контракт')]
    STATUS_CHOICES = [
        ('обучается', 'обучается'),
        ('академический отпуск', 'академический отпуск'),
        ('отчислен', 'отчислен'),
        ('выпускник', 'выпускник'),
    ]

    REQUIRED_FIELDS = ['email', 'student_id', 'course']

    middle_name = models.CharField('отчество', max_length=100, blank=True)
    birth_date = models.DateField('дата рождения', null=True, blank=True)
    gender = models.CharField('пол', max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField('телефон', max_length=20, blank=True)
    address = models.TextField('адрес', blank=True)
    photo = models.ImageField('фото', upload_to='students/', blank=True, null=True)
    student_id = models.CharField('номер студенческого билета', max_length=20, unique=True)
    group = models.CharField('учебная группа', max_length=20)
    specialty = models.CharField('специальность', max_length=150)
    course = models.PositiveSmallIntegerField('курс', choices=COURSE_CHOICES)
    admission_year = models.PositiveSmallIntegerField('год поступления', blank=True, null=True)
    education_form = models.CharField('форма обучения', max_length=20, choices=EDUCATION_FORM_CHOICES)
    funding = models.CharField('основа обучения', max_length=20, choices=FUNDING_CHOICES)
    status = models.CharField('статус', max_length=20, choices=STATUS_CHOICES, default='обучается')
    created_at = models.DateTimeField('создан', auto_now_add=True)
    updated_at = models.DateTimeField('изменён', auto_now=True)

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенты'
        ordering = ['last_name', 'first_name']

    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'.strip()

    def __str__(self):
        return f'{self.full_name} ({self.group})'
