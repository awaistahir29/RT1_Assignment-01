from __future__ import print_function
import time
from sr.robot import *

"""
Assignment 1 python script
The main code is after the defination of the function.

"""

threshold_silver = 0.4
"""float: Threshhold to maintain the distance between the robot and the silver token"""    

threshold_gold = 0.75
"""float: Threshhold to maintain the appropriate distance between the robot and the golden token"""   

a_th = 10.0
""" float: Threshold for the control of the orientation of the robot """

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
  	
def find_golden_token():
	"""
	Function to find the closest token

	Returns:
	g_dist (float): distance of the closest token (-1 if no token is detected)
	golden_rot_y (float): angle between the robot and the token (-1 if no token is detected)
	"""
	g_dist=100
	for token in R.see():
		if token.dist < g_dist and token.info.marker_type is MARKER_TOKEN_GOLD:
		   g_dist=token.dist
		   golden_rot_y=token.rot_y
		   
	if g_dist==100:
		return -1, -1
	else:
		return g_dist, golden_rot_y
		
def find_silver_token():
	"""
	Function to find the closest token

	Returns:
	s_dist (float): distance of the silver token (-1 if no token is detected)
	silver_rot_y (float): angle between the robot and the silver token (-1 if no token is detected)
	"""
	s_dist=100
	for token in R.see():
		if token.dist < s_dist and token.info.marker_type is MARKER_TOKEN_SILVER and -120 <token.rot_y < 120:
		   s_dist=token.dist
		   silver_rot_y=token.rot_y
		   
	if s_dist==100:
		return -1, -1
	else:
		return s_dist, silver_rot_y
   	
def wall():
	"""
	Function to turn the robot if wall(golden token) detected

	Turn right if wall detected on the left side of the robot 
	Turn Left if wall detected on the right side of the robot
	"""
	print("Wall Detected!")
	if golden_rot_y > 0: 
	   print("Left a bit")
	   drive(-7.5, 1)	   
	   turn(-5, 1.0)
	   drive(10, 2)
	else: 
	   print("Right a bit")
	   drive(-7.5, 1)
	   turn(+5, 1.0)
	   drive(10,2)

def target():
	"""
	Function to grab the silver token
	Put it behind and move forward
	"""
	print("Found it!")
        R.grab() # if we are close to the token, we grab it.
        print("Gotcha!")
        turn(+15, 4.0)
        R.release()
        turn(+0, 2.0)
        drive(-10, 2.0)
        turn(-15, 4.0)
        drive(15, 2.5)
        #Grabbing the box, turning clockwise direction, leaving the box, going backward , turning counter-clockwise direction,and moving forward
	
#here goes the code


while 1:
    s_dist, silver_rot_y=find_silver_token() #Here we have the distance and angle of the silver token 
    g_dist, golden_rot_y=find_golden_token() #Here we have the distance and angle of the golden token
    if s_dist==-1: 
        print("I don't see any token!!")
	exit()  # if silver markers is not detected, the program ends
    elif g_dist==-1: 
        print("I don't see any token!!")
	exit()  # If golden markers is not detected, the program ends
    elif s_dist < threshold_silver:  
	target() #If silver token is in the range of the robot, it will grab it and place it at the back of it. Thereafter it will move forward 
    elif g_dist < threshold_gold:# If the wall(golden token) is too closed to the robot, the robot will move back and change its path
    	wall() 
    elif -a_th <= silver_rot_y <= a_th: # if the robot is well aligned with the silver token, we go forward
        print("Ah, here we are!.")
        drive(20, 0.5)#going straight to the box
    elif silver_rot_y < -a_th: # if the robot is not well aligned with the silver token, we move it on the left or on the right
        print("Left a bit...")
        turn(-10, 0.1)
        drive(10, 0.4)
    elif silver_rot_y > a_th:
        print("Right a bit...")
        turn(+10, 0.1)
        drive(10, 0.4)


