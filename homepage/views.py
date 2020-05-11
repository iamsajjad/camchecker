
"""
created by Sajjad @ https://github.com/iamsajjad
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render
from datetime import datetime
from quickping import Quickping

def homepage(request):
    return render(request, 'homepage.html')

def runCheck(request):

    sRange = request.POST['srange']
    eRange = request.POST['erange']
    ignore = request.POST['ignore']
    
    ignore = ignore.split(' ')
    cams = Quickping(sRange, eRange, ignore=ignore, threads=256, log=True)
    cams.active()

    response = {
            "start": cams.start,
            "end": cams.end,
            "active": cams.activeAddresses,
            "deactive": cams.deactiveAddresses,
    }

    return render(request, 'homepage.html', response)

