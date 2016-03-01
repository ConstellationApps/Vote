from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import RequestContext, loader

from . import vote_summation

import json
import logging
import time

logger = logging.getLogger(__name__)

from .models import Candidate, Vote


def index(request):
    candidate_list = Candidate.objects.all()
    template = loader.get_template('vote/index.html')
    return HttpResponse(template.render({'candidate_list': candidate_list}, request))

def faq(request):
    return HttpResponse("FAQ")

def detail(request, candidateID):
    candidate = get_object_or_404(Candidate, pk=candidateID)
    candidateDict = { "name":candidate.name,
                      "info":candidate.description,
                      "id":candidate.id}
    return HttpResponse(json.dumps(candidateDict))

def listCandidates(request):
    candidates = Candidate.objects.all()
    candidateDict = dict()
    for candidate in candidates:
        candidateDict[candidate.id]=candidate.name
    return HttpResponse(json.dumps(candidateDict))

def castVote(request):
    voterUID = "test"
    voteTS = str(time.strftime("%Y-%m-%d %H:%M:%S%z"))

    # get a list of people who've voted
    uids = list()
    for uid in Vote.objects.all():
        uids.append(uid.uid)

    if False: #voterUID in uids:
        # double vote detected, alert the user
        logger.warning("{} attempted double vote.".format(voterUID))
        return HttpResponse(status=423)
    else:
        # normal single vote
        try:
            logger.info("{} is trying to case vote for {} at {}".format(voterUID, request.POST.get('vote', ''), voteTS))
            v = Vote(uid=voterUID, order=request.POST.get('vote', ''), timestamp = voteTS)
            v.save()
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(status=500)

def add(request):
    proposedCandidate = request.POST.get('name', '')
    candidates = Candidate.objects.all()
    candidateDict = dict()
    for candidate in candidates:
        candidateDict[candidate.id]=candidate.name.lower()

    if False:
        # this check should determine if the candidate is banned
        # mainly intended to deal with joke votes, this check
        # must be first to work correctly
        return HttpResponse(status=418)
    if proposedCandidate.lower() not in candidateDict.values():
        # candidate doesn't exist, return add success
        try:
            c = Candidate(name=proposedCandidate, description="This is a write-in candidate")
            c.save()
            print("Added candidate {0} with id {1}".format(proposedCandidate, c.id))
            return HttpResponse(c.id, status=200)
        except Exception as e:
            print(e)
            return HttpResponse(status=500)
    else:
        # candidate exists
        return HttpResponse(status=409)

def findWinners(request):
    ballots = list()
    for ballot in Vote.objects.all():
        print(ballot)
        print(ballot.order.split(','))
        marks = list()
        for mark in ballot.order.split(','):
            marks.append(int(mark))
        ballots.append(marks)

    print(ballots)
    box = vote_summation.Vote(ballots)
    box.computeWinners()
    return HttpResponse(json.dumps(box.getWinners()))
