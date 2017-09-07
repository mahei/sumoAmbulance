#!/usr/bin/env python
"""
@file    runner.py
@author  Lena Kalleske
@author  Daniel Krajzewicz
@author  Michael Behrisch
@author  Jakob Erdmann
@date    2009-03-26
@version $Id: runner.py 22608 2017-01-17 06:28:54Z behrisch $

Tutorial for traffic light control via the TraCI interface.

SUMO, Simulation of Urban MObility; see http://sumo.dlr.de/
Copyright (C) 2009-2017 DLR/TS, Germany

This file is part of SUMO.
SUMO is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.
"""
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import subprocess
import random

class MyVehicle():

	def __init__(self,id):

		self.myID = id
		self.instert_time = step

	def printData(self):
		print('vehID', self.myID, "insertion time: ", self.insert_time)
	
	
	
# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import traci


STEPS = 1000

ambulance_insertion_step = None
ambulance_arrival_step   = None


def run():

        global ambulance_insertion_step
        global ambulance_arrival_step   

	step = 0
	

        my_output_file = open(os.path.join('MapFirenze7','some_output.txt'), 'w')

        changedRoute = False

        
	vehicle_id_last = []
	vehicle_id_now  = []


	while step <= STEPS:

                # check if the ambulance did arrive

                if ambulance_insertion_step is None:
                        inserted_vehicles_last = traci.simulation.getDepartedIDList()
        
                        if "ambulance_0" in inserted_vehicles_last:
                                ambulance_insertion_step = step

                if ambulance_arrival_step is None:
                        arrived_vehicles_last = traci.simulation.getArrivedIDList()
                        if "ambulance_0" in arrived_vehicles_last:
                                ambulance_arrival_step   = step 
                
                vehicle_id_now  = traci.vehicle.getIDList()

                if step == 71:
                        veh_pos = traci.vehicle.getLanePosition(vehID='76')
                     #   print (veh_pos, traci.vehicle.getSpeed(vehID='76'))
                        traci.vehicle.setStop(vehID='76', edgeID="-324493313#1", pos=veh_pos +0.0001, flags=1)
                        
#                if step == 80:
#                        traci.vehicle.moveTo(vehID="ambulance_0", laneID="-324493313#0_0", pos=0.01)
                        
                
                if step == 100:
                        traci.vehicle.resume(vehID='76')


                if step == 125:

                        traci.lane.setAllowed(laneID="-324493313#0_0",
                                              allowedClasses = ['authority'])

                        traci.lane.setDisallowed(laneID="-324493313#0_0",
                                              disallowedClasses = ['private', 'emergency', 'army', 'vip', 'passenger', 'hov', 'taxi', 'bus', 'coach',
                                                                   'delivery', 'truck', 'trailer', 'tram', 'rail_urban', 'rail', 'rail_electric',
                                                                   'motorcycle', 'moped', 'bicycle', 'pedestrian', 'evehicle', 'ship',
                                                                   'custom1', 'custom2'])
                        
                           
#                        print ('Dissalowed',  traci.lane.getDisallowed(laneID="-324493313#0_0")   )     
#

                        
		print('step', step, 'vehicle number', len(traci.vehicle.getIDList()))
		#if step == 20 :
			##traci.vehicle.changeTarget(vehID='0', edgeID="-24778980#0")
		
		if "0" in traci.vehicle.getIDList() and not changedRoute:
			if traci.vehicle.getRoadID(vehID='0') == "202463503#1" :
				traci.vehicle.setRoute(vehID='0', edgeList=["202463503#1", "202463503#2", "202463503#3", "4405726#1", "4405726#2", "4405726#3", "4405726#4"])
				changedRoute = True
		traci.simulationStep()
		step += 1
		
	traci.close()

        ambulance_travel_time = ambulance_arrival_step - ambulance_insertion_step
        print ('ambulance insterion step' ,         ambulance_insertion_step) 
        print ('ambulance arrival   step' ,         ambulance_arrival_step) 
        print ('ambulance travel time   ' ,         ambulance_travel_time) 

        my_out_string = ';'.join([str(ambulance_insertion_step), str(ambulance_arrival_step), str(ambulance_travel_time)])
        
        my_output_file.write(my_out_string)
        my_output_file.close()
        
        ambulance_arrival_step   = None 
	sys.stdout.flush()




# this is the main entry point of this script
if __name__ == "__main__":
   

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    
    #    sumoBinary = checkBinary('sumo')
    sumoBinary = checkBinary('sumo-gui')

   

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "MapFirenze7/map.sumocfg",
                             #"--tripinfo-output", "tripinfo.xml"
							 ])
    run()
