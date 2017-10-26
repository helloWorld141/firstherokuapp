from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.test, name='test'),
	url(r'^dims$', views.dims, name='dims'),
	url(r'^testws_cam$', views.testWSCam, name='testWSCam'),
	url(r'^testws_staff$', views.testWSStaff, name='testWSStaff'),
]