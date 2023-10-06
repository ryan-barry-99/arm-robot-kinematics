"""
File: ArmRobot.py

Description:This module defines the ArmRobot class, which represents an arm robot with multiple joints. 
It provides functionality to add links to the arm, move individual joints, update the Denavit-Hartenberg 
(DH) table, and perform forward and inverse kinematics calculations.


Author: Ryan Barry
Date Created: October 5, 2023
"""

from ArmRobotKinematics import PRISMATIC, REVOLUTE, ArmRobotKinematics

class ArmRobot(ArmRobotKinematics):
    def __init__(self):
        super().__init__(self)
        '''
        Additional initialization code specific to the arm robot:
        This is where you will define the configuration of your robot with the addLink method
        '''
        # Add a link called link0 with a revolute joint and length 1 m
        self.link0 = self.addLink(joint_type=REVOLUTE, length=1)
        # Add a prismatic joint with an initial extended length of 1 m
        self.link1 = self.addLink(joint_type=PRISMATIC, length=1)
        pass
         
    def inverse_kinematics(self, target_position, target_orientation):
        # Override the generic inverse kinematics method
        # Implement the specific inverse kinematics calculations for the arm robot
        pass