from django.urls import path
from users.apis import views

api_v1_prefix = "api/v1"

urlpatterns = [
    path(f'{api_v1_prefix}/auth/register/',
         views.RegisterView.as_view(), name='register'),
    path(f'{api_v1_prefix}/auth/login/',
         views.LoginView.as_view(), name='login'),
]
