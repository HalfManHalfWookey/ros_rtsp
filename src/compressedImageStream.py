#!/usr/bin/env python2

import sys
import numpy as np
import rospy
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage
from std_msgs.msg import Int64

class CameraSwitch():
    def __init__(self):
        rospy.init_node("RTSP_Server",anonymous=True)
        self.imageSubscriber = rospy.Subscriber(str(rospy.get_param("image_topic")), CompressedImage, self.imageCallback)
        self.bridge = CvBridge()
        self.gst_str = "appsrc ! videoconvert ! video/x-raw, format=I420, width=" + str(rospy.get_param("image_width")) + ", height="+ str(rospy.get_param("image_height")) + ", framerate=30/1 ! fdsink"
        self.out = cv2.VideoWriter(self.gst_str, 0, 30, (rospy.get_param("image_width"), rospy.get_param("image_height")), True)
        self.img = np.zeros((rospy.get_param("image_height"), rospy.get_param("image_width"), 3), np.uint8)

    def imageCallback(self, msg):
        self.img = self.bridge.compressed_imgmsg_to_cv2(msg)
        
    def main(self):
        while not rospy.is_shutdown():
            self.out.write(self.img)
            


if __name__ == "__main__":
    print("Initiating Server Start")
    cs = CameraSwitch()
    cs.main()
