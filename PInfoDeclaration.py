
import time ;

class PacketInfo :

    def __init__(self):

        self.srcIP ;

        self.dstIP ;

        self.ttl ;

        self.ipID ;

        self.Protocol ;




class ICMPPacketInfo(PacketInfo) :       # ICMP

    def __init__(self,SRCIP,DSTIP,TTL,IPID,PROTOCOL,TYPE,CODE):

        self.srcIP = SRCIP ;

        self.dstIP = DSTIP ;

        self.ttl = TTL ;

        self.ipID = IPID ;

        self.Protocol = PROTOCOL ;

        self.type = TYPE ;

        self.code = CODE ;


    def timeStamp(self):
        self.arrive_time = time.localtime(time.time());



class NonICMPPacketInfo(PacketInfo) :   # UDP / TCP

    def __init__(self,SRCIP,DSTIP,TTL,IPID,PROTOCOL,SPORT,DPORT):

        self.srcIP = SRCIP ;

        self.dstIP = DSTIP ;

        self.ttl = TTL ;

        self.ipID = IPID ;

        self.Protocol = PROTOCOL ;

        self.sourcePort = SPORT ;

        self.destinationPort = DPORT ;


    def timeStamp(self):
        self.arrive_time = time.localtime(time.time());