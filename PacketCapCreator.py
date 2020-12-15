import threading;
from threading import Thread;
from PacketCap import *;
import time;

import os;

class Packet_catcher_creator(Thread) :

    def __init__(self,delayTime,queue_to_PR):
        Thread.__init__(self);

        self.IP_Addresses_List = [];

        self.Interface_List = [];

        self.running = True ;

        self.delay =delayTime ;

        self.Created_Catchers:Packet_Catcher = [] ;

        self.Created_ThreadEvents = [] ;

        self.to_PR = queue_to_PR


    def run(self):
        while self.running == True :
            newcomings:dict = {};

            newcomings= dict(zip(self.Interface_List,self.IP_Addresses_List));

            for IN,IP in newcomings.items():
                match_found = False;
                for catcher in self.Created_Catchers:
                    if catcher.Interface_Name ==  IN :
                        match_found =True;
                        if catcher.Ip == IP :
                            break;
                        else :
                            catcher.Ip = IP;
                            print("IP address of " + IN + " changed to " + IP + " !!!" );

                    else :
                        continue;
                if (match_found==False):
                    new_packet_catch_unit = Packet_Catcher(IP,IN,self.to_PR);

                    e = threading.Event();
                    self.Created_ThreadEvents.append(e);
                    t = threading.Thread(target=new_packet_catch_unit._TheSniff,args=(e,));
                    t.start();


                    self.Created_Catchers.append(new_packet_catch_unit);



            time.sleep(self.delay);

    def stop(self):
        for event in self.Created_ThreadEvents:
            event.set();


        self.running = False ;
