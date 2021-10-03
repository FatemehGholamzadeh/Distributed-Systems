from django.shortcuts import render, redirect, get_object_or_404
from submissions.models import SubmissionCache, MainSubmission, lang_dictionary
from django.views.generic import (CreateView, ListView, DetailView)
from django.contrib.auth.mixins import (LoginRequiredMixin, )
from submissions.forms import SubmissionForm
from django.core.files.base import ContentFile
from problems.models import Problem
from django.urls import reverse_lazy
from private_storage.views import PrivateStorageDetailView
from coders.models import UserProfile


# BASE_CACHE_SUBMISSION_PATH = 'submissions/cache/'
# BASE_MAIN_SUBMISSION_PATH = 'submissions/main/'
SOLUTIONS_VISIBLE = False       # Set true to make solutions visible to all the user

class SubmissionCacheView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = reverse_lazy('homepage')
    template_name = 'submissions/submit_code.html'
    form_class = SubmissionForm
    success_url = reverse_lazy('homepage')
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form':form, 'problem':self.kwargs['problemslug']})
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_cache_submission = form.save(commit = False)
            new_cache_submission.user_handle = request.user
            new_cache_submission.actual_language = lang_dictionary[form.cleaned_data['language']]
            problemObj = get_object_or_404(Problem, slug=self.kwargs['problemslug'])
            new_cache_submission.problem_submitted = problemObj
            src_code = form.cleaned_data['Source_Code']
            new_cache_submission.save()
            new_cache_submission.solution.save('',ContentFile(src_code))
            new_main_submission = MainSubmission.objects.create(
            created_date = new_cache_submission.created_date,
            user_handle = new_cache_submission.user_handle,
            problem_submitted = new_cache_submission.problem_submitted,
            language = new_cache_submission.language,
            actual_language = new_cache_submission.actual_language,
            )
            new_main_submission.save()
            new_main_submission.solution.save('', ContentFile(form.cleaned_data['Source_Code']))
            new_cache_submission.sidno = new_main_submission.id
            new_cache_submission.save()
            print('New Submission -\nProblem - {}\nUser - {}\nCacheSubmissionID - {}\nMainSubmissionID - {}'
            .format(problemObj.slug, request.user, new_cache_submission.id, new_main_submission.id))
            return redirect('homepage')
        return render(request, self.template_name, {'form':form})

class SubmissionListView(ListView):
    model = MainSubmission
    template_name = 'submissions/submission_list.html'
    queryset = MainSubmission.objects.all().order_by('-id')
    context_object_name = 'submissions_list'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_solutions_visible'] = SOLUTIONS_VISIBLE
        return context

class SubmissionDetailView(DetailView):
    model = MainSubmission
    slug_field = 'id'
    slug_url_kwarg = 'submission_id'
    template_name = 'submissions/submission_detail.html'
    # Include a can_access_function for restricting view to only the submitters
    def get(self, request, *args, **kwargs):
        submissionObj = get_object_or_404(MainSubmission, id=self.kwargs['submission_id'])
        if (request.user == submissionObj.user_handle) or (request.user in UserProfile.objects.filter(is_staff=True) or SOLUTIONS_VISIBLE) :
            solution_file = open(submissionObj.solution.path, 'r')
            src_code = solution_file.read()
            solution_file.close()
            return render(request, self.template_name, {'submission':submissionObj, 'src_code':src_code})
        else:
            return render(request, 'forbidden.html')


class ProblemSubmissionListView(ListView):
    model = MainSubmission
    template_name = 'submissions/submission_list.html'
    context_object_name = 'submissions_list'
    paginate_by = 10
    def get_queryset(self):
        problem_slug = self.kwargs['slug']
        problem = Problem.objects.get(slug=problem_slug)
        return problem.problem_m_submission.all().order_by('-id')

class MySubmissionListView(ListView):
    model = MainSubmission
    template_name = 'submissions/submission_list.html'
    context_object_name = 'submissions_list'
    paginate_by = 10
    def get_queryset(self):
        urlusername = self.kwargs['username']
        user = UserProfile.objects.get(username=urlusername)
        return user.user_m_submission.all().order_by('-id')
