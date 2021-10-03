from django.shortcuts import render
from django.urls import reverse_lazy
from submissions.models import Leaderboard
from coders.models import Faqs, UserProfile
from django.views.generic import ListView, CreateView
from coders.forms import FAQForm
from django.contrib.auth.mixins import UserPassesTestMixin

def homePage(request):
    return render(request,'home.html')
class LeaderboardListView(ListView):
    model = Leaderboard
    template_name = 'leaderboard.html'
    queryset = Leaderboard.objects.all().order_by('rank')
    context_object_name = 'coders_list'
    paginate_by = 20

class FAQListView(ListView):
    model = Faqs
    template_name = 'faqs.html'
    queryset = Faqs.objects.all().order_by('id')
    context_object_name = 'faq_list'

class FAQCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        if self.request.user in UserProfile.objects.filter(is_superuser=True):
            return True
        return False
    model = Faqs
    form_class = FAQForm
    success_url = reverse_lazy('post_faq')
    template_name = 'post_faq.html'


