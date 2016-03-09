from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/candidate/(?P<candidateID>[0-9]+)$', views.detail),
    url(r'^listCandidates$', views.listCandidates),
    url(r'^cast$', views.castVote),
    url(r'^add$', views.add),
    url(r'^results$', views.results),
    url(r'^login$', views.login_view),
    url(r'^logout$', views.logout_view),
]
