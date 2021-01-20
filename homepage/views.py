
'''
created by Sajjad @ https://github.com/iamsajjad
'''

import time

from django.shortcuts import render
from django.http import HttpResponseRedirect
from quickping import Quickping
from .models import Devices

def homepage(request):
    return render(request, 'homepage.html')

def saveDevice(request):

    if request.method == "POST":

        name = request.POST['name']
        ipaddress = request.POST['ipaddress']

        try:
            update = Devices.objects.get(ipaddress=ipaddress)
            update.name = name
            update.save()
        except:
            addDev = Devices.objects.create(name=name, ipaddress=ipaddress)
            addDev.save()

        return HttpResponseRedirect('/saveDevice')


    response = {
            "start" : True,
            "devices": Devices.objects.all()
    }

    return render(request, 'saveDevice.html', response)

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

    savedDevices = Devices.objects.all()

    response = {
        'start': cams.start,
        'end': cams.end,
        'ignore': cams.ignore,
        'timeToDone': timeToDone,
        'addresses': len(cams.addresses),
        'active': cams.activeAddresses,
        'saved': savedDevices,
        'deactive': cams.deactiveAddresses,
    }

    return render(request, 'homepage.html', response)
