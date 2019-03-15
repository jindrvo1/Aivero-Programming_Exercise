#!/usr/bin/env python

import rospy
from std_msgs.msg import Int64
from programming_exercise.msg import Solution
import numpy as np

class Numbers():
	# Create an array with the size of the window
	def __init__(self, size):
		self.nums = np.zeros(size)

	# Append a new number to the end of the array and delete the first number to maintain correct length
	def add_num(self, num):
		self.nums = np.append(self.nums[1:], num)

	# Find the max in the array
	# Conversion to int is done because numpy integer data types are not instances of Python's int
	def get_max(self):
		return int(np.max(self.nums))

def callback(data, args):
	# Convert received number to int
	received = int(data.data)

	# Object storing the numbers
	numbers = args[0]
	
	# Publisher
	pub = args[1]

	# Add received number to the array
	numbers.add_num(received)
	
	# Publish maximum to the topic 'verify' alongside with the actual data point
	pub.publish(solution=numbers.get_max(), input=data.data)

def listener():
	# Size of the window
	N_NUMBERS = 1000

	# Object storing the numbers
	nums = Numbers(N_NUMBERS)

	# Publisher to 'verify'
	pub = rospy.Publisher('verify', Solution, queue_size=10)

	rospy.init_node('listener', anonymous=True)

	rospy.Subscriber('numbers', Int64, callback, (nums, pub))

	rospy.spin()

if __name__ == '__main__':
	listener()