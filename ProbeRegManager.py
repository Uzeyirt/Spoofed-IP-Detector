import threading;
from threading import Thread;
import socket
import subprocess;
import time
from PInfoDeclaration import *
First_Option_For_Probe = [42234,80]
Second_Option_For_Probe = [42235,443]
Third_Option_For_Probe = [42236,21]
Forth_Option_For_Probe = [42237,113]

class ProbeRegManager() :
    def __init__(self,RManager):

        self.ExpectedResponses = []

        self.Responses = []

        self.LANResponses = []

        self.ExpectedLANResponses = []

        self.ResultM = RManager;

        self.running = True

    def attach_PR(self,ThePR):

        self.Attached_PR = ThePR ;
    def attachPcc(self,pcc):

        self.PacCapC = pcc

    def run_func (self):

        if self.Responses != [] :
            for response in self.Responses:
                relatedEntry = self.FindThePeer(response);
                self.Responses.remove(response);
                if relatedEntry is not None :
                    relatedEntry.add_response_packet(response);
        if self.LANResponses != [] :
            for response in self.LANResponses:

                relatedEntry = self.FindTheLANPeer(response);
                self.LANResponses.remove(response);
                if relatedEntry is not None :
                    relatedEntry.add_response_packet(response);

        self.CheckExpected()
        self.CheckExpectedLAN()

    def sendToResultManager(self,ent):
        self.ResultM.Results.append(ent) ;
    def sendToLANResultManager(self,ent):
        self.ResultM.LANResults.append(ent) ;
    def FindThePeer (self,resp) :
        for entry in self.ExpectedResponses :

            if ( (resp.dstIP == entry.firstPacket.dstIP) & (resp.srcIP == entry.firstPacket.srcIP) ) :
                return entry
    def FindTheLANPeer (self,resp) :
        for entry in self.ExpectedLANResponses :

            if ( (resp.dstIP == entry.firstPacket.dstIP) & (resp.srcIP == entry.firstPacket.srcIP) ) :
                return entry

    def stop (self) :

        self.running = False ;

    def CheckExpected(self):

        for ExpResE in self.ExpectedResponses:

            if self.IsTimeout(ExpResE.creation_time) == True :

                self.ExpectedResponses.remove(ExpResE)

                entry_will_be_deleted = self.Attached_PR.getEntry(ExpResE.firstPacket.srcIP,ExpResE.firstPacket.dstIP)

                if entry_will_be_deleted is not None :

                    self.Attached_PR.ExpectedResponseList.remove(entry_will_be_deleted);

                else :
                    print('this is none');
                self.sendToResultManager(ExpResE);
                self.ResultM.run_func()
    def CheckExpectedLAN(self):

        for ExpResE in self.ExpectedLANResponses:

            if self.IsTimeout(ExpResE.creation_time) == True :

                self.ExpectedLANResponses.remove(ExpResE)

                entry_will_be_deleted = self.Attached_PR.getLANEntry(ExpResE.firstPacket.srcIP,ExpResE.firstPacket.dstIP)

                if entry_will_be_deleted is not None :

                    self.Attached_PR.LANExpectedResponseList.remove(entry_will_be_deleted);

                else :
                    print('this is none');
                self.sendToLANResultManager(ExpResE);
                self.ResultM.run_func()

    def IsTimeout(self, Time):

        timee = time.localtime(time.time())

        Tdistance = self.TimeDistance(Time, timee)

        if int(Tdistance) > int(20) : #because delay may be high

            return True

        else :

            return False

    def TimeDistance(self, Creation_Time, Time) :

        Distance = (Time.tm_hour - Creation_Time.tm_hour)*3600 + (Time.tm_min - Creation_Time.tm_min)*60 + (Time.tm_sec - Creation_Time.tm_sec)

        Day_Distance = Time.tm_mday - Creation_Time.tm_mday

        if Day_Distance == 0 :

            return Distance

        else :

            return ( 24*3600 + Distance )

class PResEntry :
    def __init__(self,packet):

        self.firstPacket = packet ;

        self.creation_time = time.localtime(time.time()) ;

        self.ResponsePackets = [] ;

    def add_response_packet(self,pack):

        self.ResponsePackets.append(pack) ;
