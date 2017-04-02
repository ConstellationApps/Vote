import json
import datetime

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views import View

from constellation_base.models import GlobalTemplateSettings

from .models import (
    Poll,
    PollOption
)


def index(request):
    """Return index text"""
    return HttpResponse("foo!")


class manage_poll(View):
    def get(self, request, pollID=None):
        """ Returns a page that allows for the creation of a poll """
        template_settings = GlobalTemplateSettings(allowBackground=False)
        template_settings = template_settings.settings_dict()

        poll = None
        pollOptions = None

        # If pollID was set, get that poll and its options to edit
        if pollID is not None:
            poll = Poll.objects.get(pk=pollID)
            pollOptions = list(PollOption.objects.get(poll=poll))

        return render(request, 'constellation_vote/manage-poll.html', {
            'template_settings': template_settings,
            'poll': poll,
            'pollOptions': pollOptions,
            'visible_groups': [(g.name, g.pk) for g in Group.objects.all()]
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

            pollOptionsDict = pollDict["options"]
            if pollOptionsDict["starts"] != "":
                newPoll.starts = datetime.datetime(pollInfoDict["starts"])
            if pollOptionsDict["ends"] != "":
                newPoll.ends = datetime.datetime(pollInfoDict["ends"])

            owning_group = Group.objects.get(name=pollOptionsDict["owned_by"])
            newPoll.owned_by = owning_group

            # Checkboxes don't POST if they aren't checked
            if "results_visible" in pollOptionsDict:
                newPoll.results_visible = True
            else:
                newPoll.results_visible = False

            newPoll.full_clean()
            newPoll.save()

            # Now we create the options
            for option in pollDict["choices"]:
                newOption = PollOption()
                newOption.poll = newPoll
                newOption.text = option["text"]
                if "desc" in option:
                    newOption.desc = option["desc"]
                newOption.save()
            # If we've made it this far, the poll itself is saved
        except ValidationError:
            newPoll.delete()
            return HttpResponseBadRequest("Poll could not be created!")

        return HttpResponse(pollDict)
