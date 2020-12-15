import threading;
import time

from threading import Thread;


class Trusted_DB() :
    def __init__ (self,StaticDBTimeout):

        self.DBEntryList = [] ;

        self.DBTimeout = int(StaticDBTimeout)

        self.running = True;

    def CreateNewEntry(self, packet ):
        new_entry = DB_Entry(packet, self.DBTimeout)
        self.DBEntryList.append(new_entry)
        '''
        if (new_entry.Packet_info.Protocol == "ICMP"):

            print(
                 str(new_entry.creation_time.tm_hour) + ":" + str(new_entry.creation_time.tm_min) + ":" + str(new_entry.creation_time.tm_sec)  + " - "+'ADDED !!! --- source IP: ' + new_entry.Packet_info.srcIP + ' dest IP: ' + new_entry.Packet_info.dstIP + ' TTL: ' + str(
                    new_entry.Packet_info.ttl) + ' IP ID: ' + str(new_entry.Packet_info.ipID) + ' type: ' + str(
                    new_entry.Packet_info.type) + ' code: ' + str(new_entry.Packet_info.code));

        else:

            print(
                str(new_entry.creation_time.tm_hour) + ":" + str(new_entry.creation_time.tm_min) + ":" + str(new_entry.creation_time.tm_sec)  + " - "+'ADDED !!! --- source IP: ' + new_entry.Packet_info.srcIP + ' dest IP: ' + new_entry.Packet_info.dstIP + ' TTL: ' + str(
                    new_entry.Packet_info.ttl) + ' IP ID: ' + str(new_entry.Packet_info.ipID) + ' Source P: ' + str(
                    new_entry.Packet_info.sourcePort) + ' Destination P: ' + str(new_entry.Packet_info.destinationPort));
        '''
    def returnPackt(self, packet):
        for pck_entry in self.DBEntryList:
            if ((str(pck_entry.Packet_info.srcIP) == packet.srcIP) & (str(pck_entry.Packet_info.dstIP) == packet.dstIP)) :
                return pck_entry

            else:
                continue
    def isContains(self, packet):
        if self.DBEntryList == [] :
            return False ;
        else :
            for pck_entry in self.DBEntryList:
                if ((str(pck_entry.Packet_info.srcIP) == packet.srcIP) & (str(pck_entry.Packet_info.dstIP) == packet.dstIP)) :
                    return True

                else:
                    continue
            return False
    def RefreshTimeout(self, packet):
        for pck_entry in self.DBEntryList:
            if ((str(pck_entry.Packet_info.srcIP) == packet.srcIP) & (str(pck_entry.Packet_info.dstIP) == packet.dstIP)) :
                pck_entry.creation_time = time.localtime(time.time()) ;
                pck_entry.Packet_info.ttl = packet.ttl
                break
            else :
                continue

    def DeleteForTimeout(self):
        if not self.DBEntryList == [] :
            for pck_entry in self.DBEntryList:
                currentTime = time.localtime(time.time()) ;


                if (pck_entry.isTimeout(currentTime) == True) :
                    '''
                    if (pck_entry.Packet_info.Protocol == "ICMP"):

                        print(
                            str(currentTime.tm_hour) + ":" + str(currentTime.tm_min) + ":" + str(currentTime.tm_sec)  + " - "+'DELETED !!! --- source IP: ' + pck_entry.Packet_info.srcIP + ' dest IP: ' + pck_entry.Packet_info.dstIP + ' TTL: ' + str(
                                pck_entry.Packet_info.ttl) + ' IP ID: ' + str(pck_entry.Packet_info.ipID) + ' type: ' + str(
                                pck_entry.Packet_info.type) + ' code: ' + str(pck_entry.Packet_info.code)  + " TIME DISTANCE ::: " + str(pck_entry.TimeDistance(pck_entry.creation_time, currentTime)));

                    else:

                        print(
                             str(currentTime.tm_hour) + ":" + str(currentTime.tm_min) + ":" + str(currentTime.tm_sec)  + " - "+'DELETED !!! --- source IP: ' + pck_entry.Packet_info.srcIP + ' dest IP: ' + pck_entry.Packet_info.dstIP + ' TTL: ' + str(
                                pck_entry.Packet_info.ttl) + ' IP ID: ' + str(pck_entry.Packet_info.ipID) + ' Source P: ' + str(
                                pck_entry.Packet_info.sourcePort) + ' Destination P: ' + str(pck_entry.Packet_info.destinationPort)+ " TIME DISTANCE ::: " + str(pck_entry.TimeDistance(pck_entry.creation_time, currentTime)));
                    '''
                    self.DBEntryList.remove(pck_entry)

                else:
                    continue




class DB_Entry ():
    def __init__(self,packet,timeout_seconds):

        self.Packet_info = packet ;

        self.timeout = timeout_seconds ;

        self.creation_time = time.localtime(time.time()) ;

    def isTimeout(self, Time):
        Tdistance = self.TimeDistance(self.creation_time, Time)

        if int(Tdistance) > int(self.timeout) :

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






