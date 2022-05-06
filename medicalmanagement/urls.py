
from django.contrib import admin
from django.urls import path
from medical import views
from django.contrib.auth.views import LogoutView,LoginView
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),


    path('customer/',include('customer.urls')),
    path('',views.home_view,name=''),
    path('logout', LogoutView.as_view(template_name='medical/logout.html'),name='logout'),
    path('aboutus/', views.aboutus_view),
    #path('contactus', views.aboutus_view),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),
   
    path('adminlogin', LoginView.as_view(template_name='medical/adminlogin.html'),name='adminlogin'),


]
