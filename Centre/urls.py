from django.conf.urls import url
from Centre import views


urlpatterns = [
    url(r'^api/inscription$', views.inscription),
    url(r'^api/vaccin$', views.vaccin_list),
    url(r'^api/vaccin/(?P<pk>[0-9]+)$', views.vaccin_detail),
    url(r'^api/vaccin/(?P<pk>[0-9]+)/lot$', views.lot_liste),
    url(r'^api/lot$', views.lot_detail),
    url(r'^api/creneau/(?P<vaccin_id>[0-9]+)$', views.creneau_list),
    url(r'^api/creneau/detail$', views.detail_creneau),
    url(r'^api/creneau/reserver/(?P<idCreneau>[0-9]+)$', views.reserverCreneau),
    url(r'^api/creneau/annuler/(?P<idCreneau>[0-9]+)$', views.annulerCreneau),
    url(r'^api/creneau/mesCreneaux$', views.mesCreneaux_list),
]