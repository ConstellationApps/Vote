import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .models import Poll
from .models import PollOption


def index(request):
    """Return index text"""
    return HttpResponse("foo!")


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
