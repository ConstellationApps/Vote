from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import RequestContext, loader

import json
import logging

logger = logging.getLogger(__name__)

from .models import Candidate, Vote

def index(request):
    candidate_list = Candidate.objects.all()
    template = loader.get_template('vote/index.html')
    context = RequestContext(request, {
        'candidate_list': candidate_list,
    })
    return HttpResponse(template.render(context))

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
    logger.info(request.POST)
    return HttpResponse("Success")
