from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Student

PERSONAL_FIELDS = ('middle_name', 'birth_date', 'gender', 'phone', 'address', 'photo')
STUDY_FIELDS = (
    'student_id', 'group', 'course', 'admission_year',
    'education_form', 'funding', 'status',
)


@admin.register(Student)
class StudentAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Личные данные студента', {'fields': PERSONAL_FIELDS}),
        ('Учёба', {'fields': STUDY_FIELDS}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('ФИО', {'fields': ('last_name', 'first_name', 'email')}),
        ('Личные данные студента', {'fields': PERSONAL_FIELDS}),
        ('Учёба', {'fields': STUDY_FIELDS}),
    )
    list_display = ('username', 'last_name', 'first_name', 'middle_name', 'student_id', 'group', 'course', 'status')
    search_fields = ('username', 'last_name', 'first_name', 'middle_name', 'student_id')
    list_filter = ('group', 'course', 'status')
