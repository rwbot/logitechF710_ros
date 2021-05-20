#!/usr/bin/env python
import rospy, sys, math, time, copy, yaml, subprocess
# from tf_conversions.transformations import quaternion_from_euler
from tf.transformations import *
from geometry_msgs.msg import Pose, Twist
from sensor_msgs.msg import Joy
from std_msgs.msg import Bool, String
inf = 0#float("inf")
class JoyButtonCommander(object):

    def __init__(self):
        rospy.logwarn("Initialized joy_button_commander")
        self.debug = True

        # rospy.on_shutdown(self.shutdown)


        self.activation_pub = rospy.Publisher("pause_navigation", Bool, queue_size=1)
        self.sound_pub = rospy.Publisher('sound_path', String, queue_size=1)

        self.joy_sub = rospy.Subscriber("joy", Joy, self.joy_cb)
        self.activation_sub = rospy.Subscriber("pause_navigation", Bool, self.activation_sub)
        
        self.is_active = False
        self.estop = False
        self.vel_active = False
        self.publish_rate = rospy.Rate(0.69)
        self.axes_msg = list()
        self.buttons_msg = list()
        self.last_msg = rospy.Time.now()

    # def shutdown(self):
    #     # self.pubEStop()
    #     return

    def activation_sub(self,msg):
        self.is_active = msg.data

    def joy_cb(self, msg):
        # Check if there's a change in button states
        # rospy.loginfo_throttle(1, "Joy Callback")
        self.axes_msg = msg.axes
        self.buttons_msg = msg.buttons
        change = sum(self.buttons_msg)
        if change > 0:
            # rospy.loginfo_throttle(1, "Button Pressed")
            elapsed = rospy.Time.now() - self.last_msg
            if elapsed.to_sec() > 1:
                self.read_buttons()
                self.last_msg = rospy.Time.now()
        
    def read_buttons(self):
        rospy.loginfo_throttle(1, "Reading Buttons")
        if self.buttons_msg[2] == 1:
            self.pubEStop()
            # if self.is_active:
            #     subprocess.call('rostopic pub -r 10 /soft_estop_active std_msgs/Bool "data: false"', shell=True)
            #     rospy.loginfo_throttle(1,"publishing FALSE")
            # else:
            #     subprocess.call('rostopic pub -r 10 /soft_estop_active std_msgs/Bool "data: true"', shell=True)
            #     rospy.loginfo_throttle(1,"publishing FALSE")

    def pubEStop(self):
        estop = Bool()
        estop.data = not self.is_active
        rospy.logerr_throttle(1,"Publishing Estop as %s", estop)
        self.activation_pub.publish(estop)
        self.publish_rate.sleep()


    def read_YAML(self):
        stream = open("/home/yukon/shuttle_ws/src/fuse_benchmarking/config/f710_commands.yaml", 'r')
        dictionary = yaml.load(stream)
        # for key, value in dictionary.items():

if __name__ == "__main__":
    rospy.init_node("joy_button_commander")
    
    jbc = JoyButtonCommander()

    while not rospy.is_shutdown():
        rospy.spin()
    # soa.shutdown()