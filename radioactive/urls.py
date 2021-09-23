from django.contrib import admin
from django.urls import path
from app import views
from app.forms import *
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.SignUp_View.as_view(), name="signup"),
    url(r'^addsource/$',views.SourceForm_View.as_view(), name="addsource"),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),
    url(r'^dashboard/$',views.dashboard, name="dashboard"),
    url(r'^contact/$',views.contact, name="contact"),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='app/login.html'), name="logout"),
]
