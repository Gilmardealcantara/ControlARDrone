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
from PIDControl import PIDControl
#import class status untuk menentukan status ddari quadcopter
# from drone_status import DroneStatus

COMMAND_PERIOD = 1000
DEBUG = False
MAX_SPEED = 1
SPEED = 0.1*MAX_SPEED
DELAY = 5
# tempo de amostragem
T = 100.0

class AutonomousFlight():
    def __init__(self):
        self.status = ""
        rospy.init_node('forward', anonymous=False)
        self.navdata = Navdata()
        self.odom = Odometry()
        self.mark = Marker()
        self.last_time = time.time()
        self.state = "hover"
        self.speed = 0.0
        self.count = 0

        self.rate = rospy.Rate(100.0) # self.rate.sleep_dur.nsecs/1000000
        self.period_s = self.rate.sleep_dur.nsecs/1000000000.0 # second
        #self.period_s = self.rate.sleep_dur.nsecs/1000000.0 # milisecons
        
        self.pidAlt = PIDControl(self.period_s, 1, 0, 0, 'Altitude control')

        self.pubTakeoff = rospy.Publisher("ardrone/takeoff",Empty, queue_size=10)
        self.pubLand = rospy.Publisher("ardrone/land",Empty, queue_size=10)
        self.pubLand = rospy.Publisher("ardrone/land",Empty, queue_size=10)
        self.pubCommand = rospy.Publisher('cmd_vel',Twist, queue_size=10)
        self.command = Twist()
        rospy.Subscriber("/ardrone/navdata", Navdata, self.cbNavdata)
        # rospy.Subscriber("/ardrone/odometry", Odometry, self.cbOdom)
        rospy.Subscriber("/ground_truth/state", Odometry, self.cbOdom)
        rospy.Subscriber("/visualization_marker", Marker, self.cbMarker)
        self.state_change_time = rospy.Time.now()
        rospy.on_shutdown(self.SendLand)

    def SendTakeOff(self):
        self.pubTakeoff.publish(Empty())
        self.rate.sleep()

    def SendLand(self):
        self.pubLand.publish(Empty())
        self.rate.sleep()

    def SendCommand(self):
        self.pubCommand.publish(self.command)
        # self.rate.sleep()
    
    def SetCommand(self, linear_x, linear_y, linear_z, angular_x, angular_y, angular_z):
        self.command.linear.x = linear_x
        self.command.linear.y = linear_y
        self.command.linear.z = linear_z
        self.command.angular.x = angular_x
        self.command.angular.y = angular_y
        self.command.angular.z = angular_z
        self.SendCommand()

    def cbNavdata(self, msg):
        self.navdata = msg
    
    def cbOdom(self, msg):
        self.odom = msg

    def cbMarker(self, msg):
        self.mark = msg
   
    def printNavdata(self):
        nd = self.navdata
        print('NAVDATA -- bt: ' + str(nd.batteryPercent) +
            '\nvx:   ' + str(nd.vx) + 
            '\nvy:   ' + str(nd.vy) + 
            '\nvz:   ' + str(nd.vx) + 
            '\nrotZ: ' + str(nd.rotZ))
            # '\nangles: ' + str(nd.rotX) + ', ' + str(nd.rotY) + ', ' + str(nd.rotZ))

    def printOdom(self):
        od = self.odom
        print('ODOMETRY:\n'\
            'pose:' +
            '\nx: ' + str(od.pose.pose.position.x) + 
            '\ny: ' + str(od.pose.pose.position.y) + 
            '\nz: ' + str(od.pose.pose.position.z))# +\
            # '\norientation: ' + str(od.pose.pose.orientation.x) + ', ' +\
            # str(od.pose.pose.orientation.y) + ', ' + str(od.pose.pose.orientation.z)) 

    def printMark(self):
        mk = self.mark
        print('AR-MARK:pose' + 
            '\nposition:\n\tx: ' + str(mk.pose.position.x) + 
            '\n\ty: ' + str(mk.pose.position.y) + 
            '\n\tz: ' + str(mk.pose.position.z) +
            '\norientation:\n\tx: ' + str(mk.pose.orientation.x) + 
            '\n\ty: ' + str(mk.pose.orientation.y) + 
            '\n\tz: ' + str(mk.pose.orientation.z) + 
            '\n\tw: ' + str(mk.pose.orientation.w)
        )

    def printData(self):
        self.printNavdata()
        self.printOdom()
        # self.printMark()
        print
        pass

    def saturation(self, vel):
        if vel > SPEED: return SPEED
        elif vel < -SPEED: return -SPEED
        return vel
    
    def setLastTime(self, lt):
        self.last_time = lt

    def droneTask(self, now):
        time_pass = now - self.last_time
        if(time_pass >= DELAY):
            self.count +=1
            self.last_time = now
            if self.count == 1: self.state = "flyUp"
            if self.count == 2: self.state = "hover"
            if self.count == 3: self.state = "flyDown"
            if self.count > 3: self.state = "hover"
            
            # self.state = "flyUp" if self.count <= 3 else "flyDown"
            # if(self.state == "hover" and self.count <= 7):
            #     self.state = "flyUp" if self.count <= 3 else "flyDown"
            # else:
            #     self.state = "hover"
                
        print(self.state)
        print(time_pass)
        if(self.state == "hover"):
            self.SetCommand(0,0,0,0,0,0)
        elif(self.state == "flyUp"):
            self.SetCommand(0,0,SPEED,0,0,0)
        elif(self.state == "flyDown"):
            self.SetCommand(0,0,-SPEED,0,0,0)
