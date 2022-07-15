from django.urls import path
from .import views


urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('register/',views.user_register,name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('',views.dashboard,name="dashboard"),

    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    

]


