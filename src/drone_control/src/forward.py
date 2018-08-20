#!/usr/bin/env python 

#import library ros 
import rospy
import time

#import library untuk mengirim command dan menerima data navigasi dari quadcopter
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from std_msgs.msg import Empty
from ardrone_autonomy.msg import Navdata
from nav_msgs.msg import Odometry
from visualization_msgs.msg import Marker

#import class status untuk menentukan status ddari quadcopter
# from drone_status import DroneStatus

COMMAND_PERIOD = 1000

MAX_SPEED = 1
SPEED = 0.25*MAX_SPEED
DELAY = 2

class AutonomousFlight():
    def __init__(self):
        self.status = ""
        rospy.init_node('forward', anonymous=False)
        rospy.Subscriber("/ardrone/navdata", Navdata, self.cbNavdata)
        rospy.Subscriber("/ardrone/odometry", Odometry, self.cbOdom)
        rospy.Subscriber("/visualization_marker", Marker, self.cbMarker)
        self.navdata = Navdata()
        self.odom = Odometry()
        self.mark = Marker()

        self.rate = rospy.Rate(10)
        self.pubTakeoff = rospy.Publisher("ardrone/takeoff",Empty, queue_size=10)
        self.pubLand = rospy.Publisher("ardrone/land",Empty, queue_size=10)
        self.pubLand = rospy.Publisher("ardrone/land",Empty, queue_size=10)
        self.pubCommand = rospy.Publisher('cmd_vel',Twist, queue_size=10)
        self.command = Twist()
        
        #self.commandTimer = rospy.Timer(rospy.Duration(COMMAND_PERIOD/1000.0),self.SetCommand)
        self.state_change_time = rospy.Time.now()
        rospy.on_shutdown(self.SendLand)

    def SendTakeOff(self):
        self.pubTakeoff.publish(Empty())
        self.rate.sleep()

    def SendLand(self):
        self.pubLand.publish(Empty())

    def SetCommand(self, linear_x, linear_y, linear_z, angular_x, angular_y, angular_z):
        self.command.linear.x = linear_x
        self.command.linear.y = linear_y
        self.command.linear.z = linear_z
        self.command.angular.x = angular_x
        self.command.angular.y = angular_y
        self.command.angular.z = angular_z
        self.pubCommand.publish(self.command)
        self.rate.sleep()
    
    def cbNavdata(self, msg):
        #print(msg)
        self.navdata = msg
    
    def cbOdom(self, msg):
        #print(msg)
        self.odom = msg

    def cbMarker(self, msg):
        self.mark = msg
        #print(self.mark)
   
    def printNavdata(self):
        nd = self.navdata
        print('NAVDATA -- bt: ' + str(nd.batteryPercent) + \
            '\nspeed: ' + str(nd.vx) + ', ' + str(nd.vy) + ', ' + str(nd.vx) + \
            '\nangles: ' + str(nd.rotX) + ', ' + str(nd.rotY) + ', ' + str(nd.rotZ))

    def printOdom(self):
        od = self.odom
        print('ODOMETRY:\n'\
            'pose: ' + str(od.pose.pose.position.x) + ', ' +\
            str(od.pose.pose.position.y) + ', ' + str(od.pose.pose.position.z) +\
            '\norientation: ' + str(od.pose.pose.orientation.x) + ', ' +\
            str(od.pose.pose.orientation.y) + ', ' + str(od.pose.pose.orientation.z)) 

    def printMark(self):
        mk = self.mark
        print('AR-MARK:\n'\
            'pose: ' + str(mk.pose.position.x) + ',' +\
            str(mk.pose.position.y) + ', ' + str(mk.pose.position.z))

    def printData(self):
        self.printNavdata()
        self.printOdom()
        self.printMark()
        print
        pass

    def controlAZ(self):
        vz = (self.navdata.rotZ/(180/7))
        if abs(vz > 1): vz = 1
        print("Control Orientation rotZ: " + str(self.navdata.rotZ) + ", vz: " +  str(vz))
        self.SetCommand(0,0,0,vz,0,0)
        pass

    def droneTask(self, time_pass):
        #if(abs(self.navdata.rotZ) > 5):
        #    self.controlAZ()
        #    return

        if time_pass > 6*DELAY:
            self.SetCommand(0,0,0,0,0,0)
            print("Drone Finish - rotZ: " + str(self.navdata.rotZ))            
        elif time_pass > 5*DELAY:
            self.SetCommand(SPEED,0,0,0,0,0)
            print("Drone Foward - rotZ: " + str(self.navdata.rotZ))            
        elif time_pass > 4*DELAY:
            self.SetCommand(0,-SPEED,0,0,0,0)
            print("Drone Right - rotZ: " + str(self.navdata.rotZ))
        elif time_pass > 3*DELAY:
            print("Drone Back - rotZ: " + str(self.navdata.rotZ))
            self.SetCommand(-SPEED,0,0,0,0,0)
        elif time_pass > 2*DELAY:
            self.SetCommand(0,SPEED,0,0,0,0)
            print("Drone Left - rotZ: " + str(self.navdata.rotZ))
        elif time_pass > DELAY:
            print("Drone Foward - rotZ: " + str(self.navdata.rotZ))
            self.SetCommand(SPEED,0,0,0,0,0)    
        
if __name__ == '__main__':
    try:
        uav = AutonomousFlight()
        #rospy.spin()
        now = time.time()
        last_time = now

        # tempo de loop ~ 100 ms        
        while not rospy.is_shutdown():
            ##uav.printData()
            ##time.sleep(1)
            # Time loop
            now = time.time()
            
            st = uav.navdata.state
            if st == 2:
                uav.SendTakeOff()
                last_time = time.time()
            elif st == 3 or st == 4 or st == 7:
                #uav.printNavdata()
                #print(uav.navdata.rotZ)
                #uav.droneTask(now - last_time);     
                pass
            else:
                uav.SetCommand(0,0,0,0,0,0)
                print('Drone state: ' + str(st))

    except rospy.ROSInterruptException:
        pass
