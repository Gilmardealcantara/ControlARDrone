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
        # print(msg)
        self.navdata = msg
    
    def cbOdom(self, msg):
        #print(msg)
        self.odom = msg

    def cbMarker(self, msg):
        self.mark = msg
        #print(self.mark)
   
    def printNavdata(self):
        nd = self.navdata;
        print('NAVDATA -- bt: ' + str(nd.batteryPercent) + '\n'\
            'speed: ' + str(nd.vx) + ', ' + str(nd.vy) + ', ' + str(nd.vx) + \
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
    
if __name__ == '__main__':
    try:
        i = 0
        uav = AutonomousFlight()
        #rospy.spin()
        while not rospy.is_shutdown():
            uav.printData()
            time.sleep(1)
            #uav.SendTakeOff()
            #uav.SetCommand(0,0,1,0,0,0) 
    
    
    except rospy.ROSInterruptException:
        pass
