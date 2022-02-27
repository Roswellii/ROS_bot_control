#!/usr/bin/env python  
import rospy
from darknet_ros_msgs.msg import BoundingBoxes


def callback(data):
    print data
def listener():
    rospy.init_node('topic_subscriber')
    sub = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, callback)
    print sub

    print type(sub)
    rospy.spin()

if __name__ == '__main__':
    listener()
