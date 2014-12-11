from django.conf.urls import patterns, url
from simulations import views
from simulations import models
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = patterns('',
    url(r'^new/$', login_required(views.SimulationCreate.as_view()), name='create_form'),
    url(r'^edit/(?P<pk>\d+)/$', login_required(never_cache(views.SimulationEdit.as_view())), name='simulation_edit'),
    url(r'^cancel/(?P<pk>\d+)/$', login_required(never_cache(views.SimulationCancel.as_view())), name='simulation_cancel'),
    url(r'^$', login_required(views.SimulationLanding.as_view()), name='simulation_landing'),
    url(r'^management$', staff_member_required(views.SimulationManagement.as_view()), name='simulation_management'),
    url(r'^start_instance/(?P<instance_id>[a-z0-9\-]+)$', staff_member_required(views.StartInstance.as_view()), name='start_instance'),
    url(r'^stop_instance/(?P<instance_id>[a-z0-9\-]+)$', staff_member_required(views.StopInstance.as_view()), name='stop_instance'),
)