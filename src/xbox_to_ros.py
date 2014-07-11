#!/usr/bin/env python

import pygame, sys, time
from pygame.locals import *

import numpy as np
#from sensor_msgs.msg import Joy
import rospy
import roscopter.msg, roscopter.srv

rospy.init_node('xbox_control')
pub_rc = rospy.Publisher('send_rc', roscopter.msg.RC)

pygame.init()
print pygame.joystick.get_count()
joy = pygame.joystick.Joystick(0)
joy.init()

#Stick axes numbers
# left horizontal	0
# left vertical		1
# left trigger		2
# right horizontal	3
# right vertical	4
# right trigger		5

#Button numbers
# right shoulder	5
# back				6
# start				7

# WAIT TO LET ARDUCOPTER CONNECT - SHOULD BE SMART WITH SUBSCRIBER
time.sleep(10)

r = rospy.Rate(10)
while not rospy.is_shutdown():
	call_cmd = rospy.ServiceProxy('command', roscopter.srv.APMCommand)

	for event in pygame.event.get():

		#Get button values
		altitude = joy.get_button(0)
		loiter = joy.get_button(1)
		land = joy.get_button(2)
		launch = joy.get_button(3)
		stabilize = joy.get_button(4)
		dead_man = joy.get_button(5)
		disarm = joy.get_button(6)
		arm = joy.get_button(7)

		if dead_man:
			#Get stick values
			throttle = joy.get_axis(1) * -1 * 400 + 1500
			yaw = joy.get_axis(0) * 500 + 1500
			pitch = joy.get_axis(4) * -1 * 500 + 1500
			roll = joy.get_axis(3) * 500 + 1500

			#Publish RC commands
			vals = [roll, pitch, throttle, yaw, 0, 0, 0, 0]
			pub_rc.publish(vals)
		else:
			call_cmd(12)
			#MAKE SO THIS DOESN'T ALWAYS CALL CMD
			
			
			# vals = [0, 0, 0, 0, 0, 0, 0, 0]
			# pub_rc.publish(vals)
			# vals = [-1, -1, -1, -1, -1, -1, -1, -1]
			# pub_rc.publish(vals)
			# print "You must hold down the right bumper to send RC commands."

		#Publish button commands
		if stabilize:
			call_cmd(7)
		elif altitude:
			call_cmd(8)
		elif loiter:
			call_cmd(10)
		elif disarm:
			call_cmd(4)
		elif land:
			call_cmd(2)
		
		if not disarm:
			if arm:
				call_cmd(3)
	r.sleep()
