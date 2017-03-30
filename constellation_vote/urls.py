from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index$', views.index, name='index'),

    url(r'^manage/create-poll$', views.manage_create_poll.as_view(),
        name="manage_create_poll"),
]
