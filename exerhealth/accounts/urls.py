from django.urls import path
from exerhealth.accounts import views

app_name = 'accounts'

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('profile/', views.profile_page, name='profile'),
    path('profile/bmi_calculator/', views.bmi_calculator, name='bmi_calculator'),
    path('profile/bmi_calculator/bmi_plot', views.bmi_plot, name='bmi_plot'),

]
