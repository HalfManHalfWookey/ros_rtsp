#!/usr/bin/env python2
import sys
import subprocess
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage

class bashSetUp():
    def __init__(self):
        rospy.init_node("RTSP_Setup",anonymous=True)
        self.serverStarted = False


    def main(self):
        while not rospy.is_shutdown():  
            if (self.serverStarted==False):
                print("Starting Stream")
                bashCommand = '~/catkin_ws/src/ros_rtsp/src/rtsp_server "rtspsrc location={rtsp_uri} ! queue2 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! x264enc pass=0 quantizer={qvalue} speed-preset={speed} bitrate={bitrate} tune=zerolatency sliced-threads=true ! rtph264pay name=pay0 pt=96" {port} {url}'.format(rtsp_uri=str(rospy.get_param("rtsp_uri")), framerate=str(rospy.get_param("fps")), qvalue=str(rospy.get_param("qvalue")), speed=str(rospy.get_param("speed-preset")), bitrate=str(rospy.get_param("bitrate")), port=str(rospy.get_param("port")), url=str(rospy.get_param("url")))
                process = subprocess.Popen(bashCommand, shell=True)
                self.serverStarted = True
                
            

if __name__ == "__main__":
    print("Initiating Server Setup")
    sh = bashSetUp()
    sh.main()
