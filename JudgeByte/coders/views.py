from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from coders.forms import UserProfileCreationForm
from django.contrib.auth import login, authenticate
from coders.models import UserProfile
from django.utils.crypto import get_random_string
from django.views.generic.edit import FormView
from coders.forms import GenerateRandomUserForm
from django.contrib import messages
from coders.userGenerate import create_random_user_accounts

class SignUpCreateView(CreateView):
    form_class = UserProfileCreationForm
    # success_url = reverse_lazy('coders:login')
    template_name = 'coders/signup.html'
    def get(self, request, *args, **kwargs):
         form = self.form_class()
         return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save()
            name = form.cleaned_data['name']
            handle = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            print('New User registered-\nName - {}\nHandle - {}'.format(name,handle))
            user = authenticate(username=handle,password=raw_password)
            login(request, user)
            return redirect('homepage')
        return render(request, self.template_name, {'form':form})

class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'coders/user_info.html'
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "userprofile"     #Used for setting custom object name for html templates
    def get_queryset(self):
        username_c = self.kwargs["username"]
        return UserProfile.objects.filter(username=username_c)

class GenerateRandomUserView(FormView):
    template_name = 'coders/generate_random_users.html'
    form_class = GenerateRandomUserForm

    class GenerateRandomUserView(FormView):
        template_name = 'coders/generate_random_users.html'
        form_class = GenerateRandomUserForm

        def form_valid(self, form):
            total = form.cleaned_data.get('total')
            create_random_user_accounts(total)
            form.save()
            messages.success(self.request, 'We are generating your random users! Wait a moment and refresh this page.')

            return redirect('homepage')
