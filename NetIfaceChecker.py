import subprocess
import time;
from threading import Thread;

import netifaces;


class IP_Finder(Thread):

    def __init__(self, delay_second, p_c_c, queue_to_PR,queue_to_probe):
        Thread.__init__(self)
        self.IP_Address_List = [];
        self.Active_Interface_List = [];
        self.Network_Mask_List = []
        self.AddressRangeList = []
        self.to_Probe = queue_to_probe
        self.running = True;
        self.delay = delay_second;
        self.PCC = p_c_c;
        self.to_PR = queue_to_PR

    def run(self):

        while self.running == True:

            self.IP_Address_List = [];
            self.Active_Interface_List = [];
            self.Network_Mask_List = []
            self.AddressRangeList = []
            interfaces= netifaces.interfaces();
            interfaces.remove('lo')

            for interfacee in interfaces:
                try:
                    addrs = netifaces.ifaddresses(interfacee)
                    addresses = addrs[netifaces.AF_INET];



                    ip_adress_of_operational_interface = addresses[0]['addr'];
                    if (interfacee is not self.Active_Interface_List):

                        self.IP_Address_List.append(ip_adress_of_operational_interface);

                        self.Active_Interface_List.append(interfacee);
                        Mask = addresses[0]['netmask']
                        
                        self.Network_Mask_List.append(Mask)
                        L = self.GetMaskLenght(Mask)

                        N_A = self.getNetworkAddress(ip_adress_of_operational_interface, Mask)  # string

                        if N_A is not None:
                            Range = self.getRange(N_A, self.GetMaskLenght(Mask))  # AddressRange class
                            self.AddressRangeList.append(Range)


                except:
                    continue




            self.PCC.Interface_List = self.Active_Interface_List;

            self.PCC.IP_Addresses_List = self.IP_Address_List;
            SendingList = [self.IP_Address_List,self.Network_Mask_List,self.AddressRangeList]
            SendingListtoProbe = [self.IP_Address_List,self.Active_Interface_List]
            if self.to_PR.empty():
                self.to_PR.put(SendingList);
            else :
                while not self.to_PR.empty():
                    self.to_PR.get()
                self.to_PR.put(SendingList);
            if self.to_Probe.empty():
                self.to_Probe.put(SendingListtoProbe);
            else :
                while not self.to_Probe.empty():
                    self.to_Probe.get()
                self.to_Probe.put(SendingListtoProbe);

            time.sleep(self.delay);

    def getRange(self, N_A, Lenght):
        address_size = (2) ** (32 - int(Lenght))
        address_size_backup = address_size
        FirstOctetChange = address_size_backup // ((2) ** (24))
        address_size = address_size % ((2) ** (24))

        address_size_backup = address_size
        SecondOctetChange = address_size_backup // ((2) ** (16))
        address_size = address_size % ((2) ** (16))

        address_size_backup = address_size
        ThirdOctetChange = address_size_backup // ((2) ** (8))
        address_size = address_size % ((2) ** (8))

        address_size_backup = address_size
        ForthOctetChange = address_size_backup
        N_A_octets = N_A.split('.');
        LastRAnge0 = int(N_A_octets[0]) + int(FirstOctetChange)
        LastRAnge1 = int(N_A_octets[1]) + int(SecondOctetChange)
        LastRAnge2 = int(N_A_octets[2]) + int(ThirdOctetChange)
        LastRAnge3 = int(N_A_octets[3]) + int(ForthOctetChange)
        ResultRange = AddressRange()
        ResultRange.set_Min_Address(
            str(N_A_octets[0] + '.' + N_A_octets[1] + '.' + N_A_octets[2] + '.' + str(int(N_A_octets[3]) + 1)))
        ResultRange.set_Max_Address(self.getMax(LastRAnge0, LastRAnge1, LastRAnge2, LastRAnge3));
        return ResultRange

    def getMax(self, l1, l2, l3, l4):
        if l4 == 0:
            l4 = 255;
            if l3 == 0:
                l3 = 255
                if l2 == 0:
                    l2 = 255
                    if l1 == 0:
                        l1 = 255
                    else:
                        l1 = l1 - 1
                else:
                    l2 = l2 - 1
            else:
                l3 = l3 - 1
        else:
            l4 = l4 - 1
        return str(str(l1) + '.' + str(l2) + '.' + str(l3) + '.' + str(l4))

    def GetMaskLenght(self, Mask):
        Octets = Mask.split('.')
        Lenght = 0
        for Octet in Octets:
            if int(Octet) == 0:
                return Lenght
            elif int(Octet) == 128:
                return Lenght + 1
            elif int(Octet) == 192:
                return Lenght + 2
            elif int(Octet) == 224:
                return Lenght + 3
            elif int(Octet) == 240:
                return Lenght + 4
            elif int(Octet) == 248:
                return Lenght + 5
            elif int(Octet) == 252:
                return Lenght + 6
            elif int(Octet) == 254:
                return Lenght + 7
            else:
                Lenght = Lenght + 8

    def getNetworkAddress(self, IP, Mask):

        if (IP is not None) & (Mask is not None):
            IP_octets = IP.split('.')
            Mask_octets = Mask.split('.')
            N_A_octets = []
            counter = 0
            for counter in range(4):
                if int(Mask_octets[counter]) == 255:
                    N_A_octets.append(IP_octets[counter])
                elif not int(Mask_octets[counter]) == 0:
                    differenceOfTList = 256 - int(Mask_octets[counter])
                    counter2 = 0;
                    Temp_List = []
                    while counter2 <= 256:
                        Temp_List.append(counter2)
                        counter2 = counter2 + differenceOfTList


                    for counter2 in range(500):
                        if ((Temp_List[counter2]) <= int(IP_octets[counter])) & (
                                int(IP_octets[counter]) < (Temp_List[counter2 + 1] )):
                            N_A_octets.append(str(Temp_List[counter2]))

                            break;
                else:
                    N_A_octets.append('0')

            return (N_A_octets[0] + '.' + N_A_octets[1] + '.' + N_A_octets[2] + '.' + N_A_octets[3])

    def GetNetworkMask(self, IP_Address):
        command = "sudo ip addr";
        pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE).stdout;
        o = pipe.readlines()
        output_words = str(o).split(' ')
        for target_word in output_words:
            if IP_Address in target_word:
                Last_target_word = target_word.split('/')
                Mask_Lenght = Last_target_word[1];
                return self.get_MaskFromLenght(int(Mask_Lenght))

    def get_MaskFromLenght(self, L):
        if L == 1:
            return '128.0.0.0'
        elif L == 2:
            return '192.0.0.0'
        elif L == 3:
            return '224.0.0.0'
        elif L == 4:
            return '240.0.0.0'
        elif L == 5:
            return '248.0.0.0'
        elif L == 6:
            return '252.0.0.0'
        elif L == 7:
            return '254.0.0.0'
        elif L == 8:
            return '255.0.0.0'
        elif L == 9:
            return '255.128.0.0'
        elif L == 10:
            return '255.192.0.0'
        elif L == 11:
            return '255.224.0.0'
        elif L == 12:
            return '255.240.0.0'
        elif L == 13:
            return '255.248.0.0'
        elif L == 14:
            return '255.252.0.0'
        elif L == 15:
            return '255.254.0.0'
        elif L == 16:
            return '255.255.0.0'
        elif L == 17:
            return '255.255.128.0'
        elif L == 18:
            return '255.255.192.0'
        elif L == 19:
            return '255.255.224.0'
        elif L == 20:
            return '255.255.240.0'
        elif L == 21:
            return '255.255.248.0'
        elif L == 22:
            return '255.255.252.0'
        elif L == 23:
            return '255.255.254.0'
        elif L == 24:
            return '255.255.255.0'
        elif L == 25:
            return '255.255.255.128'
        elif L == 26:
            return '255.255.255.192'
        elif L == 27:
            return '255.255.255.224'
        elif L == 28:
            return '255.255.255.240'
        elif L == 29:
            return '255.255.255.248'
        elif L == 30:
            return '255.255.255.252'
        else:
            return 'no mask!!!'

    def stop(self):
        self.running = False


class AddressRange:
    def __init__(self):
        return

    def set_Min_Address(self, min):
        self.Min_Address = min;

    def set_Max_Address(self, max):
        self.Max_Address = max;
