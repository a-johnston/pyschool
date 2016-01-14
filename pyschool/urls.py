from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^submit/$', views.submit_challenge, name='submit')
]
