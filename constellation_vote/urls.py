from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^view/list$', views.view_list, name='view_list'),

    url(r'^manage/poll$', views.manage_poll.as_view(),
        name="manage_poll"),
    url(r'^manage/poll/(?P<poll_id>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})$',
        views.manage_poll.as_view(),
        name="manage_poll"),
]
