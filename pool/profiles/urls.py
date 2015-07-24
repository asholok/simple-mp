from django.conf.urls import patterns, url
from profiles import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("",
    url(r'^$', TemplateView.as_view(template_name='create_profile.html'), name='index'),
    url(r'^edit/$', login_required(TemplateView.as_view(template_name='edit_profile.html')), name='edit'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
)

