from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'username', 'last_name', 'first_name', 'middle_name', 'email',
            'birth_date', 'gender', 'phone', 'address', 'photo',
            'student_id', 'group', 'specialty', 'course', 'admission_year',
            'education_form', 'funding', 'status',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class StudentCreateForm(StudentForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password1') != cleaned_data.get('password2'):
            self.add_error('password2', 'Пароли не совпадают')
        return cleaned_data

    def save(self, commit=True):
        student = super().save(commit=False)
        student.set_password(self.cleaned_data['password1'])
        if commit:
            student.save()
        return student
