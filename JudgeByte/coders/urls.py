from django.urls import include, path
from coders import views
from submissions import views as subviews

app_name = 'coders'
urlpatterns = [
    path('signup/', views.SignUpCreateView.as_view(), name='sign_up'),
    path('profile/<str:username>/', views.UserProfileDetailView.as_view(), name='user_info'),
    path('profile/<str:username>/submissions', subviews.MySubmissionListView.as_view(), name='user_submissions'),
    path('signup/generateRandomUser', views.GenerateRandomUserView.as_view(), name='random_sign_up'),

]
