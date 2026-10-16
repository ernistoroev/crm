from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, style={'input_type': 'password'})
    group_name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'username', 'password', 'last_name', 'first_name', 'middle_name', 'email',
            'birth_date', 'gender', 'phone', 'address', 'student_id', 'group', 'group_name',
            'course', 'admission_year', 'education_form', 'funding', 'status',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        student = Student(**validated_data)
        student.set_password(password)
        student.save()
        return student

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
