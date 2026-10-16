from django.test import TestCase
from django.urls import reverse

from .models import Student


def make_student(**kwargs):
    data = {
        'username': 'ivanov', 'last_name': 'Иванов', 'first_name': 'Иван',
        'middle_name': 'Петрович', 'gender': 'М', 'student_id': 'S-001',
        'group': 'ИС-21', 'specialty': 'Информационные системы', 'course': 2,
        'education_form': 'очная', 'funding': 'бюджет',
    }
    data.update(kwargs)
    return Student.objects.create_user(password='pass12345', **data)


class StudentModelTests(TestCase):
    def test_full_name_and_str(self):
        student = make_student()
        self.assertEqual(student.full_name, 'Иванов Иван Петрович')
        self.assertEqual(str(student), 'Иванов Иван Петрович (ИС-21)')

    def test_full_name_without_middle_name(self):
        student = make_student(middle_name='')
        self.assertEqual(student.full_name, 'Иванов Иван')


class StudentAdminTests(TestCase):
    def test_admin_pages_open(self):
        admin_user = make_student(username='admin', student_id='A-1', is_staff=True, is_superuser=True)
        self.client.force_login(admin_user)
        self.assertEqual(self.client.get(reverse('admin:users_student_changelist')).status_code, 200)
        self.assertEqual(self.client.get(reverse('admin:users_student_add')).status_code, 200)
        self.assertEqual(self.client.get(reverse('admin:users_student_change', args=[admin_user.pk])).status_code, 200)


class StudentCrudTests(TestCase):
    def setUp(self):
        self.student = make_student()
        make_student(username='petrova', last_name='Петрова', first_name='Анна',
                     middle_name='', gender='Ж', student_id='S-002', group='ИС-22')

    def login(self):
        self.client.login(username='ivanov', password='pass12345')

    def test_list_search_and_group_filter(self):
        url = reverse('users:list')
        response = self.client.get(url)
        self.assertContains(response, 'Иванов')
        self.assertContains(response, 'Петрова')

        response = self.client.get(url, {'q': 'петрова'})
        self.assertContains(response, 'Петрова')
        self.assertNotContains(response, 'Иванов Иван')

        response = self.client.get(url, {'group': 'ИС-21'})
        self.assertContains(response, 'Иванов Иван')
        self.assertNotContains(response, 'Петрова Анна')

    def test_detail(self):
        response = self.client.get(reverse('users:detail', args=[self.student.pk]))
        self.assertContains(response, 'S-001')

    def test_create_requires_login(self):
        response = self.client.get(reverse('users:create'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('users:create'))

    def test_create_hashes_password(self):
        self.login()
        response = self.client.post(reverse('users:create'), {
            'username': 'sidorov', 'last_name': 'Сидоров', 'first_name': 'Олег',
            'gender': 'М', 'student_id': 'S-003', 'group': 'ИС-23',
            'specialty': 'Программирование', 'course': 1, 'education_form': 'заочная',
            'funding': 'контракт', 'status': 'обучается',
            'password1': 'secret123', 'password2': 'secret123',
        })
        student = Student.objects.get(username='sidorov')
        self.assertRedirects(response, reverse('users:detail', args=[student.pk]))
        self.assertTrue(student.check_password('secret123'))
        self.assertNotEqual(student.password, 'secret123')

    def test_create_password_mismatch(self):
        self.login()
        response = self.client.post(reverse('users:create'), {
            'username': 'x', 'password1': 'a', 'password2': 'b',
        })
        self.assertContains(response, 'Пароли не совпадают')

    def test_update(self):
        self.login()
        url = reverse('users:update', args=[self.student.pk])
        data = {
            'username': 'ivanov', 'last_name': 'Иванов', 'first_name': 'Иван',
            'gender': 'М', 'student_id': 'S-001', 'group': 'ИС-31',
            'specialty': 'Информационные системы', 'course': 3,
            'education_form': 'очная', 'funding': 'бюджет', 'status': 'обучается',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('users:detail', args=[self.student.pk]))
        self.student.refresh_from_db()
        self.assertEqual(self.student.group, 'ИС-31')
        self.assertEqual(self.student.course, 3)

    def test_delete_with_confirmation(self):
        self.login()
        other = Student.objects.get(username='petrova')
        url = reverse('users:delete', args=[other.pk])
        self.assertContains(self.client.get(url), 'Удалить студента?')
        response = self.client.post(url)
        self.assertRedirects(response, reverse('users:list'))
        self.assertFalse(Student.objects.filter(pk=other.pk).exists())
