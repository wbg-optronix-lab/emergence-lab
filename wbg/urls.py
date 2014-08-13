from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
import django.contrib
from rest_framework.urlpatterns import format_suffix_patterns

import core.views
import growths.views
import afm.api


admin.autodiscover()

urlpatterns = patterns(
    'django.contrib.auth.views',
    # urls, add login_required() around the as_view() call for security

    # misc urls
    url(r'^$', core.views.homepage.as_view(), name='home'),
    url(r'^media/(?P<filename>.*)$', login_required(core.views.protected_media)),
    url(r'^quicksearch/', login_required(core.views.QuickSearchRedirect.as_view()), name='quicksearch'),
    url(r'^exception/', login_required(core.views.ExceptionHandlerView.as_view()), name='exception'),
    url(r'^accounts/login/', login, {'template_name': 'core/login.html'}, name='login'),
    url(r'^accounts/logout/', logout, {'template_name': 'core/logout.html'}, name='logout'),
    url(r'^wbg-admin/', include(admin.site.urls)),

    # core urls
    url(r'^operators/$', login_required(core.views.operator_list.as_view()), name='operator_list'),
    url(r'^operators/create/$', login_required(core.views.operator_create.as_view()), name='operator_create'),
    url(r'^platters/$', login_required(core.views.platter_list.as_view()), name='platter_list'),
    url(r'^projects/$', login_required(core.views.project_list.as_view()), name='project_list'),
    url(r'^projects/(?P<slug>[\w-]+)/$', login_required(core.views.ProjectDetailView.as_view()), name='project_detail_all'),
    url(r'^dashboard/(?P<slug>[\w-]+)/$', login_required(core.views.ProjectDetailDashboardView.as_view()), name='project_detail_dashboard'),
    url(r'^investigations/$', login_required(core.views.investigation_list.as_view()), name='investigation_list'),

    # growths urls
    url(r'^growths/search/$', login_required(growths.views.growth_list.as_view()), name='afm_filter'),
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/$', login_required(growths.views.GrowthDetailView.as_view()), name='growth_detail'),
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/recipe/$', login_required(growths.views.recipe_detail.as_view()), name='recipe_detail'),
    url(r'^(?P<growth>[gt][1-9][0-9]{3,})/(?P<pocket>\d+\-?\d*)/$', login_required(growths.views.SampleFamilyDetailView.as_view()), name='sample_family_detail'),
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/readings/$', login_required(growths.views.readings_detail.as_view()), name='readings_detail'),
    url(r'^(?P<slug>[gt][1-9][0-9]{3,})/readings/update/$', login_required(growths.views.update_readings.as_view()), name='update_readings'),
    url(r'^sample/(?P<pk>\d+)/$', login_required(growths.views.SampleDetailView.as_view()), name='sample_detail'),
    url(r'^sample/split/$', login_required(growths.views.SplitSampleView.as_view()), name='split_sample'),

    # dashboard views
    url(r'^dashboard/$', login_required(core.views.Dashboard.as_view()), name='profile_dashboard'),

    # creategrowth urls
    url(r'^creategrowth/start/$', login_required(growths.views.CreateGrowthStartView.as_view()), name='create_growth_start'),
    url(r'^creategrowth/prerun/$', login_required(growths.views.CreateGrowthPrerunView.as_view()), name='create_growth_prerun'),
    url(r'^creategrowth/readings/$', login_required(growths.views.create_growth_readings.as_view()), name='create_growth_readings'),
    url(r'^creategrowth/postrun/$', login_required(growths.views.create_growth_postrun), name='create_growth_postrun'),

    # afm urls
    url(r'^afm/', include('afm.urls')),
    url(r'^api/v0/afm/$', afm.api.AFMListAPI.as_view()),
    url(r'^api/v0/afm/(?P<pk>\d+)/$', afm.api.AFMDetailAPI.as_view()),

    # hall urls
    url(r'^hall/$', include('hall.urls')),
    
    # user-specific views
    url(r'^(?P<username>[\w-]+)/(?P<slug>[\w-]+)/$', login_required(core.views.ProjectDetailView.as_view()), name='project_detail_user'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
