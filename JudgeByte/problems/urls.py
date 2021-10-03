from django.urls import include, path
from problems import views
from submissions import views as subviews

app_name = 'problems'
urlpatterns = [
    path('new/', views.ProblemView.as_view(), name='new_problem'),
    path('problemset/<slug:slug>/submissions', subviews.ProblemSubmissionListView.as_view(), name='problem_submissions'),
    path('problemset/<slug:slug>/update', views.ProblemUpdateView.as_view(), name='problem_update'),
    path('problemset/<slug:slug>/', views.ProblemDetailView.as_view(), name='problem_page'),
    path('problemset/', views.ProblemListView.as_view(), name='problem_list'),
    # path('profile/<str:username>/', views.UserProfileDetailView.as_view(), name='user_info')

]
