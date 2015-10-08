from django.conf.urls import url, patterns
from django.conf import settings
from django.views.generic.base import RedirectView

from naturebank import views
from naturebank.models import Biotope, Species

biotope_list = {
    'queryset': Biotope.objects.all(),
    'allow_empty': True,
    'extra_context': {}
}

species_list = {
    'queryset': Species.objects.all(),
    'allow_empty': True,
    'extra_context': {}
}

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(url='/home/'), name='index'),
    url(r'^biotopes/$', views.BiotopeListView.as_view(), name='biotope_list'),
    url(r'^biotopes/d/(?P<pk>\d+)/$', views.BiotopeDetailView.as_view(),
        name='biotope_detail'),
    url(r'^biotopes/c/(?P<site_code>[^/]+)/$',
        views.BiotopeDetailView.as_view(), name='biotope_detail'),
    url(r'^biotopes/b/(?P<pk>\d+)/$', views.BiotopeDetailBriefView.as_view(),
        name='biotope_brief'),
    (r'^biotope_list_filter/(?P<filter_name>[^/]+)/$',
     views.biotope_list_filter),
    url(r'^species/$', views.SpeciesListView.as_view(), name='species_list'),
    url(r'^species/d/(?P<pk>\d+)/$', views.SpeciesDetailView.as_view(),
        name='species_detail'),
    (r'^(?P<layer>[^/]+)/kml/$', views.kml, {}),
    (r'^bound/$', views.bound, {}),
    (r'^settlements/$', views.settlements_kml, {}),
    url(r'^favicon\.ico$', RedirectView.as_view(
        url=settings.STATIC_URL + 'favicon.ico'), name='favicon'),
)
