

import sys
import requests
from packaging.version import parse as parseVersion



def check4updates(url,thisver=None):
    if thisver == None:
        #sys.stderr.write("No local version.\n")
        pass
    try:
        r = requests.get(url)
    except:
        #sys.stderr.write("Unable to check for updates.\n")
        #sys.stderr.write("Check https://pypi.org/project/PyTangtv for updates.\n\n")
        return
    if not r.ok:
        #sys.stderr.write("Unable to check for updates: "+str(r.reason)+"\n")
        #sys.stderr.write("Check https://pypi.org/project/PyTangtv for updates.\n\n")
        return
       
    data = r.json()
    l = list(data['releases'].keys())
    l.sort(key=parseVersion)
    latest = l[-1]
    if thisver != None and latest == thisver:
        #sys.stderr.write("Running version "+str(thisver)+" is the latest.\n\n")
        pass
    elif thisver != None and thisver in data['releases'] and latest != thisver:
        sys.stderr.write("Running version "+str(thisver)+" can be upgraded to "+str(latest)+".\n")
        sys.stderr.write("Upgrade with \"pip install pytangtv --upgrade\" or\n")
        sys.stderr.write("check https://pypi.org/project/PyTangtv for updates.\n\n")
    elif thisver != None and thisver not in data['releases']:
        #sys.stderr.write("Unknown local version: "+str(thisver)+"\n")
        #sys.stderr.write("Version "+str(latest)+" is latest available\n\n")
        pass
    else:
        #sys.stderr.write("Version "+str(latest)+" is latest available\n\n")
        pass

def updatemsgs(url,thisver=None):
    msg = "\n";
    if thisver == None:
        msg = msg + "No local version.\n"
        pass
    try:
        r = requests.get(url)
    except:
        msg = msg + "Unable to check for updates.\n"
        msg = msg + "Check https://pypi.org/project/PyTangtv for updates.\n\n"
        return msg
    if not r.ok:
        msg = msg + "Unable to check for updates: "+str(r.reason)+"\n"
        msg = msg + "Check https://pypi.org/project/PyTangtv for updates.\n\n"
        return msg
       
    data = r.json()
    l = list(data['releases'].keys())
    l.sort(key=parseVersion)
    latest = l[-1]
    if thisver != None and latest == thisver:
        msg = msg + "Running version "+str(thisver)+" is the latest.\n\n"
        pass
    elif thisver != None and thisver in data['releases'] and latest != thisver:
        msg = msg + "Running version "+str(thisver)+" can be upgraded to "+str(latest)+".\n"
        msg = msg + "Upgrade with \"pip install pytangtv --upgrade\" or\n"
        msg = msg + "check https://pypi.org/project/PyTangtv for updates.\n\n"
    elif thisver != None and thisver not in data['releases']:
        msg = msg + "Unknown local version: "+str(thisver)+"\n"
        msg = msg + "Version "+str(latest)+" is latest available\n\n"
        pass
    else:
        msg = msg + "Version "+str(latest)+" is latest available\n\n"
        pass
    return msg
    
    
