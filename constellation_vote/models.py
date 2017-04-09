import datetime
import uuid

from django.contrib.auth.models import User, Group
from django.db import models
from guardian.shortcuts import get_groups_with_perms


class Poll(models.Model):
    """ Model for the Poll Itself """
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False)

    title = models.CharField(max_length=128)
    desc = models.TextField(blank=True, null=True)

    starts = models.DateTimeField(auto_now=True)
    ends = models.DateTimeField(blank=True, null=True)

    owned_by = models.ForeignKey(Group, null=True, blank=True)
    results_visible = models.BooleanField(default=False)

    archived = models.BooleanField(default=False)

    @property
    def is_active(self):
        """ Returns whether or not the poll is active """
        now = datetime.datetime.now()
        return self.starts <= now <= self.ends

    @property
    def pretty_start_date(self):
        """ Returns the start date in a format acceptable to the JS """
        if self.starts:
            return self.starts.strftime("%m/%d/%Y %H:%M")
        else:
            return ""

    @property
    def pretty_end_date(self):
        """ Returns the end date in a format acceptable to the JS """
        if self.ends:
            return self.ends.strftime("%m/%d/%Y %H:%M")
        else:
            return ""

    @property
    def visible_by(self):
        """ Returns the group that has the poll_visible permission """
        visible_by = get_groups_with_perms(self, attach_perms=True)
        if visible_by:
            return list(filter(lambda x: 'poll_visible' in visible_by[x],
                               visible_by.keys()))[0]
        else:
            return ""

    class Meta:
        permissions = (
            ("poll_owned_by", "Poll Owner"),
            ("poll_visible", "Poll is Visible")
        )


class PollOption(models.Model):
    """Model for the individual Poll Options"""
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False)
    poll = models.ForeignKey(Poll,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)
    text = models.CharField(blank=True, null=True, max_length=75)
    desc = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)


class Ballot(models.Model):
    """A filled out ballot from the Poll"""
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False)
    poll = models.ForeignKey(Poll)
    owned_by = models.ForeignKey(User)

    # The selected options are stored as a colon seperated list of uuids.  It
    # would be nice to store these as real object references, but that isn't
    # really necessary and for summation its possible to use the uuid's and
    # then later reconstitute the results as options that have the friendly
    # text
    selected_options = models.TextField()
