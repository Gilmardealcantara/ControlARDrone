#!/usr/bin/env python

import rospy
import time


from visualization_msgs.msg import Marker

class ARPoseFilter():
    def __init__(self):
        # rospy.init_node('filter', anonymous=False)
        rospy.Subscriber("/visualization_marker", Marker, self.cbMarker)
        self.pubFilterPose = rospy.Publisher("ar_filter_pose",Marker, queue_size=10)
        self.poses = []
        self.last_pose = None
        
    def cbMarker(self, msg):
        # print(msg.pose.position)
        if self.last_pose :
            if abs(msg.pose.position.x - self.last_pose.x) > 0.5: msg.pose.position.x = self.last_pose.x
            if abs(msg.pose.position.x - self.last_pose.y) > 0.5: msg.pose.position.y = self.last_pose.y
            if abs(msg.pose.position.z - self.last_pose.z) > 0.5: msg.pose.position.z = self.last_pose.z
        
        self.last_pose = msg.pose.position

        self.pubFilterPose.publish(msg)

        return

        # fitro deixa lento
        self.poses.insert(0, msg.pose.position)
        poses_len = len(self.poses)


        if poses_len > 10:
            self.poses.pop()
            msg.pose.position.x =  sum([ ele.x for ele in self.poses])/poses_len 
            msg.pose.position.y =  sum([ ele.y for ele in self.poses])/poses_len 
            msg.pose.position.z =  sum([ ele.z for ele in self.poses])/poses_len 
            
            self.pubFilterPose.publish(msg)
        
    