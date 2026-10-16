from django.test import TestCase

from users.models import Student
from users.serializers import StudentSerializer

from .models import Direction, Faculty, Group
from .serializers import DirectionSerializer, GroupSerializer


class SerializerTests(TestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(name='Информационные технологии', short_name='ИТ')
        self.direction = Direction.objects.create(code='09.02.07', name='Информационные системы', faculty=self.faculty)
        self.group = Group.objects.create(name='ИС-21', direction=self.direction, admission_year=2024)

    def test_related_names_in_output(self):
        self.assertEqual(DirectionSerializer(self.direction).data['faculty_name'], 'Информационные технологии')
        data = GroupSerializer(self.group).data
        self.assertEqual(data['direction'], self.direction.pk)
        self.assertEqual(data['direction_name'], 'Информационные системы')
        self.assertEqual(data['faculty_name'], 'Информационные технологии')

    def student_payload(self, **kwargs):
        payload = {
            'username': 'ivanov', 'password': 'secret12345', 'last_name': 'Иванов',
            'first_name': 'Иван', 'gender': 'М', 'student_id': 'S-001', 'group': self.group.pk,
            'course': 1, 'education_form': 'очная', 'funding': 'бюджет',
        }
        payload.update(kwargs)
        return payload

    def test_student_password_hashed_and_hidden(self):
        serializer = StudentSerializer(data=self.student_payload())
        self.assertTrue(serializer.is_valid(), serializer.errors)
        student = serializer.save()
        self.assertTrue(student.check_password('secret12345'))
        self.assertNotIn('password', serializer.data)
        self.assertEqual(serializer.data['group_name'], 'ИС-21')

    def test_student_id_unique(self):
        Student.objects.create_user(username='other', student_id='S-001', course=1)
        serializer = StudentSerializer(data=self.student_payload())
        self.assertFalse(serializer.is_valid())
        self.assertIn('student_id', serializer.errors)
