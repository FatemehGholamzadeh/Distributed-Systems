from django.urls import include, path
from submissions import views

app_name = 'submissions'
urlpatterns = [
    path('', views.SubmissionListView.as_view(), name='submission_home'),
    path('<int:submission_id>/', views.SubmissionDetailView.as_view(), name='submission_detail'),
    path('submit/<slug:problemslug>/', views.SubmissionCacheView.as_view(), name='submit_code'),
]
