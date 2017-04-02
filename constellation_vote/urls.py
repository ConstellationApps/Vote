from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index$', views.index, name='index'),

    url(r'^manage/poll$', views.manage_poll.as_view(),
        name="manage_poll"),
]
