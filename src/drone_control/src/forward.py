#!/usr/bin/env python 

#import library ros 
import rospy
import time

from AutonomousFlight import AutonomousFlight
from FollowTarget import FollowTarget

def takeoff_Land():
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
            else:
                uav.SetCommand(0,0,0,0,0,0)  
    except rospy.ROSInterruptException:
        pass    

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

def mark_rountine():
    
    '''
        w = (0, 0, 0)
        odom = (xo, yo, co)
        m = (xm, ym, zm)
        ir para:
        camera esta no eixo x

        m' = "odom + m"
        m'_x = x0 + zm, ou -x0 -zm   
        m'_y = livre
        m'_z = z0 + ym
        w -> de modo a zerar xm, erro = xm 
        

        orientation w ve controla yaw
    '''
    try:
        uav = FollowTarget()
        uav.SetCommand(0,0,0,0,0,0)
        now = time.time()
        last_time = now

        # tempo de loop ~ 100 ms        
        while not rospy.is_shutdown():
            uav.rate.sleep()
            now = time.time()
            st = uav.navdata.state
            print('\nDrone state: ' + str(st))
            
            now = rospy.get_rostime()
            # print("Current time %i %i", now.secs, now.nsecs)
            # print("AR-Mark time %s %s", uav.mark.header.stamp.secs, uav.mark.header.stamp.nsecs)
            
            # uav.printMark()
            # continue

            if st == 2:
                uav.SendTakeOff()
                last_time = time.time()
                # elif st == 3 or st == 4 or st == 7:
            elif st == 3:
                if now.secs - uav.mark.header.stamp.secs <= 1:
                    uav.controlAZ(0.0)
                    uav.controlDistance(0.4)
                    uav.controlZ(0.0) # set point com relacao a y do alvo
                    uav.controlWith(0.0) # set point con relacao a x do alvo
                else:
                    uav.SetCommand(0,0,0,0,0,0)
                    print("Lost target")
                pass

            uav.SendCommand() 
            
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    mark_rountine()
