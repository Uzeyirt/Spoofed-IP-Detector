from PInfoDeclaration import *;
from threading import Thread;
from NetIfaceChecker import *
import subprocess;
Expected_dest_Port = [42234,42236,42237,42238,42239,42240,42241]
Expected_src_Port = [80,25,143,110,3389,21,443]
class PacKetRouter ():
    def __init__(self,CC,DB,PS,FPS,pck_queue,int_queue):

        self.Sent_DataBase = DB;

        self.PacketPool_from_PCs = pck_queue;

        self.Info_from_IPF = int_queue

        self.connectionControl = CC;

        self.probingSys = PS;

        self.FirstProbingSys = FPS

        self.ExpectedResponseList = []

        self.LANExpectedResponseList = []

        self.running = True;

        self.important_task = True;

        self.NetworkM_List = []

        self.IPA_List = []

        self.AddressRangeListt = []
    def run_func(self) :
        if not self.Info_from_IPF.empty() :
            Infoo = self.Info_from_IPF.get()
            self.IPA_List = Infoo[0]
            self.NetworkM_List = Infoo[1]
            self.AddressRangeListt = Infoo[2]
            print(Infoo)

        print('PR population : ' + str((self.PacketPool_from_PCs).qsize()))
        print("liste pop :     " + str( len(self.ExpectedResponseList)))
        print("liste(LAN) pop :     " + str(len(self.LANExpectedResponseList)))
        packt = self.PacketPool_from_PCs.get() ;
        if int((self.PacketPool_from_PCs).qsize()) > 200 :
            while not self.PacketPool_from_PCs.empty() :
                temp = self.PacketPool_from_PCs.get()
                if (self.is_LAN(packt) == False):

                    if self.IsResponse(packt):
                        packt.timeStamp()
                        self.SendTheResponse(packt);
                else:

                    if self.IsLANResponse(packt):
                        packt.timeStamp()
                        self.SendTheLANResponse(packt);
            #print(str(self.AddressRangeListt[0].Min_Address) + '    ' + str(self.AddressRangeListt[0].Max_Address))
        #self.Sent_DataBase.DeleteForTimeout()
        if (self.is_LAN(packt) == False) :

            if self.IsResponse(packt):
                packt.timeStamp()
                self.SendTheResponse(packt) ;


            else :

                self.SendToConnectionControl(packt) ;

                self.connectionControl.run_func()

        else :

            if self.IsLANResponse(packt):
                packt.timeStamp()
                self.SendTheLANResponse(packt);
            else :

                self.FirstProbingSys.LANPacketListToProbe.append(packt)

                self.FirstProbingSys.run_func_LAN()



        self.probingSys.run_func();

    def is_LAN(self,packet) :
        if not self.IPA_List == [] :
            counter = 0 ;

            try :
                while (len(self.IPA_List) >= counter + 1)  &  (packet.dstIP != self.IPA_List[counter]) :
                    counter = counter + 1 ;
                if ((len(self.IPA_List) < counter + 1)) :
                    return False;
                if self.is_in_Range(packet.srcIP,self.AddressRangeListt[counter]) ==True:
                    #print('It Is in LAN!!!!  ----->  ' + packet.srcIP)
                    return True

                else :
                    #print('It Is NOT in LAN!!!!  ----->  ' + packet.srcIP)
                    return False
            except :
                return False
    def is_in_Range (self,IP,AddresList) :
        IP_octets = IP.split('.')
        Min_octets = AddresList.Min_Address.split('.')
        Max_octets = AddresList.Max_Address.split('.')
        counter = 0
        if (IP_octets != []) & (Max_octets != []) & (Min_octets != []) :
            while counter < 4 :
                if (int(IP_octets[counter]) == int(Max_octets[counter])) & (int(IP_octets[counter]) == int(Min_octets[counter])):
                    counter = counter + 1
                    continue
                elif  (int(IP_octets[counter]) <= int(Max_octets[counter])) & (int(IP_octets[counter]) >= int(Min_octets[counter])) :
                    counter = counter + 1
                    continue
                else :
                    return False ;

            return True ;
        else :
            print('sikinti buyuk !!!!!!!')
    def SendTheResponse(self,packet) :

        self.probingSys.Responses.append(packet);
    def SendTheLANResponse(self,packet) :

        self.probingSys.LANResponses.append(packet);

    def SendToConnectionControl(self,packet):

        self.connectionControl.PacketsToConnectionCheck.append(packet);

    def isContains(self,sIP,dIP):
        for expected in self.ExpectedResponseList :
            if ((expected.SIP == sIP) & (expected.DIP == dIP)) :
                return True;
        return False;
    def isLANContains(self,sIP,dIP):
        for expected in self.LANExpectedResponseList :
            if ((expected.SIP == sIP) & (expected.DIP == dIP)) :
                return True;
        return False;
    def getEntry (self,sIP,dIP) :
        for expected in self.ExpectedResponseList :
            if ((expected.SIP == sIP)  & (expected.DIP == dIP) ) :
                return expected;
    def getLANEntry (self,sIP,dIP) :
        for expected in self.LANExpectedResponseList :
            if ((expected.SIP == sIP)  & (expected.DIP == dIP) ) :
                return expected;

    def IsResponse(self,packet):
        if not packet.Protocol == 'ICMP' :

            for expected in self.ExpectedResponseList :

                if self.areTheySame(expected,packet)== True:

                    return True;
        else :
            for expected in self.ExpectedResponseList :
                if self.areTheySameICMP(expected,packet)== True :
                    return True;
        return False;
    def IsLANResponse(self,packet):
        if not packet.Protocol == 'ICMP' :

            for expected in self.LANExpectedResponseList :

                if self.areTheySame(expected,packet) == True:

                    return True;
        else :
            for expected in self.LANExpectedResponseList :
                if self.areTheySameICMP(expected,packet) == True :
                    return True;
        return False;
    def areTheySame(self,pck1,pck2):
        if ((pck1.SIP == pck2.srcIP)  & (pck1.DIP == pck2.dstIP)) :
            for counter in range(7) :
                if (pck2.sourcePort == str(Expected_src_Port[counter])) & (pck2.destinationPort == str(Expected_dest_Port[counter])) :
                    return True;
        return False
    def areTheySameICMP(self, pck1, pck2):

        if ((pck1.SIP == pck2.srcIP) & (pck1.DIP == pck2.dstIP)  ):#gelistirilmeli

            return True;

        return False;
    '''
    def areTheySameForICMP(self,pck1,pck2):
        if ((pck1.SIP == pck2.srcIP) & (pck1.DIP == pck2.dstIP)):
            return True;
        return False;
    '''
    def stop(self) :

        self.running = False ;

