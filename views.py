from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

import json

from .models import Candidate, Vote

def index(request):
    return HttpResponse("Hello World!")

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
