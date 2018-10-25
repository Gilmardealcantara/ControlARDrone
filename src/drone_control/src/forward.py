#!/usr/bin/env python 

#import library ros 
import rospy
import time
from math import sqrt

from AutonomousFlight import AutonomousFlight
from FollowTarget import FollowTarget
from ARPoseFilter import ARPoseFilter
from ControlPose import ControlPose
from CamposVetoriais import CamposVetoriais

def get_data():
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
            # uav.printData()
            if st == 2:
                uav.SendTakeOff()
                uav.setLastTime(now)
            elif (st == 4 or st == 3) and (now - last_time) > 10:
                uav.droneTask(now); 
                pass
            else:
                uav.SetCommand(0,0,0,0,0,0)
                pass
    except rospy.ROSInterruptException:
        pass    

def campos_vetoriais():
    try:
        uav = CamposVetoriais()
        raio = 1.0
            

        while uav.navdata.state != 3 and  uav.navdata.state != 7: 
            uav.SendTakeOff()
            print(uav.navdata.state)
        # rospy.spin()

        while not rospy.is_shutdown():  
            uav.rate.sleep()
            x = uav.odom.pose.pose.position.x
            y = uav.odom.pose.pose.position.y
            z = uav.odom.pose.pose.position.z
            yaw = uav.navdata.rotZ

            vw =  -((yaw - 45)/90)
            vz = - (z - 1.000)

            vx_n = 0 
            vy_n = 0
            if yaw > 40.0 and yaw < 50.0:
                vx =  - ((pow(x, 4) + pow(y, 4) - pow(raio, 4)) * 4 * pow(x, 3))/ pow(raio, 4) - 4 * pow(y, 3)                                                     
                vy =  - ((pow(x, 4) + pow(y, 4) - pow(raio, 4)) * 4 * pow(y, 3))/pow(raio, 4) + 4 * pow(x, 3)
                vx_n = 0.5 * (vx / (sqrt(pow(vx, 2) + pow(vy, 2)) + 0.0001))
                vy_n = 0.5 * (vy / (sqrt(pow(vx, 2) + pow(vy, 2)) + 0.0001 ))

            uav.SetCommand(vx_n,vy_n,0,0,0,vw)
            
            print("__x: " + str(x))
            print("__y: " + str(y))
            print("__z: " + str(z))
            print("yaw: " + str(yaw))
            print("_vx: " + str(vx_n))
            print("_vy: " + str(vy_n))
            print("_vz: " + str(vz))
            print()


    except rospy.ROSInterruptException:
        pass  

def control():
    try:
        uav = AutonomousFlight()
        # uav.pidAlt.update_params(0.06231, 0.00001301, 0)
        uav.pidAlt.update_params(3.096,0.07325, 0.0)
        uav.pidAlt.set_point(2.0)
        last_time = rospy.get_rostime().nsecs
        lt = time.time() 
        # tempo de loop ~ 100 ms        
        while not rospy.is_shutdown():
            uav.rate.sleep()
            

            st = uav.navdata.state
            # print('Drone state: ' + str(st))
            
            if st == 2:
                uav.SendTakeOff()
            elif (st == 4 or st == 3) and ((time.time() - lt) > 5):
                vel = uav.pidAlt.get_vel(uav.odom.pose.pose.position.z)
                uav.SetCommand(0,0,vel,0,0,0)
                # now = rospy.get_rostime()
                # print("Set time: %i", uav.rate.sleep_dur.nsecs/1000000000.0)
                # print("Cur time: %i", (now.nsecs - last_time)/1000000000.0)
                # last_time = now.nsecs
                pass
            else:
                uav.SetCommand(0,0,0,0,0,0)
                pass
    except rospy.ROSInterruptException:
        pass 

def control_routine():
    try:
        uav = AutonomousFlight()
        # uav.pidAlt.update_params(0.06231, 0.00001301, 0)
        uav.pidAlt.update_params(3.096,0.07325, 0.0)
        uav.pidAlt.set_point(1.0)
            
        last_time = rospy.get_rostime().nsecs
        lt = time.time()
        state = 0; 
        # tempo de loop ~ 100 ms        
        while not rospy.is_shutdown():
            uav.rate.sleep()
            
            st = uav.navdata.state
            # print('Drone state: ' + str(st))
            
            if st == 2:
                uav.SendTakeOff()
            elif (st == 4 or st == 3):
                now = time.time()
                if(now - lt > 5):
                    lt = now
                    if(state == 0): uav.pidAlt.set_point(1.5)
                    if(state == 1): uav.pidAlt.set_point(2.0)
                    if(state == 2): uav.pidAlt.set_point(2.5)
                    if(state == 3): uav.pidAlt.set_point(2.0)
                    if(state == 4): uav.pidAlt.set_point(1.5)
                    if(state == 5): uav.pidAlt.set_point(1.0)
                    state+=1
                vel = uav.pidAlt.get_vel(uav.odom.pose.pose.position.z)
                uav.SetCommand(0,0,vel,0,0,0)
                # now = rospy.get_rostime()
                # print("Set time: %i", uav.rate.sleep_dur.nsecs/1000000000.0)
                # print("Cur time: %i", (now.nsecs - last_time)/1000000000.0)
                # last_time = now.nsecs
                pass
            else:
                uav.SetCommand(0,0,0,0,0,0)
                pass
    except rospy.ROSInterruptException:
        pass 



if __name__ == '__main__':
    campos_vetoriais()

