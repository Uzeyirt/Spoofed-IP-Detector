import threading;
import subprocess;
from threading import Thread;

Accepted_for_TCP = ['ESTABLISHED', 'FIN_WAIT', 'CLOSE_WAIT', 'LAST_ACK', 'TIME_WAIT', 'CLOSE']


class ConnTrackModule():

    def __init__(self, T_Database, Probing_System):



        self.sentList = []

        self.ProbingSystem = Probing_System;

        self.PacketsToConnectionCheck = []

        self.running = True;

    def run_func(self):


        if not self.PacketsToConnectionCheck == []:
            #print('contracklist : ' + str(len(self.PacketsToConnectionCheck)))
            packt = self.PacketsToConnectionCheck[0];

            self.PacketsToConnectionCheck.remove(packt);


            if self.IsPacketNewlySent(packt) == False:
                if len(self.sentList) == 5 :
                    self.sentList.remove(self.sentList[0])
                    self.sentList.append(packt)
                else :
                    self.sentList.append((packt))

                if not self.IsConnectionEstablished(packt):
                    self.sendToProbingSystem(packt)
                    self.ProbingSystem.run_func()



                    ####print('- - - - - - - - - - > SENT TO PROBING! --- source and dest : ' + packt.srcIP + ' ' + packt.dstIP)
    def IsPacketNewlySent(self,pck):
        for pac in self.sentList :
            if pck.srcIP == pac.srcIP:
                return True;
        return False;

    def ISContains(self, packett):
        for packetentry in self.PacketsToConnectionCheck:
            if packetentry.Protocol == 'ICMP':
                if packett.Protocol == 'ICMP':
                    if ((packett.srcIP == packetentry.srcIP) & (packett.dstIP == packetentry.dstIP)):
                        return True;
                else:
                    continue
            else:
                if packett.Protocol == 'ICMP':
                    continue
                else:
                    if ((packett.srcIP == packetentry.srcIP) & (packett.dstIP == packetentry.dstIP) & (
                            packett.sourcePort == packetentry.sourcePort) & (
                            packett.destinationPort == packetentry.destinationPort)):
                        return True;

        return False;

    def sendToProbingSystem(self, packt):
        self.ProbingSystem.PacketListToProbe.append(packt)

    def IsConnectionEstablished(self, packet):

        if packet.Protocol == 'TCP':

            IPv4_ProtocoL = 'tcp'
            src = packet.srcIP
            dst = packet.dstIP
            sport = packet.sourcePort
            dport = packet.destinationPort

            command = "sudo conntrack -L --proto " + IPv4_ProtocoL + " --src " + src + " --dst " + dst + " --sport " + sport + " --dport " + dport
            pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout;
            output = pipe.readlines();

            src = packet.dstIP
            dst = packet.srcIP
            sport = packet.destinationPort
            dport = packet.sourcePort
            command = "sudo conntrack -L --proto " + IPv4_ProtocoL + " --src " + src + " --dst " + dst + " --sport " + sport + " --dport " + dport
            pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout;

            reverse_output = pipe.readlines();

            output = output + reverse_output

            for one_line_from_output in output:
                words = str(one_line_from_output).split(' ');
                print(len(words))
                if words[8] in Accepted_for_TCP:
                    # print('---> TCP connection found! --- source and dest : ' + dst + ' ' + src)
                    return True;
            ####print('---> TCP connection COULD NOT BE found! --- source and dest : ' + dst + ' ' + src)
            return False;
        if packet.Protocol == 'UDP':
            IPv4_ProtocoL = 'udp'
            src = packet.dstIP
            dst = packet.srcIP
            sport = packet.destinationPort
            dport = packet.sourcePort
            command = "sudo conntrack -L --proto " + IPv4_ProtocoL + " --src " + src + " --dst " + dst + " --sport " + sport + " --dport " + dport
            pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout;
            output = pipe.readlines();

            for one_line_from_output in output:
                words = str(one_line_from_output).split(' ');
                print(len(words))
                if not words[12] == '[UNREPLIED]':
                    # print('---> UDP connection found! --- source and dest : ' + dst + ' ' + src)
                    return True;
            ####print('---> UDP connection COULD NOT BE found! --- source and dest : ' + dst + ' ' + src)
            return False;
        if packet.Protocol == 'ICMP':
            IPv4_ProtocoL = 'icmp'
            src = packet.dstIP
            dst = packet.srcIP

            command = "sudo conntrack -L --proto " + IPv4_ProtocoL + " --src " + src + " --dst " + dst
            pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout;
            output = pipe.readlines();

            for one_line_from_output in output:
                words = str(one_line_from_output).split(' ');
                if not words[12] == '[UNREPLIED]':
                    # print ('---> ICMP connection found! --- source and dest : ' + dst + ' ' + src)
                    return True;
            ####print('---> ICMP connection COULD NOT BE found! --- source and dest : ' + dst + ' ' + src)
            return False;

