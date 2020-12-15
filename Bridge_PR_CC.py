from PInfoDeclaration import *;
from threading import Thread;

class BridgePRCC ():
    def __init__(self,CC,DB):



        self.PacketPool = [] ;

        self.connectionControl = CC;

        self.PacketsToConnectionCheck = []

        self.running = True;

        self.Sent_DataBase = DB ;



    def run_func(self):
        #print('bridge  population : ' + str(len(self.PacketsToConnectionCheck)))
        self.Sent_DataBase.DeleteForTimeout()
        for packt in self.PacketsToConnectionCheck :
            if self.Sent_DataBase.isContains(packt) == False :
                self.Sent_DataBase.CreateNewEntry(packt);
                self.PacketsToConnectionCheck.remove(packt)
                if not self.connectionControl.ISContains(packt):
                    self.SendToConnectionControl(packt)
                    self.connectionControl.run_func()
                    #print('SENT !! -- ' + packt.srcIP)
                    #self.tx_file.write('SENT ---> ' + packt.srcIP + ' ' + packt.dstIP + '\n')  # testing purposes
                #else :
                    #print('no again !! -- ' + packt.srcIP)
            else :
                self.PacketsToConnectionCheck.remove(packt)
                self.Sent_DataBase.RefreshTimeout(packt)
                #print('packet already sent!!!!!!')
    def SendToConnectionControl(self,packet):

        self.connectionControl.PacketsToConnectionCheck.append(packet);
    def stop(self):
        self.running = False ;


