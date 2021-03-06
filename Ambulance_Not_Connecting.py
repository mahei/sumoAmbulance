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


STEPS = 200

ambulance_insertion_step = None
ambulance_arrival_step   = None


def run():

        global ambulance_insertion_step
        global ambulance_arrival_step   

	step = 0
	       
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

               
                        
		print('step', step, 'vehicle number', len(traci.vehicle.getIDList()))
		
		
		traci.simulationStep()
		step += 1
		
	traci.close()

        ambulance_travel_time = ambulance_arrival_step - ambulance_insertion_step
        print ('ambulance insterion step' ,         ambulance_insertion_step) 
        print ('ambulance arrival   step' ,         ambulance_arrival_step) 
        print ('ambulance travel time   ' ,         ambulance_travel_time) 

       
        ambulance_arrival_step   = None 
	sys.stdout.flush()

if __name__ == "__main__":
      
    sumoBinary = checkBinary('sumo-gui')

    traci.start([sumoBinary, "-c", "MapFirenze7/map.sumocfg",
							 ])
    run()
