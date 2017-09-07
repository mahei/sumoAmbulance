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

def run():


        # 76
        # sec 65
        
	step = 0
	changedRoute = False
	
	vehicle_id_last = []
	vehicle_id_now  = []
	
	while step <= STEPS:
	
                vehicle_id_now  = traci.vehicle.getIDList()

                if step == 70:
                        veh_pos = traci.vehicle.getLanePosition(vehID='76')
                     #   print (veh_pos, traci.vehicle.getSpeed(vehID='76'))
                        traci.vehicle.setStop(vehID='76', edgeID="-324493313#1", pos=veh_pos +0.0001, flags=1)
                        
                #        traci.vehicle.setStop(vehID='91', edgeID="-324493313#1", pos=135.97, flags=1)
                
                if step == 100:
                        traci.vehicle.resume(vehID='76')

                        
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
