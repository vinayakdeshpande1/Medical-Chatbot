from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('customerclick', views.customerclick_view,name='customerclick'),
    path('customersignup', views.customer_signup_view,name='customersignup'),
    path('customer-dashboard', views.customer_dashboard_view,name='customer-dashboard'),
    path('customerlogin', LoginView.as_view(template_name='medical/adminlogin.html'),name='customerlogin'),
    path('eng',views.eng.as_view(),name="eng"),
    path('engm',views.engm.as_view(),name="engm"),
    path('engh',views.engh.as_view(),name="engh"),
    
]