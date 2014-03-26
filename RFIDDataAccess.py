#!/usr/bin/python

import sqlite3

class DataAccess:

    connectionString = "/home/pi/RFID.db"




    def DeleteAllAuthorizedUsers( self):

        conn = sqlite3.connect(DataAccess.connectionString)
        conn.execute("Delete From AuthorizedUsers")
        conn.commit()
        conn.close()

        return


    def InsertAuthorizedUser( self, rfid, uid, username):

        conn = sqlite3.connect(DataAccess.connectionString)
        command = "Insert Into AuthorizedUsers (RFID, uid, name) values ('{0}',{1},'{2}');".format(rfid,uid,username)
        conn.execute(command)
        conn.commit()
        conn.close()

        return
    
    def IsRFIDAuthorized(self, rfid):
        allowed = False
        conn = sqlite3.connect(DataAccess.connectionString)
        command = "Select * From AuthorizedUsers Where RFID = '{0}'".format(rfid)
        
        for row in conn.execute(command):    
            allowed = True

        conn.close()

        return allowed        



    
    def InsertLaserLog(self, LogTime, Duration, User, MaterialID, Billing, PicturePath):
        conn = sqlite3.connect(DataAccess.connectionString)
        command = "Insert into LaserLog (Logtime, Duration, User, MaterialID, Billing, PicturePath) Values ('{0}', {1}, '{2}', {3}, '{4}', '{5}')".format(LogTime, Duration, User, MaterialID, Billing, PicturePath)
        conn.execute(command)
        conn.commit()
        conn.close()

        return        

