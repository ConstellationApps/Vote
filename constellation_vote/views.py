import json

from datetime import datetime

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views import View

from guardian.shortcuts import assign_perm

from constellation_base.models import GlobalTemplateSettings

from .models import (
    Poll,
    PollOption
)


def index(request):
    """Return index text"""
    return HttpResponse("foo!")


def view_list(request):
    ''' Returns a page that includes a list of submitted forms '''
    template_settings = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings.settings_dict()
    polls = Poll.objects.all()

    return render(request, 'constellation_vote/list.html', {
        'template_settings': template_settings,
        'polls': polls,
    })


class manage_poll(View):
    def get(self, request, poll_id=None):
        """ Returns a page that allows for the creation of a poll """
        template_settings = GlobalTemplateSettings(allowBackground=False)
        template_settings = template_settings.settings_dict()

        poll = None
        pollOptions = None

        # If poll_id was set, get that poll and its options to edit
        if poll_id is not None:
            poll = Poll.objects.get(pk=poll_id)
            pollOptions = serializers.serialize(
                "json", PollOption.objects.filter(poll=poll))

        return render(request, 'constellation_vote/manage-poll.html', {
            'template_settings': template_settings,
            'poll': poll,
            'pollOptions': pollOptions,
            'visible_groups': [(g.name, g.pk) for g in Group.objects.all()]
            })

    def post(self, request, poll_id=None):
        """ Creates a poll """
        pollDict = json.loads(request.POST["data"])
        try:
            # Try creating the poll and if that fails, then we won't put in
            # options
            pollInfoDict = pollDict["meta"]
            pollOptionsDict = pollDict["options"]
            poll, c = Poll.objects.get_or_create(pk=poll_id)

            poll.title = pollInfoDict["title"]
            poll.desc = pollInfoDict["desc"]

            if pollOptionsDict["starts"] != "":
                poll.starts = datetime.strptime(pollOptionsDict["starts"],
                                                "%m/%d/%Y %H:%M")
            if pollOptionsDict["ends"] != "":
                poll.ends = datetime.strptime(pollOptionsDict["ends"],
                                              "%m/%d/%Y %H:%M")

            owning_group = Group.objects.get(name=pollOptionsDict["owner"])
            poll.owned_by = owning_group

            # Checkboxes don't POST if they aren't checked
            if "results_visible" in pollOptionsDict:
                poll.results_visible = True
            else:
                poll.results_visible = False

            poll.full_clean()
            poll.save()

            # Now we create the options
            for optionDict in pollDict["choices"]:
                opt_ID = None
                if "uuid" in optionDict:
                    opt_ID = optionDict["uuid"]
                opt, c = PollOption.objects.get_or_create(pk=opt_ID)
                opt.poll = poll
                opt.text = optionDict["text"]
                if "desc" in optionDict:
                    opt.desc = optionDict["desc"]
                if "active" in optionDict:
                    opt.active = True
                else:
                    opt.active = False
                opt.save()
            # If we've made it this far, the poll itself is saved
            # Now we can set the permissions on this object
            visibleGroup = Group.objects.get(name=pollOptionsDict["visible"])
            assign_perm("poll_visible", visibleGroup, poll)

        except ValidationError:
            poll.delete()
            return HttpResponseBadRequest("Poll could not be created!")

        return HttpResponse(pollDict)
