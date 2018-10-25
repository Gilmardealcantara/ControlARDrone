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
from PID import PID

#import class status untuk menentukan status ddari quadcopter
# from drone_status import DroneStatus

DEBUG = True

COMMAND_PERIOD = 1000

MAX_SPEED = 1
SPEED = 0.05*MAX_SPEED
DELAY = 2
# tempo de amostragem
T = 100

class FollowTarget():
    def __init__(self):
        # rospy.init_node('forward', anonymous=False)
        rospy.Subscriber("/ardrone/navdata", Navdata, self.cbNavdata)
        rospy.Subscriber("/ardrone/odometry", Odometry, self.cbOdom)
        # rospy.Subscriber("/ground_truth/state", Odometry, self.cbOdom)
        # rospy.Subscriber("/visualization_marker", Marker, self.cbMarker)
        rospy.Subscriber("/ar_filter_pose", Marker, self.cbMarker)
        self.navdata = Navdata()
        self.odom = Odometry()
        self.mark = Marker()
        self.rate = rospy.Rate(100)
        self.pubTakeoff = rospy.Publisher("ardrone/takeoff",Empty, queue_size=10)
        self.pubLand = rospy.Publisher("ardrone/land",Empty, queue_size=10)
        self.pubLand = rospy.Publisher("ardrone/land",Empty, queue_size=10)
        self.pubCommand = rospy.Publisher('cmd_vel',Twist, queue_size=1)

        self.command = Twist()
        #self.pid = {
        #    'az': PID(T * 0.001, (1.0/360.0), 0, 0, "Orientation"),
        #    'z': PID(T * 0.001, 0.20000000000, 0.0, 0.00000, "Altitude"), # 5
        #    'x': PID(T * 0.001, 0.20000000000, 0.0, 0.00000, "X Position"), # 2
        #    'y': PID(T * 0.001, 0.50000000000, 0.0, 0.00000, "Y Position") # 5
        #}

        self.pid = {
            # 'az': PID(T * 0.001, (1.0/180.0), 0, 0, "Orientation"),
            'az': PID(T/1000.0, 2.0, 0.0, 1.0, "Orientation"),
            'z':  PID(T/1000.0, 2.0, 0.0, 1.0, "Altitude"),
            'x':  PID(T/1000.0, 0.007, 0.000, 0.001, "X Position"),
            'y':  PID(T/1000.0, 0.007, 0.000, 0.001, "Y Position")
        }
        
        #self.commandTimer = rospy.Timer(rospy.Duration(COMMAND_PERIOD/1000.0),self.SetCommand)
        self.state_change_time = rospy.Time.now()
        self.last_stamp = time.time()
        rospy.on_shutdown(self.SendLand)

    def SendTakeOff(self):
        self.pubTakeoff.publish(Empty())
        self.rate.sleep()

    def SendLand(self):
        self.pubLand.publish(Empty())

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
    
    def cbOdom(self, msg):
        #print(msg)
        self.odom = msg

    def cbMarker(self, msg):
        self.mark = msg
        # now = time.time()
        # print(now - self.last_stamp)
        # self.last_stamp = now
        # print(msg.pose.position.x)
        # self.controlAZ(0.0)
        # self.controlDistance(0.30000000000)
        # self.controlZ(0.00000000000) # set point com relacao a y do alvo
        #self.controlWith(0.00000000000) # set point con relacao a x do alvo
        #self.SendCommand()


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
        self.printMark()
        print
        pass

    def saturation(self, vel):
        if vel > SPEED: return SPEED
        elif vel < -SPEED: return -SPEED
        return vel

    def controlAZ(self, ref):
        self.pid['az'].err = ref - self.navdata.rotZ
        vel = self.pid['az'].get_vel()
        
        if DEBUG:
            print("\nControl Orientation:" + \
                "\nrotZ: " + str(self.navdata.rotZ) + \
                "\nref: " +  str(ref) + \
                "\nerr: " + str(self.pid['az'].err) + \
                "\npid: " + str(vel) 
            )

        # if vel > 1 : vel = -1
        # if vel < -1 : vel = 1
            
        self.command.angular.z = self.saturation(vel)
        self.pid['az'].last_err = self.pid['az'].err
        
    def controlZ(self, ref):
        self.pid['z'].err = ref - self.mark.pose.position.y
        vel = self.pid['z'].get_vel()
        
        if DEBUG:
            print("\nControl Altitude z:" +
                "\nmark_y : " + str(self.mark.pose.position.y) +
                "\nref: " +  str(ref) +
                "\nerr: " + str(self.pid['z'].err) +
                "\npid vel: " + str(vel) + "\nmax_vel: " + str(SPEED) 
            )

        self.command.linear.z = self.saturation(vel)
        self.pid['z'].last_err = self.pid['z'].err

    def controlWith(self, ref):
        mark_x = self.mark.pose.position.x
        self.pid['y'].err = ref - mark_x
        vel = self.pid['y'].get_vel()
        
        if DEBUG:
            print("\nControl Lateral y:" +
                "\nmark_x : " + str(mark_x) +
                "\nref: " +  str(ref) +
                "\nerr: " + str(self.pid['y'].err) +
                "\npid vel: " + str(vel) + "\nmax_vel: " + str(SPEED) 
            )

        self.command.linear.y = self.saturation(vel)
        self.pid['y'].last_err = self.pid['y'].err 

    def controlDistance(self, ref):
        mark_z = self.mark.pose.position.z
        self.pid['x'].err = mark_z - ref
        vel = self.pid['x'].get_vel()
        
        if DEBUG:
            print("\nControl Distance x:" +
                "\nmark_z : " + str(mark_z) +
                "\nref: " +  str(ref) +
                "\nerr: " + str(self.pid['x'].err) +
                "\npid vel: " + str(vel) + "\nmax_vel: " + str(SPEED) 
            )

        self.command.linear.x = self.saturation(vel)
        self.pid['x'].last_err = self.pid['x'].err 
