from django.conf.urls import url
from Centre import views


urlpatterns = [
    url(r'^api/vaccin$', views.vaccin_list),
    url(r'^api/vaccin/(?P<pk>[0-9]+)$', views.vaccin_detail),
    url(r'^api/vaccin/(?P<pk>[0-9]+)/lot$', views.lot_liste),
    url(r'^api/lot$', views.lot_detail),
]