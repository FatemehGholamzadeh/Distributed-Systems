from django.shortcuts import render, redirect, get_object_or_404
from problems.models import Problem
from django.views.generic import (CreateView, ListView, DetailView, UpdateView)
from problems.forms import ProblemUploadForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin,)
import subprocess
import os


class ProblemView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = reverse_lazy('homepage')
    permission_required = 'coders.can_set_problems'
    template_name = 'problems/post_problem.html'
    form_class = ProblemUploadForm
    success_url = reverse_lazy('homepage')
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_problem = form.save(commit=False)
            new_problem.setter = request.user
            new_problem.save()
            print('New Problem Posted-\nProblem Name - {}\nSetter - {}'.format(form.cleaned_data['problem_name'], request.user))
            # Extract test cases from zip file
            testFileUnzip = subprocess.Popen(['unzip', '-o', new_problem.test_file.path, '-d', os.path.dirname(new_problem.test_file.path)])
            testFileUnzip.wait()
            return redirect('homepage')
        return render(request, self.template_name, {'form':form})

class ProblemUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        try:
            obj = Problem.objects.get(setter=self.request.user, slug=self.kwargs['slug'])
            return True
        except Problem.DoesNotExist:
            return False
    login_url = '/login'
    model = Problem
    template_name = 'problems/post_problem.html'
    form_class = ProblemUploadForm
    redirect_field_name = reverse_lazy('homepage')
    permission_required = 'coders.can_set_problems'


class ProblemListView(ListView):
    model = Problem
    template_name = 'problems/problem_list.html'
    queryset = Problem.objects.all().order_by('id')
    context_object_name = 'problems_list'
    paginate_by = 20

class ProblemDetailView(DetailView):
    model = Problem
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    template_name = 'problems/problem_detail.html'
    context_object_name = 'probleminfo'
    def get_queryset(self):
        return Problem.objects.filter(slug=self.kwargs['slug'])
