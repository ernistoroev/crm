from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from rest_framework import mixins, viewsets
from academics.models import Group
from .serializers import StudentSerializer
from .forms import StudentCreateForm, StudentForm
from .models import Student


class StudentListView(ListView):
    model = Student
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().select_related('group')
        q = self.request.GET.get('q', '').strip()
        group = self.request.GET.get('group', '')
        if q:
            # SQLite не умеет искать без учёта регистра по кириллице,
            # поэтому ищем и введённый текст, и вариант с заглавной буквы
            condition = Q()
            for word in {q, q.capitalize()}:
                condition |= (
                    Q(last_name__icontains=word)
                    | Q(first_name__icontains=word)
                    | Q(middle_name__icontains=word)
                )
            queryset = queryset.filter(condition)
        if group.isdigit():
            queryset = queryset.filter(group_id=group)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['q'] = self.request.GET.get('q', '')
        context['current_group'] = self.request.GET.get('group', '')
        return context


class StudentDetailView(DetailView):
    model = Student
    context_object_name = 'student'


class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentCreateForm

    def get_success_url(self):
        return reverse('users:detail', args=[self.object.pk])


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    context_object_name = 'student'

    def get_success_url(self):
        return reverse('users:detail', args=[self.object.pk])


class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    context_object_name = 'student'
    success_url = reverse_lazy('users:list')

class StudentViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Student.objects.select_related('group')
    serializer_class = StudentSerializer



