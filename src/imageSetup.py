#!/usr/bin/env python2
import sys
import subprocess
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

class bashSetUp():
    def __init__(self):
        rospy.init_node("RTSP_Setup")
        self.imageSubscriber = rospy.Subscriber(str(imageTopic), Image, self.imageCallback)
        self.bitrate = rospy.get_param("bitrate")
        self.bridge = CvBridge()
        self.startServer = False
        self.serverStarted = False
    

    def imageCallback(self, msg):
        if(self.startServer == False):
            self.img = self.bridge.imgmsg_to_cv2(msg)
            rospy.set_param("image_width", self.img.shape[1])
            rospy.set_param("image_height", self.img.shape[0])
            self.startServer = True


    def main(self):
        while not rospy.is_shutdown():
            if (self.startServer == True and self.serverStarted==False):
                print("Starting Stream")
                bashCommand = 'rosrun ros_rtsp compressedImageStream.py | ~/catkin_ws/src/ros_camera/src/rtsp_server "fdsrc fd=0 ! queue2 ! videoparse format=i420 height=' + str(rospy.get_param("image_height")) + ' width=' + str(rospy.get_param("image_width")) + ' framerate='+ str(rospy.get_param("fps")) + '/1 ! videoconvert ! x264enc bitrate=' + str(rospy.get_param("bitrate")) + ' ! rtph264pay name=pay0 pt=96"'
                process = subprocess.Popen(bashCommand, shell=True)
                self.serverStarted = True
                
            

if __name__ == "__main__":
    print("Initiating Server Setup")
    sh = bashSetUp()
    sh.main()