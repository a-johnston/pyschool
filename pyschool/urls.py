from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^$', views.index, name='index'),
    url(r'^post/$', views.post_test, name='post_test'),
    url(r'^register/$', views.register, name='register'),
    url(r'^accounts/profile/$', views.login, name='index')
]
