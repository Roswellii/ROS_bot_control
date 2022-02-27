#!/usr/bin/env python  
import rospy
from darknet_ros_msgs.msg import BoundingBoxes
from geometry_msgs.msg import Twist
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalID
from geometry_msgs.msg import PoseWithCovarianceStamped,PoseStamped


global stop 
def PoseCallBack(data):
    print 2
    global stop
    if stop==1:
        # obtain current pose from node "amcl"
        x = data.pose.pose.position.x
        y = data.pose.pose.position.y
        orien_z = data.pose.pose.orientation.z
        orien_w = data.pose.pose.orientation.w
        # new goal is made from current pose to make the bot stop
        client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        client.wait_for_server()
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x  # set target location. 
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.orientation.w = 1.0  # set orientation. orientation.w== 1 means face x+
        msg = "bot stops at: "+ str(x) + "," + str(y)+ "," + str(orien_z)+ "," + str(orien_w)
        print msg
        # this loop ensures the bot stop. 
        #TODO: however, how to make the bot continue patrol? 
        while(1):
            client.send_goal(goal) # send target 
       
        stop= 0

def callback(data):
    print 1
    # print data.bounding_boxes[0].Class
    result= data.bounding_boxes[0].Class
    if result == 'stop sign':
        print "stop sign detected!"
        global stop
        stop= 1
        result
    
    #     
    #     # pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    #     # desired_velocity = Twist()
    #     # desired_velocity.linear.x = 0
    #     # desired_velocity.linear.y = 0
    #     # desired_velocity.angular.z = 0
    #     # pub.publish(desired_velocity)
    #     sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, PoseCallBack)
    #     print "bot stop!"
       

def listener():
    rospy.init_node('yolo2move')
    sub_dect = rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, callback)
    sub_stop = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, PoseCallBack)
    rospy.spin()

if __name__ == '__main__':
    stop= 0
    print "em-stop controller starts!"
    listener()