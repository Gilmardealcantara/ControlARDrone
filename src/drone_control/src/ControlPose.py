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
from tum_ardrone.msg import filter_state
from visualization_msgs.msg import Marker
from PID import PID
#import class status untuk menentukan status ddari quadcopter
# from drone_status import DroneStatus

COMMAND_PERIOD = 1000
DEBUG = True
MAX_SPEED = 1
SPEED = MAX_SPEED
DELAY = 2
# tempo de amostragem
T = 100.0

class ControlPose():
    def __init__(self):
        self.status = ""
        rospy.init_node('forward', anonymous=False)
        self.pid = {
            'az': PID(T * 0.001, (1.0/(180.0*1)), 0, 0, "Orientation"),
            # 'az': PID(T/1000.0, 2.0, 0.0, 1.0, "Orientation"),
            'z':  PID(T/1000.0, 1.0, 0.000, 0.0, "Altitude"),
            'x':  PID(T/1000.0, 1.0, 0.000, 0.0, "X Position"),
            'y':  PID(T/1000.0, 1.0, 0.000, 0.0, "Y Position")
        }

        self.navdata = Navdata()
        self.odom = Odometry()
        self.mark = Marker()
        self.predictPose = filter_state()

        self.rate = rospy.Rate(100)
        self.pose = {'x': -1.0,'y': -1.0, 'z': 1.0, 'w': 0.0}
        self.pubTakeoff = rospy.Publisher("ardrone/takeoff",Empty, queue_size=10)
        self.pubLand = rospy.Publisher("ardrone/land",Empty, queue_size=10)
        self.pubLand = rospy.Publisher("ardrone/land",Empty, queue_size=10)
        self.pubCommand = rospy.Publisher('cmd_vel',Twist, queue_size=10)
        self.command = Twist()
        rospy.Subscriber("/ardrone/navdata", Navdata, self.cbNavdata)
        rospy.Subscriber("/ardrone/predictedPose", filter_state, self.cbPose)
        # rospy.Subscriber("/ardrone/odometry", Odometry, self.cbOdom)
        # rospy.Subscriber("/ground_truth/state", Odometry, self.cbOdom)
        rospy.Subscriber("/visualization_marker", Marker, self.cbMarker)
        self.state_change_time = rospy.Time.now()
        # rospy.on_shutdown(self.SendLand)

    def SendTakeOff(self):
        self.pubTakeoff.publish(Empty())
        self.rate.sleep()

    def SendLand(self):
        self.pubLand.publish(Empty())
        self.rate.sleep()

    def SendCommand(self):
        self.pubCommand.publish(self.command)
        self.rate.sleep()
    
    def SetCommand(self, linear_x, linear_y, linear_z, angular_x, angular_y, angular_z):
        self.command.linear.x = linear_x
        self.command.linear.y = linear_y
        self.command.linear.z = linear_z
        self.command.angular.x = angular_x
        self.command.angular.y = angular_y
        self.command.angular.z = angular_z
        self.SendCommand()

    def cbNavdata(self, msg):
        #print(msg)
        self.navdata = msg
    
    def cbPose(self, msg):
        self.predictPose = msg
        
    def cbOdom(self, msg):
        self.odom = msg
        # if(self.navdata.state == 4 or self.navdata.state == 3):
        #     self.controlAZ(self.pose['w'])
        #     self.controlZ(self.pose['z'])
        #     self.controlY(self.pose['y'])
        #     self.controlX(self.pose['x'])
        #     self.SendCommand()

    def cbMarker(self, msg):
        self.mark = msg
        #print(self.mark)
   
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
    
    def controlAZ(self, ref):
        # self.pid['az'].err = ref - self.navdata.rotZ 
        self.pid['az'].err = self.predictPose.yaw - ref 
        vel = self.pid['az'].get_vel()
        
        if DEBUG:
            print("\nControl Orientation:" + \
                "\nodom_az: " + str(self.predictPose.yaw) + \
                "\nref: " +  str(ref) + \
                "\nerr: " + str(self.pid['az'].err) + \
                "\npid: " + str(vel) 
            )

        self.command.angular.z = self.saturation(vel)
        self.pid['az'].last_err = self.pid['az'].err
        
    def controlZ(self, ref):
        self.pid['z'].err = ref - self.predictPose.z
        vel = self.pid['z'].get_vel()
        
        if DEBUG:
            print("\nControl Altitude:" + \
                "\nodom_z: " + str(self.predictPose.z ) + \
                "\nref: " +  str(ref) + \
                "\nerr: " + str(self.pid['z'].err) + \
                "\npid: " + str(vel) 
            )

        self.command.linear.z = self.saturation(vel)
        self.pid['z'].last_err = self.pid['z'].err
        
    def controlY(self, ref):
        self.pid['y'].err = ref - self.predictPose.y
        vel = self.pid['y'].get_vel()

        if DEBUG:
            print("\nControl Position y:" + \
                "\nodom_y: " + str(self.predictPose.y ) + \
                "\nref: " +  str(ref) + \
                "\nerr: " + str(self.pid['y'].err) + \
                "\npid: " + str(vel) 
            )
        self.command.linear.y = self.saturation(vel)
        self.pid['y'].last_err = self.pid['y'].err
        

    def controlX(self, ref):
        self.pid['x'].err = ref - self.predictPose.x
        vel = self.pid['x'].get_vel()
        
        if DEBUG:
            print("\nControl Position x:" + \
                "\nodom_x: " + str(self.predictPose.x ) + \
                "\nref: " +  str(ref) + \
                "\nerr: " + str(self.pid['x'].err) + \
                "\npid: " + str(vel) 
            )


        self.command.linear.x = self.saturation(vel)
        self.pid['x'].last_err = self.pid['x'].err
        

    def droneTask(self, time_pass):
        
        if time_pass > 6*DELAY:
            self.SetCommand(0,0,0,0,0,0)
            # print("Drone Finish - rotZ: " + str(self.navdata.rotZ))            
        elif time_pass > 5*DELAY:
            self.SetCommand(SPEED,0,0,0,0,0)
            # print("Drone Foward - rotZ: " + str(self.navdata.rotZ))            
        elif time_pass > 4*DELAY:
            self.SetCommand(0,-SPEED,0,0,0,0)
            # print("Drone Right - rotZ: " + str(self.navdata.rotZ))
        elif time_pass > 3*DELAY:
            self.SetCommand(-SPEED,0,0,0,0,0)
            # print("Drone Back - rotZ: " + str(self.navdata.rotZ))
        elif time_pass > 2*DELAY:
            self.SetCommand(0,SPEED,0,0,0,0)
            # print("Drone Left - rotZ: " + str(self.navdata.rotZ))
        elif time_pass > DELAY:
            self.SetCommand(SPEED,0,0,0,0,0)    
            # print("Drone Foward - rotZ: " + str(self.navdata.rotZ))
