from scapy.all import * ;
from PInfoDeclaration import * ;
import datetime;
from Trusted_DB import *
Expected_dest_Port = [42234,42236,42237,42238,42239,42240,42241]
Expected_src_Port = [80,25,143,110,3389,21,443]
class Packet_Catcher(Thread) :
    def __init__(self,ip_address_assigned,Int_Name,queue_to_PR):

        Thread.__init__(self);


        self.running = True;
        self.Last_TCP = []
        self.Ip = ip_address_assigned ;
        self.Last_UDP = []
        self.Interface_Name = Int_Name ;

        self.to_PR =  queue_to_PR

        open(str(self.Interface_Name) + 'ICMP', "w+")




    def AddToStorage(self,PInfo) :

        self.PacketStorage.append(PInfo);

    def packet_callback(self,packet):

        if '(IPv4)' in packet.layers()[0].mysummary(packet) :

            if (packet[IP].dst == self.Ip):
                if packet.haslayer(TCP) :
                    packet_info = NonICMPPacketInfo(packet[IP].src, packet[IP].dst, str(packet[IP].ttl),str(packet[IP].id), "TCP", str(packet[TCP].sport),str(packet[TCP].dport));
                    if self.isSameTCP(packet_info) == False :

                        #print('not same tcp!!!     ' + packet_info.srcIP)
                        if len(self.Last_TCP) == 20:
                            self.Last_TCP.remove(self.Last_TCP[0])
                            self.Last_TCP.append(packet_info)
                        else:
                            self.Last_TCP.append(packet_info)
                        self.to_PR.put(packet_info)
                            #print('source IP: ' + packet[IP].src + ' dest IP: ' + packet[IP].dst + ' TTL: ' + str(packet[IP].ttl) + ' IP ID: ' + str(packet[IP].id) + ' src port: ' + str(packet[TCP].sport) + ' dst port: ' +str(packet[TCP].dport));
                        #else :
                            #print('same tcp  ;;;;;;;;;;;;;;;;    ' +  packet_info.srcIP)

                elif packet.haslayer(UDP) :

                    packet_info = NonICMPPacketInfo(packet[IP].src, packet[IP].dst, str(packet[IP].ttl),str(packet[IP].id), "UDP", str(packet[UDP].sport),str(packet[UDP].dport) ) ;
                    if self.isSameUDP(packet_info) == False:

                        #print('not same udp!!!   ' + packet_info.srcIP)
                        if len(self.Last_UDP) == 10:
                            self.Last_UDP.remove(self.Last_UDP[0])
                            self.Last_UDP.append(packet_info)
                        else :
                            self.Last_UDP.append(packet_info)
                        self.to_PR.put(packet_info)

                        #print('source IP: ' + packet[IP].src + ' dest IP: ' + packet[IP].dst + ' TTL: ' + str(packet[IP].ttl) + ' IP ID: ' + str(packet[IP].id) + ' src port: ' + str(packet[UDP].sport) + ' dst port: ' + str(packet[UDP].dport));
                    #else :
                        #print ('same udp   ' + packet_info.srcIP )
                elif packet.haslayer(ICMP):
                    packet_info = ICMPPacketInfo(packet[IP].src,packet[IP].dst,str(packet[IP].ttl),str(packet[IP].id),"ICMP",str(packet[ICMP].type),str(packet[ICMP].code) ) ;
                    self.to_PR.put(packet_info)
                    tmp = open(str(self.Interface_Name) + 'ICMP', "a")
                    #print('\nsource IP: ' + packet_info.srcIP + ' dest IP: ' +  packet_info.dstIP + ' TTL: ' + str(packet_info.ttl) + ' IP ID: ' + str(packet_info.ipID)  + ' type: ' + str(packet_info.type) + ' code: ' + str(packet_info.code) + '\n' );
                    tmp.close()
    def _TheSniff(self,e):

        print( 'port sniffer added for port : ' + str(self.Interface_Name));
        sniff(iface = self.Interface_Name,prn = self.packet_callback,stop_filter = lambda p: e.is_set());

    def stop(self):

        self.running = False;

    def isSameUDP(self,pack):
        for udppac in self.Last_UDP:
            if (udppac.srcIP == pack.srcIP) & (udppac.dstIP == pack.dstIP) & (udppac.sourcePort == pack.sourcePort) & (
                    udppac.destinationPort == pack.destinationPort):
                return True
        return False;



    def isSameTCP(self,pack):
        if int(pack.destinationPort) in Expected_dest_Port:
            return False;
        else :
            for tcppac in self.Last_TCP:
                if (tcppac.srcIP == pack.srcIP) & (tcppac.dstIP == pack.dstIP) & (tcppac.sourcePort == pack.sourcePort) & (tcppac.destinationPort == pack.destinationPort) :
                    return True


        return False
