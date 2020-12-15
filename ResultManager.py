import threading;
from threading import Thread;


class ResultManager():
    def __init__(self):
        self.Results = []
        self.LANResults = []
        self.running = True;
        self.no_resp = 0
        self.yes_resp = 0
        self.Stass = ProbeStatisticcc()
        self.counter = 0;
        self.Stas = statisticcc();
        self.FinalEvaluationStas =EvaStas()
        self.EvaluationList = []
        open("FinalOutput1.txt", "w+")
         # testing purposes

    def run_func(self):
        if not self.Results == [] :
            for Peer in self.Results :
                new_evaluation = Evaluation_Class(str(Peer.firstPacket.srcIP),str(Peer.firstPacket.dstIP))
                if not Peer.ResponsePackets == [] :

                    self.PrintFinalREsults(Peer,new_evaluation) ;
                    self.yes_resp = self.yes_resp + 1
                    print('yes respppp ' + str(self.yes_resp))
                else :
                    new_evaluation.Status = 'NR'
                    #print('RESULT -----> ' + Peer.firstPacket.srcIP + ' --> NO RESPONSE !!!') ;
                    self.no_resp =self.no_resp + 1

                    self.Results.remove(Peer);
                if (new_evaluation.Status == 'V'):
                    print('REPORT :  ' + new_evaluation.SOURCE_IP + ' ---> ' + new_evaluation.DESTINATION_IP + ' === VALIDATED' );
                    new_evaluation.FinalSentence.append(
                            (
                                        '\nREPORT :  ' + new_evaluation.SOURCE_IP + ' ---> ' + new_evaluation.DESTINATION_IP + ' === VALIDATED'))

                    self.Stas.V_count = self.Stas.V_count + 1
                elif (new_evaluation.Status == 'NR'):
                    print('REPORT :  ' + new_evaluation.SOURCE_IP + ' ---> ' + new_evaluation.DESTINATION_IP + ' === NO RESPONSE' );
                    new_evaluation.FinalSentence.append(
                            (
                                        '\nREPORT :  ' + new_evaluation.SOURCE_IP + ' ---> ' + new_evaluation.DESTINATION_IP + ' === NO RESPONSE'))

                    self.Stas.NR_count = self.Stas.NR_count + 1
                else :
                    print('REPORT :  ' + new_evaluation.SOURCE_IP + ' ---> ' + new_evaluation.DESTINATION_IP + ' === SUSPICIOUS' );
                    new_evaluation.FinalSentence.append((
                                                                        '\nREPORT :  ' + new_evaluation.SOURCE_IP + ' ---> ' + new_evaluation.DESTINATION_IP + ' === SUSPICIOUS'))

                    self.Stas.S_count = self.Stas.S_count + 1
                self.counter = self.counter + 1
                if not new_evaluation.Status == "NR" :
                    if (self.FinalEvaluationStas.isContainss(new_evaluation.SOURCE_IP)):
                        element = self.FinalEvaluationStas.getElement(new_evaluation.SOURCE_IP)
                        if new_evaluation.Status =="V":
                            element.valid_count = element.valid_count + 1
                        elif new_evaluation.Status == "S" :
                            element.sus_count = element.sus_count + 1
                    else :
                        new_element = EvaStasElement(new_evaluation.SOURCE_IP)
                        if new_evaluation.Status =="V":
                            new_element.valid_count = new_element.valid_count + 1
                        elif new_evaluation.Status == "S" :
                            new_element.sus_count = new_element.sus_count + 1
                        self.FinalEvaluationStas.Elements.append(new_element)

                self.FINALPrints(new_evaluation)


        if not self.LANResults == []:
            for Peer in self.LANResults:
                new_evaluation = Evaluation_Class(str(Peer.firstPacket.srcIP), str(Peer.firstPacket.dstIP))
                if not Peer.ResponsePackets == []:

                    self.LANPrintFinalREsults(Peer, new_evaluation);
                    self.yes_resp = self.yes_resp + 1
                else:
                    new_evaluation.Status = 'NR'
                    # print('RESULT -----> ' + Peer.firstPacket.srcIP + ' --> NO RESPONSE !!!') ;
                    self.no_resp = self.no_resp + 1
                    self.LANResults.remove(Peer);
                if (new_evaluation.Status == 'V'):
                    print(
                            'LAN REPORT :  ' + new_evaluation.SOURCE_IP + ' ---> ' + new_evaluation.DESTINATION_IP + ' === VALIDATED');
                    new_evaluation.FinalSentence.append((
                                                                        '\nLAN REPORT :  ' + new_evaluation.SOURCE_IP + ' ---> ' + new_evaluation.DESTINATION_IP + ' === VALIDATED'))

                    self.Stas.V_count = self.Stas.V_count + 1
                elif (new_evaluation.Status == 'NR'):
                    print(
                            'LAN REPORT :  ' + new_evaluation.SOURCE_IP + ' ---> ' + new_evaluation.DESTINATION_IP + ' === NO RESPONSE');
                    new_evaluation.FinalSentence.append((
                                '\nLAN REPORT :  ' + new_evaluation.SOURCE_IP + ' ---> ' + new_evaluation.DESTINATION_IP + ' === NO RESPONSE'))

                    self.Stas.NR_count = self.Stas.NR_count + 1
                else:
                    print(
                            'LAN REPORT :  ' + new_evaluation.SOURCE_IP + ' ---> ' + new_evaluation.DESTINATION_IP + ' === SUSPICIOUS');
                    new_evaluation.FinalSentence.append((
                                '\nLAN REPORT :  ' + new_evaluation.SOURCE_IP + ' ---> ' + new_evaluation.DESTINATION_IP + ' === SUSPICIOUS'))

                    self.Stas.S_count = self.Stas.S_count + 1
                self.counter = self.counter + 1
                self.FINALPrints(new_evaluation)
    def CheckTTLConsistency(self,peer):

        return True

    def FINALPrints(self,result):
        tx_file = open("FinalOutput1.txt", "a")
        tx_file.write('\n')
        tx_file.write('----------------------------------\n')
        tx_file.write(result.SOURCE_IP + '---' + result.DESTINATION_IP)
        for one in result.Evaluations:
            tx_file.write('\n')
            tx_file.write(one)

        tx_file.write('\n')
        tx_file.write(str(result.FinalSentence[0]))
        tx_file.write('----------------------------------')
        tx_file.write('\n')
        tx_file.close()

    def CheckIPIDConsistency(self, peer):

        return True


    def PrintFinalREsults(self, peer,evaluation_sample):
        port_80_incremented = 'F' ;  #for better statistical info
        port_113_incremented = 'F'
        port_25_incremented = 'F'
        port_143_incremented = 'F'
        port_110_incremented = 'F'
        port_3389_incremented = 'F'
        port_21_incremented = 'F'
        port_443_incremented = 'F'
        self.Stass.av_numberOfResponse = ((self.Stass.av_numberOfResponse * (self.yes_resp)) + int(len(peer.ResponsePackets))) / float(self.yes_resp + 1) ;
        print('--------------------------------------------------------')
        for per in peer.ResponsePackets :
            if not per.Protocol == 'ICMP' :
                print('RESULT -----> ' + per.srcIP + ':' + per.sourcePort  +  ' --> TTL difference = ' + str(int(per.ttl) - int(peer.firstPacket.ttl)));
                print('RESULT -----> ' + per.srcIP + ':' + per.sourcePort + ' --> IPID difference = ' + str(int(per.ipID) - int(peer.firstPacket.ipID)));
                timeDistanCE = self.TimeDistance(peer.firstPacket.arrive_time,per.arrive_time)
                print ('time distance : ' + str(timeDistanCE))
                evaluation_sample.Evaluations.append(' --> TTL difference = ' + str(
                    int(per.ttl) - int(peer.firstPacket.ttl)) + '\n' + ' --> IPID difference = ' + str(
                    int(per.ipID) - int(peer.firstPacket.ipID)) + '\n' + 'time distance : ' + str(timeDistanCE) + ' second(s)')

                #self.Stass.av_timeDistance = (self.Stass.av_timeDistance* (self.yes_resp*self.Stass.av_numberOfResponse) + timeDistanCE ) / ((self.yes_resp*self.Stass.av_numberOfResponse) + 1)
                if per.sourcePort == '80' :
                    if ( port_80_incremented == 'F') :
                        self.Stass.port80 = self.Stass.port80 + 1
                        port_80_incremented = 'T'
                elif per.sourcePort == '113':
                    if port_113_incremented == 'F' :
                        port_113_incremented = 'T'
                        self.Stass.port113 = self.Stass.port113 + 1
                elif per.sourcePort == '25' :
                    if port_25_incremented == 'F':
                        port_25_incremented = 'T'
                        self.Stass.port25 = self.Stass.port25 + 1
                elif per.sourcePort == '143' :

                    if port_143_incremented == 'F' :
                        port_143_incremented = 'T'
                        self.Stass.port143 = self.Stass.port143 + 1
                elif per.sourcePort == '110':
                    if  port_110_incremented == 'F' :
                        port_110_incremented = 'T'
                        self.Stass.port110 = self.Stass.port110 + 1
                elif per.sourcePort == '3389' :
                    if port_3389_incremented == 'F' :
                        port_3389_incremented = 'T'
                        self.Stass.port3389 = self.Stass.port3389 + 1
                elif per.sourcePort == '21':
                    if port_21_incremented == 'F' :
                        port_21_incremented = 'T'
                        self.Stass.port21 = self.Stass.port21 + 1
                elif per.sourcePort == '443' :
                    if  port_443_incremented == 'F' :
                        port_443_incremented = 'T'
                        self.Stass.port443 = self.Stass.port443 + 1
            else :
                self.Stass.portICMP = self.Stass.portICMP + 1
                print('(ICMP)RESULT -----> ' + per.srcIP + ' ' + ' --> TTL difference = ' + str(int(per.ttl) - int(peer.firstPacket.ttl)));
                print('(ICMP)RESULT -----> ' + per.srcIP + ' --> IPID difference = ' + str(int(per.ipID) - int(peer.firstPacket.ipID)));
                print('time distance : ' + str(self.TimeDistance(peer.firstPacket.arrive_time, per.arrive_time)))
                evaluation_sample.Evaluations.append(' --> TTL difference(ICMP) = ' + str(
                    int(per.ttl) - int(peer.firstPacket.ttl)) + '\n' + ' --> IPID difference(ICMP) = ' + str(
                    int(per.ipID) - int(peer.firstPacket.ipID)) + '\n' + 'time distance : ' + str(
                    self.TimeDistance(peer.firstPacket.arrive_time, per.arrive_time))  + ' second(s)')

            ttl_difference = abs(int(per.ttl) - int(peer.firstPacket.ttl))
            ipid_difference = int(per.ipID) - int(peer.firstPacket.ipID)
            if (ttl_difference < 3) | ((ipid_difference > 0) & (ipid_difference <1000)) :
                evaluation_sample.Status = 'V';
            if ttl_difference == 0 :
                self.Stas.ttl_0 = self.Stas.ttl_0 + 1
            elif ttl_difference == 1 :
                self.Stas.ttl_1 = self.Stas.ttl_1 + 1
            elif ttl_difference == 2 :
                self.Stas.ttl_2 = self.Stas.ttl_2 + 1
            elif ttl_difference == 3 :
                self.Stas.ttl_3 = self.Stas.ttl_3 + 1
            else :
                self.Stas.ttl_inf = self.Stas.ttl_inf + 1

            if ipid_difference == 0 :
                self.Stas.ipid0 = self.Stas.ipid0 + 1
            elif ipid_difference < 100 :
                self.Stas.ipid100 = self.Stas.ipid100 + 1
            elif ipid_difference < 500 :
                self.Stas.ipid500 = self.Stas.ipid500 + 1
            elif ipid_difference < 1000:
                self.Stas.ipid1000 = self.Stas.ipid1000 + 1
            elif ipid_difference < 2000:
                self.Stas.ipid2000 = self.Stas.ipid2000 + 1
            elif ipid_difference < 3000:
                self.Stas.ipid3000 = self.Stas.ipid3000 + 1
            elif ipid_difference < 5000:
                self.Stas.ipid5000 = self.Stas.ipid5000 + 1
            else :
                self.Stas.ipid_inf = self.Stas.ipid_inf + 1
        print('--------------------------------------------------------')
        if not (evaluation_sample.Status == 'V') :
            evaluation_sample.Status = 'S' ;
        self.Results.remove(peer);

    def LANPrintFinalREsults(self, peer, evaluation_sample):
        port_80_incremented = 'F';  # for better statistical info
        port_113_incremented = 'F'
        port_25_incremented = 'F'
        port_143_incremented = 'F'
        port_110_incremented = 'F'
        port_3389_incremented = 'F'
        port_21_incremented = 'F'
        port_443_incremented = 'F'
        self.Stass.av_numberOfResponse = ((self.Stass.av_numberOfResponse * (self.yes_resp)) + int(
            len(peer.ResponsePackets))) / float(self.yes_resp + 1);
        print('--------------------------------------------------------')
        for per in peer.ResponsePackets:
            if not per.Protocol == 'ICMP':

                print('RESULT -----> ' + per.srcIP + ' ' + per.sourcePort + ' --> IPID difference = ' + str(
                    int(per.ipID) - int(peer.firstPacket.ipID)));
                timeDistanCE = self.TimeDistance(peer.firstPacket.arrive_time, per.arrive_time)
                print('time distance : ' + str(timeDistanCE))
                evaluation_sample.Evaluations.append(' --> TTL difference = ' + str(
                    int(per.ttl) - int(peer.firstPacket.ttl)) + '\n' + ' --> IPID difference = ' + str(
                    int(per.ipID) - int(peer.firstPacket.ipID)) + '\n' + 'time distance : ' + str(timeDistanCE) + ' second(s)')

                # self.Stass.av_timeDistance = (self.Stass.av_timeDistance* (self.yes_resp*self.Stass.av_numberOfResponse) + timeDistanCE ) / ((self.yes_resp*self.Stass.av_numberOfResponse) + 1)
                if per.sourcePort == '80':
                    if (port_80_incremented == 'F'):
                        self.Stass.port80 = self.Stass.port80 + 1
                        port_80_incremented = 'T'
                elif per.sourcePort == '113':
                    if port_113_incremented == 'F':
                        port_113_incremented = 'T'
                        self.Stass.port113 = self.Stass.port113 + 1
                elif per.sourcePort == '25':
                    if port_25_incremented == 'F':
                        port_25_incremented = 'T'
                        self.Stass.port25 = self.Stass.port25 + 1
                elif per.sourcePort == '143':

                    if port_143_incremented == 'F':
                        port_143_incremented = 'T'
                        self.Stass.port143 = self.Stass.port143 + 1
                elif per.sourcePort == '110':
                    if port_110_incremented == 'F':
                        port_110_incremented = 'T'
                        self.Stass.port110 = self.Stass.port110 + 1
                elif per.sourcePort == '3389':
                    if port_3389_incremented == 'F':
                        port_3389_incremented = 'T'
                        self.Stass.port3389 = self.Stass.port3389 + 1
                elif per.sourcePort == '21':
                    if port_21_incremented == 'F':
                        port_21_incremented = 'T'
                        self.Stass.port21 = self.Stass.port21 + 1
                elif per.sourcePort == '443':
                    if port_443_incremented == 'F':
                        port_443_incremented = 'T'
                        self.Stass.port443 = self.Stass.port443 + 1
            else:
                self.Stass.portICMP = self.Stass.portICMP + 1

                print('(ICMP)RESULT -----> ' + per.srcIP + ' --> IPID difference = ' + str(
                    int(per.ipID) - int(peer.firstPacket.ipID)));
                print('time distance : ' + str(self.TimeDistance(peer.firstPacket.arrive_time, per.arrive_time)))
                evaluation_sample.Evaluations.append(' --> IPID difference(ICMP) = ' + str(
                    int(per.ipID) - int(peer.firstPacket.ipID)) + '\n' + 'time distance : ' + str(
                    self.TimeDistance(peer.firstPacket.arrive_time, per.arrive_time)) + ' second(s)')

            ipid_difference = int(per.ipID) - int(peer.firstPacket.ipID)
            if (ipid_difference > 0) & (ipid_difference < 1000): #i dont want any false positive because of delay inside the software
                evaluation_sample.Status = 'V';


            if ipid_difference == 0:
                self.Stas.ipid0 = self.Stas.ipid0 + 1
            elif ipid_difference < 100:
                self.Stas.ipid100 = self.Stas.ipid100 + 1
            elif ipid_difference < 500:
                self.Stas.ipid500 = self.Stas.ipid500 + 1
            elif ipid_difference < 1000:
                self.Stas.ipid1000 = self.Stas.ipid1000 + 1
            elif ipid_difference < 2000:
                self.Stas.ipid2000 = self.Stas.ipid2000 + 1
            elif ipid_difference < 3000:
                self.Stas.ipid3000 = self.Stas.ipid3000 + 1
            elif ipid_difference < 5000:
                self.Stas.ipid5000 = self.Stas.ipid5000 + 1
            else:
                self.Stas.ipid_inf = self.Stas.ipid_inf + 1
        print('--------------------------------------------------------')
        if not (evaluation_sample.Status == 'V'):
            evaluation_sample.Status = 'S';
        self.LANResults.remove(peer);

    def stop(self):
        self.running = False ;
    def TimeDistance(self, Creation_Time, Time) :
        Distance = (Time.tm_hour - Creation_Time.tm_hour)*float(3600) + (Time.tm_min - Creation_Time.tm_min)*float(60) + float(Time.tm_sec - Creation_Time.tm_sec)
        Day_Distance = Time.tm_mday - Creation_Time.tm_mday
        if Day_Distance == 0 :
            return Distance
        else :
            return ( 24*3600 + Distance )
    def returnStas(self):
        return [self.Stas.ipid100,self.Stas.ipid500,self.Stas.ipid1000,self.Stas.ipid2000,self.Stas.ipid3000,self.Stas.ipid5000,self.Stas.ipid_inf,self.Stas.ipid0,
                self.Stas.ttl_0,self.Stas.ttl_1,self.Stas.ttl_2,self.Stas.ttl_3,self.Stas.ttl_inf,self.Stas.V_count,self.Stas.NR_count,self.Stas.S_count]

    def returnyesno (self):
        return [self.yes_resp,self.no_resp]
    def returnStass(self):
        return [self.Stass.port80,self.Stass.port443,self.Stass.port21,self.Stass.port113,self.Stass.port25,self.Stass.port143,self.Stass.port110,
                self.Stass.port3389,self.Stass.portICMP,self.Stass.av_numberOfResponse,self.Stass.av_timeDistance]
    def printStatistics(self):
        print('--------- TTL ------------')
        print(self.yes_resp)
        print(self.Stass.av_numberOfResponse)
        print('ttl == 0 : ' + str(float(self.Stas.ttl_0) / (float(self.yes_resp * self.Stass.av_numberOfResponse))));
        print('ttl == 1 : ' + str(float(self.Stas.ttl_1) / (float(self.yes_resp * self.Stass.av_numberOfResponse))));
        print('ttl == 2 : ' + str(float(self.Stas.ttl_2) / (float(self.yes_resp * self.Stass.av_numberOfResponse))));
        print('ttl == 3 : ' + str(float(self.Stas.ttl_3) / (float(self.yes_resp * self.Stass.av_numberOfResponse))));
        print('ttl  > 3 : ' + str(float(self.Stas.ttl_inf) / (float(self.yes_resp * self.Stass.av_numberOfResponse))));
        print('--------- IPID ------------')
        print('ipid == 0 : ' + str(float(self.Stas.ipid0) / (float(self.yes_resp * self.Stass.av_numberOfResponse))));
        print(
            'ipid < 100 : ' + str(float(self.Stas.ipid100) / (float(self.yes_resp * self.Stass.av_numberOfResponse))));
        print(
            'ipid < 500 : ' + str(float(self.Stas.ipid500) / (float(self.yes_resp * self.Stass.av_numberOfResponse))));
        print('ipid < 1000 : ' + str(
            float(self.Stas.ipid1000) / (float(self.yes_resp * self.Stass.av_numberOfResponse))));
        print('ipid < 2000 : ' + str(
            float(self.Stas.ipid2000) / (float(self.yes_resp * self.Stass.av_numberOfResponse))));
        print('ipid < 3000 : ' + str(
            float(self.Stas.ipid3000) / (float(self.yes_resp * self.Stass.av_numberOfResponse))));
        print('ipid < 5000 : ' + str(
            float(self.Stas.ipid5000) / (float(self.yes_resp * self.Stass.av_numberOfResponse))));
        print(
            'ipid < inf : ' + str(float(self.Stas.ipid_inf) / (float(self.yes_resp * self.Stass.av_numberOfResponse))));

        print('----------------------EVALUATION---------------------')
        print('-----------------------------------------------------')
        print('Validated PERCENTAGE: %' + str(100 * (float(self.Stas.V_count) / float(self.yes_resp + self.no_resp))))
        print(
            'No Response PERCENTAGE: %' + str(100 * (float(self.Stas.NR_count) / float(self.yes_resp + self.no_resp))))
        print('Suspicious PERCENTAGE: %' + str(100 * (float(self.Stas.S_count) / float(self.yes_resp + self.no_resp))))
        print('-----------------------------------------------------')
        print('-----------------------------------------------------')

class statisticcc :
    def __init__ (self) :
        self.ipid100 = 0;
        self.ipid500 = 0;
        self.ipid1000 = 0;
        self.ipid2000 = 0;
        self.ipid3000 = 0;
        self.ipid5000 = 0;
        self.ipid_inf = 0;
        self.ipid0 = 0;

        self.ttl_0 = 0;
        self.ttl_1 = 0;
        self.ttl_2 = 0;
        self.ttl_3 = 0;
        self.ttl_inf = 0;

        self.V_count = 0;
        self.NR_count = 0;
        self.S_count = 0;
    def fillStas(self,a):
        self.ipid100 = a[0];
        self.ipid500 = a[1];
        self.ipid1000 =a[2];
        self.ipid2000 = a[3];
        self.ipid3000 = a[4];
        self.ipid5000 = a[5];
        self.ipid_inf = a[6];
        self.ipid0 = a[7];

        self.ttl_0 = a[8];
        self.ttl_1 = a[9];
        self.ttl_2 = a[10];
        self.ttl_3 = a[11];
        self.ttl_inf = a[12];

        self.V_count = a[13];
        self.NR_count = a[14];
        self.S_count = a[15];
class ProbeStatisticcc() :
    def __init__(self):
        self.port80 = 0;
        self.port443 = 0;
        self.port21 = 0;
        self.port113 = 0;
        self.port25 = 0;
        self.port143 = 0;
        self.port110 = 0;
        self.port3389 = 0;
        self.portICMP = 0;
        self.av_numberOfResponse = 0;
        self.av_timeDistance = 0
    def fillStass(self,a):
        self.port80 = a[0];
        self.port443 = a[1];
        self.port21 = a[2];
        self.port113 = a[3];
        self.port25 = a[4];
        self.port143 = a[5];
        self.port110 = a[6];
        self.port3389 = a[7];
        self.portICMP = a[8];
        self.av_numberOfResponse = a[9];
        self.av_timeDistance = a[10]
class Evaluation_Class :
    def __init__(self,sip,dip): #ilerde kullanilabilir
        self.Status ='' # NR = no response , S = Suspicious , V = Validated
        self.SOURCE_IP = sip
        self.DESTINATION_IP = dip
        self.Evaluations = []
        self.FinalSentence = []

class EvaStas :
    def __init__(self):
        self.Elements = []

    def AddNew (self,EvaluationS) :

        new_element = EvaStasElement(EvaluationS.SOURCE_IP)

        self.Elements.append(new_element)

    def isContainss(self,source_IP):
        for element in self.Elements :
            if element.IPNo == source_IP :
                return True
        return False
    def getElement(self,source_IP):
        for element in self.Elements :
            if element.IPNo == source_IP :
                return element
    def print_Final_Results(self):
        print("--------- SUSPICIOUS IP NUMBERS -------------")
        for element in self.Elements :
            if not (element.sus_count == 0):
                print(element.IPNo + " valid count:" + str(element.valid_count) + "  suspicious count:" + str(element.sus_count) + " Estimated False positive probability:%" + str(float(element.valid_count/ (element.valid_count + element.sus_count))*100) )
        print("--------- --------------------- -------------")


class EvaStasElement :
    def __init__(self,ip):
        self.IPNo = ip;
        self.valid_count = 0
        self.sus_count = 0
