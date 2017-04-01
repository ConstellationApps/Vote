import uuid

from django.contrib.auth.models import User
from django.db import models


class Poll(models.Model):
    """Model for the Poll Itself"""
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False)

    title = models.CharField(max_length=128)
    desc = models.TextField(blank=True, null=True)

    starts = models.DateTimeField(auto_now=True)
    ends = models.DateTimeField(blank=True, null=True)

    archived = models.BooleanField(default=False)


class PollOption(models.Model):
    """Model for the individual Poll Options"""
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=75)
    desc = models.TextField(blank=True, null=True)


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
