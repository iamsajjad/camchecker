
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
    
    cams = Quickping(sRange, eRange, log=True, threads=512)
    cams.active()
    
    ignore = ignore.split(' ')
    
    cams.activeAddresses = [ip for ip in cams.activeAddresses if ip not in ignore]
    cams.deactiveAddresses = [ip for ip in cams.deactiveAddresses if ip not in ignore]
    
    response = {
            "start": cams.start,
            "end": cams.end,
            "active": cams.activeAddresses,
            "deactive": cams.deactiveAddresses,
    }
    return render(request, 'homepage.html', response)

