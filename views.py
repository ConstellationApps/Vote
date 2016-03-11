from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from . import vote_summation, config
from .models import Candidate, Vote
from .forms import LoginForm

import json
import logging
import time
import hashlib

logger = logging.getLogger(__name__)


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return HttpResponseRedirect("/vote/ballot")
    return render(request, 'vote/login.html', {'form': form, 'organization': config.organization, 'description': config.login_description})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/vote/login")


@login_required(login_url='/vote/login')
def index(request):
    allow_write_in = False
    ballot_size = 3
    candidate_list = Candidate.objects.all()
    template = loader.get_template('vote/index.html')
    return HttpResponse(template.render({'candidate_list': candidate_list, 'allow_writins': allow_write_in, 'ballot_size': ballot_size, 'organization': config.organization, 'description': config.vote_description}, request))


def detail(request, candidateID):
    candidate = get_object_or_404(Candidate, pk=candidateID)
    candidateDict = {"name": candidate.name,
                     "info": candidate.description,
                     "id": candidate.id}
    return HttpResponse(json.dumps(candidateDict))


def listCandidates(request):
    candidates = Candidate.objects.all()
    candidateDict = dict()
    for candidate in candidates:
        candidateDict[candidate.id] = candidate.name
    return HttpResponse(json.dumps(candidateDict))


@login_required(login_url='/vote/login')
def castVote(request):
    voterUID = str(request.user)
    voteTS = str(time.strftime("%Y-%m-%d %H:%M:%S%z"))

    # get a list of people who've voted
    uids = list()
    for uid in Vote.objects.all():
        uids.append(uid.uid)

    # convert the voterUID to something a bit more anonymous
    voterUID = hashlib.md5(voterUID.encode('utf-8')).hexdigest()

    if voterUID in uids:
        # double vote detected, alert the user
        logger.warning("{} attempted double vote.".format(voterUID))
        return HttpResponse(status=423)
    else:
        # normal single vote
        try:
            logger.info("{} is trying to case vote for {} at {}".format(voterUID, request.POST.get('vote', ''), voteTS))
            voteMarks = request.POST.get('vote', '')
            candidates = Candidate.objects.all()
            candidateIDs = list()
            for candidate in candidates:
                candidateIDs.append(candidate.pk)

            for mark in voteMarks:
                if int(mark) not in candidateIDs:
                    logger.warning("{} tried to vote for nonexistant candidate!".format(str(request.user)))
                    return HttpResponse(status=418)
            v = Vote(uid=voterUID, order=request.POST.get('vote', ''), timestamp = voteTS)
            v.save()
            return HttpResponse(status=200)
        except Exception as e:
            logger.error("Error: {}".format(e))
            return HttpResponse(status=500)


@login_required(login_url='/vote/login')
def add(request):
    proposedCandidate = request.POST.get('name', '')
    candidates = Candidate.objects.all()
    candidateDict = dict()
    for candidate in candidates:
        candidateDict[candidate.id] = candidate.name.lower()

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


@login_required(login_url='/vote/login')
def results(request):
    ballots = list()
    for ballot in Vote.objects.all():
        marks = list()
        for mark in ballot.order.split(','):
            marks.append(int(mark))
        ballots.append(marks)

    box = dict()
    box = vote_summation.Vote(ballots)
    box.computeWinners()
    winnersDict = dict()
    winners = box.getWinners()

    for w in winners:
        try:
            name = Candidate.objects.get(pk=w).name
            numvotes = winners[w]
            winnersDict[name] = numvotes
        except ObjectDoesNotExist as e:
            logging.warning("Discarding null vote for candidate: %d", w)
    template = loader.get_template('vote/results.html')
    return HttpResponse(template.render({'winnersDict': winnersDict, 'organization': config.organization}, request))
