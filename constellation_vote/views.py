import json
import datetime

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
        pollDict = json.loads(request.POST["data"])
        try:
            # Try creating the poll and if that fails, then we won't put in
            # options
            pollInfoDict = pollDict["meta"]
            newPoll = Poll()
            newPoll.title = pollInfoDict["title"]
            newPoll.desc = pollInfoDict["desc"]
            if "starts" in pollInfoDict:
                newPoll.starts = datetime.datetime(pollInfoDict["starts"])
            if "ends" in pollInfoDict:
                newPoll.ends = datetime.datetime(pollInfoDict["ends"])


            newPoll.full_clean()
            newPoll.save()
            pollID = newPoll.id

            # Now we create the options
            for option in pollDict["choices"]:
                newOption = PollOption()
                newOption.poll = pollID
                newOption.text = option["text"]
                if "desc" in option:
                    newOption.desc = option["desc"]
                newOption.save()
            # If we've made it this far, the poll itself is saved
        except ValidationError:
            return HttpResponseBadRequest("Poll could not be created!")

        return HttpResponse(pollDict)
