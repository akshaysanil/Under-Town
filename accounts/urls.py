from django.urls import path
from .import views


urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('register/',views.user_register,name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('dashboard/',views.dashboard,name="dashboard"),
    # path('',views.dashboard,name="dashboard"),

    path('activate/<uidb64>/<token>/',views.activate,name='activate'),

    path('my_orders/',views.my_orders, name="my_orders"),
    path('edit_profile/',views.edit_profile, name="edit_profile"),
    path('change_password/',views.change_password, name="change_password"),
    path('order_detail/<int:order_id>/',views.order_detail, name="order_detail"),



    

]


