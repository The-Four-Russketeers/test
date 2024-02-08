from django.urls import path
from . import views #imports main function from .views in api folder

urlpatterns = [
   path('login', views.UserLogin.as_view(), name='login'),
	path('logout', views.UserLogout.as_view(), name='logout'),
   path('user', views.UserView.as_view(), name='user'),
   path('showSchedule', views.showSchedule.as_view(), name = "showSchedule"),
]
