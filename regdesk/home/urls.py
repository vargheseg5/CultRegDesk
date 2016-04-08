from django.conf.urls import url, include

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^event_reg1/$', views.event_registraion_1, name='e1'),
	url(r'^event_reg2/$', views.event_registraion_2, name='e2'),
	url(r'^reg_submit/$', views.event_registration_submit, name='reg_submit'),
	url(r'^edit_reg1/$', views.edit_registration_1, name='e_r1'),
	url(r'^edit_reg2/$', views.edit_registration_2, name='e_r2'),
	url(r'^delete_reg/$', views.delete_registration, name='d_r'),
	url(r'^get_event_list/$', views.get_event_list, name='get_el'),
	url(r'^select_event/$', views.select_event, name='s_e'),
	url(r'^find_participent/$', views.find_participent_1, name='f_p'),
	url(r'^submit_participent/$', views.submit_participent, name='s_p'),
	]