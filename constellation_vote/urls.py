from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index$', views.index, name='index'),

    url(r'^manage/poll$', views.manage_poll.as_view(),
        name="manage_poll"),
    url(r'^manage/poll/[0-9a-f]{12}4[0-9a-f]{3}[89ab][0-9a-f]{15}\Z$',
        views.manage_poll.as_view(),
        name="manage_poll"),
]
