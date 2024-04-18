from django.urls import path
from . import views #imports main function from .views in api folder

urlpatterns = [
   path('login', views.UserLogin.as_view(), name='login'),
	path('logout', views.UserLogout.as_view(), name='logout'),
   path('user', views.UserView.as_view(), name='user'),
   path('getTNum', views.getTnum.as_view(), name = "getTNum"),
   path("test", views.test.as_view(), name = "test"),
   path("getClassesNeeded", views.getClassesNeeded.as_view(), name = "getClassesNeeded"),
   path("test2",views.test2.as_view(), name = "test2"),
]
