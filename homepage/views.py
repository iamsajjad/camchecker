
'''
created by Sajjad @ https://github.com/iamsajjad
'''

import time

from django.shortcuts import render
from quickping import Quickping


def homepage(request):
    return render(request, 'homepage.html')


def runCheck(request):

    sRange = request.POST['srange']
    eRange = request.POST['erange']
    ignore = request.POST['ignore']
    threads = int(request.POST['threads'])

    # remove repeated addresses
    ignore = list(filter(None, ignore.replace('\r', '').split('\n')))
    cleanAddresses = dict.fromkeys(ignore, 0)

    ignore = []
    for address in cleanAddresses.keys():
        ignore.append(address.strip())

    try:
        stimer = time.time()
        cams = Quickping(sRange, eRange, ignore=ignore, threads=threads, log=True)
        cams.active()
        etimer = time.time()
    except Exception as e:
        raise e

    if len(cams.ignore) == 0:
        cams.ignore = ['No Ignored Addresses']

    # time take to process
    timeToDone = time.strftime('%H:%M:%S', time.gmtime(etimer - stimer))

    response = {
        'start': cams.start,
        'end': cams.end,
        'ignore': cams.ignore,
        'timeToDone': timeToDone,
        'addresses': len(cams.addresses),
        'active': cams.activeAddresses,
        'deactive': cams.deactiveAddresses,
    }

    return render(request, 'homepage.html', response)
