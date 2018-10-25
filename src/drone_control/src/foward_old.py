#!/usr/bin/env python 

#import library ros 
import rospy
import time

from AutonomousFlight import AutonomousFlight
from FollowTarget import FollowTarget
from ARPoseFilter import ARPoseFilter
from ControlPose import ControlPose

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
            # uav.printData()
               
            if st == 2:
                uav.SendTakeOff()
                last_time = time.time()
            # elif st == 3 or st == 4 or st == 7:
            elif st == 4 or st == 3:
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
        init = time.time()

        while not rospy.is_shutdown():
            #try:
            uav.rate.sleep()
            st = uav.navdata.state
            # print('\nDrone state: ' + str(st))
            if st == 2:
                #print('takeoff')
                uav.SendTakeOff()
                pass
            else: 
                x = input('Put "kp,ki,kd" ')
                if type(x) is tuple and len(x) == 4:
                    print('update Pose')
                    uav.pose['x'] = x[0]
                    uav.pose['y'] = x[1]
                    uav.pose['z'] = x[2]
                    uav.pose['w'] = x[3]
                    
                    # uav.pid['x'].update_params(float(x[0]), float(x[1]), float(x[2]))
                    # uav.pid['y'].update_params(float(x[0]), float(x[1]), float(x[2]))
                else:
                    print('fail')
            #except: (ValueError, SyntaxError, TypeError, NameError):
            #print('Error')
        # 
        # tempo de loop ~ 100 ms        
        while not rospy.is_shutdown():
            # uav.rate.sleep()
            now = time.time()
            st = uav.navdata.state
            # print('\nDrone state: ' + str(st))
            # uav.printData()
            # uav.controlAZ(0.0)
            # uav.controlZ(1.0)
            # uav.controlY(1.0)
            # uav.controlX(1.0)
            # uav.SendCommand()
            # continue
            
            if st == 2:
                uav.SendTakeOff()
                last_time = time.time()
            elif (st == 3 or st == 4) and (time.time() - init >= 10):
                uav.controlAZ(0.0)
                uav.controlZ(1.5)
                uav.controlY(-1.0)
                uav.controlX(1.0)
                
            uav.SendCommand() 
            
    except rospy.ROSInterruptException:
        pass    

def filter_routine():
    ARPoseFilter()

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
        init = time.time()
        last_time = init
        
        # tempo de loop ~ 100 ms        
        while not rospy.is_shutdown():
            uav.rate.sleep()
            now = time.time()
            st = uav.navdata.state
            print('\nDrone state: ' + str(st))
            
            now = rospy.get_rostime()
            # print("Current time %i %i", now.secs, now.nsecs)
            # print("AR-Mark time %s %s", uav.mark.header.stamp.secs, uav.mark.header.stamp.nsecs)
            
            # uav.controlAZ(178.0)
            # uav.controlDistance(0.35000000000)
            # uav.controlZ(0.0) # set point com relacao a y do alvo
            # uav.controlWith(0.0) # set point con relacao a x do alvo
            # uav.SendCommand()
            
            #uav.SetCommand(0.05,0,0,0,0,0)
            # continue
              
            if st == 2:
                uav.SendTakeOff()
            elif (st == 3 or st == 4) and (time.time() - init >= 3):
                uav.controlAZ(98.0)
                if now.secs - uav.mark.header.stamp.secs <= 1:
                    uav.controlDistance(0.40)
                    uav.controlZ(0.0) # set point com relacao a y do alvo
                    uav.controlWith(0.0) # set point con relacao a x do alvo
                    uav.SendCommand()
                else:
                    # uav.SetCommand(0.0,0.0,0.0,0.0,0.0,0.0)
                    print("Lost target")
                    
    except rospy.ROSInterruptException:
        pass

def control_pose_routine():
    try:
        uav = ControlPose()
        uav.SetCommand(0,0,0,0,0,0)
        now = time.time()
        last_time = now
        init = time.time()
        
        while not rospy.is_shutdown():
            uav.rate.sleep()
            st = uav.navdata.state
            print('\nDrone state: ' + str(st))
            
            if st == 2:
                print('takeoff')
                # uav.SendTakeOff()
                pass
            elif(st == 4 or st == 3):
                uav.controlAZ(0.0)
                uav.controlZ(1.0)
                # uav.controlY(0.0)
                uav.controlX(0.0)
                uav.SendCommand()

                continue
                x = input('Put "kp,ki,kd" ')
                if type(x) is tuple and len(x) == 4:
                    print('update Pose')
                    uav.pose['x'] = x[0]
                    uav.pose['y'] = x[1]
                    uav.pose['z'] = x[2]
                    uav.pose['w'] = x[3]
                    
                    # uav.pid['x'].update_params(float(x[0]), float(x[1]), float(x[2]))
                    # uav.pid['y'].update_params(float(x[0]), float(x[1]), float(x[2]))
                
            
    except rospy.ROSInterruptException:
        pass 

if __name__ == '__main__':
    control_pose_routine()
    #test_rountine()
    # control_rountine()
    ##rospy.init_node('forward', anonymous=False)    
    ##filter_routine()
    ##mark_rountine()
