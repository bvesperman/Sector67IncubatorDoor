import requests
import json
import datetime
import RFIDDataAccess
import SectorAdminSite
import sys
import time 
import datetime 
import RPi.GPIO as io 
import select
from time import gmtime, strftime
import subprocess
import os
import MachineLogic
import logging


logging.basicConfig(filename='/home/pi/'+ time.strftime("%Y%m%d") + ".txt",level=logging.ERROR,)

localRFID = ""
rebootTime = time.time() + 86400

machine = MachineLogic.MachineLogic()
machine.Setup()

access = RFIDDataAccess.DataAccess()
authService = SectorAdminSite.SectorAdmin()

try:

   #Delete Current Cache of Authorized users
   access.DeleteAllAuthorizedUsers()

   #Pull down the current list of authorized users
   data = authService.GetAuthorizedUsers(machine.machineID)

   #authService.UpdateMachine(machineID)

   #add the users to the cache
   #for user in data:
   #   access.InsertAuthorizedUser(user['RFID'],user['ID'],user['FirstName'] + ' ' +user['LastName'])  

   for user in data["message"]:
     #print (user["rfid"])
     access.InsertAuthorizedUser(user["rfid"],0,user["display_name"])

except:
   logging.exception('rebooting')
   print('exception')
   rebootTime = time.time() + 60

  
try:

    #loop forever
    while True:

        # read the standard input to see if the RFID has been swiped
        while sys.stdin in select.select([sys.stdin],[],[],0)[0]:
            localRFID = sys.stdin.readline()
            if localRFID:
                localRFID = ''.join(localRFID.splitlines())

                #RFID has been swiped now check if authorized
	        print(int(localRFID))
	        machine.rfid = int(localRFID)
                if access.IsRFIDAuthorized(int(machine.rfid)):
                    machine.DoAuthorizedWork()

        machine.DoUnAuthorizedContinuousWork()
        #machine.CheckBeam()


        time.sleep(.1)

        #if  time.time() > rebootTime and not machine.Busy():
        #    print("rebooting")
        #    os.system("reboot")

except:
    logging.exception('Main loop died')
    raise