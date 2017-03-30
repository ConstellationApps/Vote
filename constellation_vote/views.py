import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render
from django.views import View

from constellation_base.models import GlobalTemplateSettings

from .models import (
    Poll,
    PollOption
)


def index(request):
    """Return index text"""
    return HttpResponse("foo!")


class manage_create_poll(View):
    def get(self, request):
        """ Returns a page that allows for the creation of a poll """
        template_settings = GlobalTemplateSettings(allowBackground=False)
        template_settings = template_settings.settings_dict()

        return render(request, 'constellation_vote/create-poll.html', {
            'template_settings': template_settings,
        })

    def post(self, request):
        """ Creates a poll """
        return HttpResponse("bar!")


def api_v1_polloption_add(request):
    """Take in JSON that includes the fields of the option"""
    pollOption = json.load(request.body.text)
    tmpOption = PollOption()

    tmpOption.text = pollOption["text"]
    if "desc" in pollOption:
        tmpOption.desc = pollOption["desc"]
    tmpOption.poll = Poll.objects.get(pollOption["poll"])

    try:
        tmpOption.save()
    except ValidationError:
        return HttpResponseBadRequest("Improperly formatted option addition")

    return HttpResponse("Option Added")


def api_v1_polloption_del(request):
    """Attempt to get and subsequently delete a poll option"""
    po = get_object_or_404(PollOption, pk=request.body.text)
    po.delete()
    return HttpResponse("Poll option deleted")
