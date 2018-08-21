#!/usr/bin/env python 

#import library ros 
import rospy
import time

from AutonomousFlight import AutonomousFlight

def test_rountine():
    try:
        uav = AutonomousFlight()
        #rospy.spin()
        now = time.time()
        last_time = now

        # tempo de loop ~ 100 ms        
        while not rospy.is_shutdown():
            uav.rate.sleep()
            now = time.time()
            st = uav.navdata.state
            print('Drone state: ' + str(st))
            uav.printData()
               
            if st == 2:
                uav.SendTakeOff()
                last_time = time.time()
                # elif st == 3 or st == 4 or st == 7:
            elif st == 3:
                uav.droneTask(now - last_time);     
                pass
            else:
                uav.SetCommand(0,0,0,0,0,0)
                pass                

            
    except rospy.ROSInterruptException:
        pass    

def control_rountine():
    try:
        uav = AutonomousFlight()
        uav.SetCommand(0,0,0,0,0,0)
        now = time.time()
        last_time = now

        # tempo de loop ~ 100 ms        
        while not rospy.is_shutdown():
            uav.rate.sleep()
            now = time.time()
            st = uav.navdata.state
            print('\nDrone state: ' + str(st))
               
            if st == 2:
                uav.SendTakeOff()
                last_time = time.time()
                # elif st == 3 or st == 4 or st == 7:
            elif st == 3:
                uav.printData()
                uav.controlAZ(0)
                uav.controlZ(2.0)
                uav.controlY(-1.0)
                uav.controlX(-1.0)
                
                pass
            uav.SendCommand() 
            
    except rospy.ROSInterruptException:
        pass    


if __name__ == '__main__':
    control_rountine()
