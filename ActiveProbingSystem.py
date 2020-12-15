import threading;
from threading import Thread;
import socket
from ProbeRegManager import *

#probe listesi = 80,113,25,143,110,3389,21,443
Option_1_For_Probe = [42234,80]

Option_3_For_Probe = [42236,25]
Option_4_For_Probe = [42237,143]
Option_5_For_Probe = [42238,110]
Option_6_For_Probe = [42239,3389]
Option_7_For_Probe = [42240,21]
Option_8_For_Probe = [42241,443]
class ActiveProbingSystem() :
    def __init__(self, T_Database,ProbeRegulatorr,from_pcc):



        self.Trusted_DB = T_Database;

        self.PacketListToProbe = []

        self.LANPacketListToProbe = []

        self.ProbeRegg = ProbeRegulatorr

        self.from_pcc = from_pcc

        self.IntList = []

        self.IpList = []

        self.running = True;
    def attachPR(self, PacRouter):

        self.PR = PacRouter



    def run_func(self):

        if not self.from_pcc.empty()  :
            Lsts = self.from_pcc.get()
            self.IpList = Lsts[0];
            self.IntList = Lsts[1];

        if not self.PacketListToProbe == [] :
            #print('probingsystemm : ' + str(len(self.PacketListToProbe)))
            is_contains = self.Add_entry_to_PacketRouter(self.PacketListToProbe[0])
            if is_contains == False :
                new_entry = PResEntry(self.PacketListToProbe[0])
                self.PacketListToProbe[0].timeStamp()
                self.ProbeRegg.ExpectedResponses.append(new_entry);
                self.Send_Probe(self.PacketListToProbe[0],Option_1_For_Probe);
                self.Send_Probe(self.PacketListToProbe[0], Option_3_For_Probe);
                self.Send_Probe(self.PacketListToProbe[0], Option_4_For_Probe);
                self.Send_Probe(self.PacketListToProbe[0], Option_5_For_Probe);
                self.Send_Probe(self.PacketListToProbe[0], Option_6_For_Probe);
                self.Send_Probe(self.PacketListToProbe[0], Option_7_For_Probe);
                self.Send_Probe(self.PacketListToProbe[0],Option_8_For_Probe);


                counter = 0
                try:
                    while not str(self.IpList[counter]) == new_entry.firstPacket.dstIP:
                        counter = counter + 1
                    IntName = str(self.IntList[counter])

                    command = "sudo ping " + new_entry.firstPacket.srcIP + " -c 1 -W 1 -I " + IntName;
                    pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE).stdout;
                    o = pipe.readlines()


                    self.PacketListToProbe.remove(self.PacketListToProbe[0])
                    '''for pack in self.PacketListToProbe :
                        print('Packetlist entrisi : ' + pack.srcIP + " " + pack.dstIP);'''


                except:
                    print('')
            else :
                #print("it is already there!!")
                self.PacketListToProbe.remove(self.PacketListToProbe[0])
    def run_func_LAN(self):
        if not self.from_pcc.empty()  :
            Lsts = self.from_pcc.get()
            self.IpList = Lsts[0];
            self.IntList = Lsts[1];
        if not self.LANPacketListToProbe == [] :

            is_contains = self.Add_LANentry_to_PacketRouter(self.LANPacketListToProbe[0])
            if is_contains == False :
                new_entry = PResEntry(self.LANPacketListToProbe[0])
                self.LANPacketListToProbe[0].timeStamp()
                self.ProbeRegg.ExpectedLANResponses.append(new_entry);
                self.Send_Probe(self.LANPacketListToProbe[0],Option_1_For_Probe);

                self.Send_Probe(self.LANPacketListToProbe[0], Option_3_For_Probe);
                self.Send_Probe(self.LANPacketListToProbe[0], Option_4_For_Probe);
                self.Send_Probe(self.LANPacketListToProbe[0], Option_5_For_Probe);
                self.Send_Probe(self.LANPacketListToProbe[0], Option_6_For_Probe);
                self.Send_Probe(self.LANPacketListToProbe[0], Option_7_For_Probe);
                self.Send_Probe(self.LANPacketListToProbe[0],Option_8_For_Probe);




                #add proper ping probe
                counter = 0
                try:
                    while not str(self.IpList[counter]) == new_entry.firstPacket.dstIP:
                        counter = counter + 1
                    IntName = str(self.IntList[counter])

                    command = "sudo ping " + new_entry.firstPacket.srcIP + " -c 1 -W 1 -I " + IntName;
                    pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE).stdout;
                    o = pipe.readlines()


                    self.LANPacketListToProbe.remove(self.LANPacketListToProbe[0])
                    '''for pack in self.PacketListToProbe :
                        print('Packetlist entrisi : ' + pack.srcIP + " " + pack.dstIP);'''


                except:
                    print('')
                    self.LANPacketListToProbe.remove(self.LANPacketListToProbe[0])


            else :
                #print("it is already there!!")
                self.LANPacketListToProbe.remove(self.LANPacketListToProbe[0])



    def Add_entry_to_PacketRouter(self,Packet):
        if self.PR.isContains(Packet.srcIP,Packet.dstIP) == False :
            new_entry = PREntry(Packet.srcIP,Packet.dstIP)
            self.PR.ExpectedResponseList.append(new_entry)
            '''
            print ('-----PR entriesss------')
            for entry in self.PR.ExpectedResponseList:
                print(entry.SIP + ':' + entry.SPort + ' ' + entry.DIP + ':' + entry.Dport)'''
            return False;
        else :
            return True;
    def Add_LANentry_to_PacketRouter(self,Packet):
        if self.PR.isLANContains(Packet.srcIP,Packet.dstIP) == False :
            new_entry = PREntry(Packet.srcIP,Packet.dstIP)
            self.PR.LANExpectedResponseList.append(new_entry)
            '''
            print ('-----PR entriesss------')
            for entry in self.PR.ExpectedResponseList:
                print(entry.SIP + ':' + entry.SPort + ' ' + entry.DIP + ':' + entry.Dport)'''
            return False;
        else :
            return True;
    def Send_Probe(self,Packet,Option):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.00001);
        shost = Packet.dstIP
        dhost = Packet.srcIP
        sport = Option[0]
        dport = Option[1]

        try:
            s.bind((shost, sport))
            s.connect((dhost, dport))

            s.sendall(b'')

            s.close()

        except Exception as e:
            print(e)
            s.close()
        #self.txx_file.write('PROBE SENT ---> ' + shost + ':' + str(sport) + ' ' + dhost + ':' + str(dport) + '\n') #testing purposes

class PREntry :
    def __init__(self,SourceIP,DestIP):

        self.SIP = SourceIP
        self.DIP = DestIP

