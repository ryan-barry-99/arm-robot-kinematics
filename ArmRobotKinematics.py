"""
File: ArmRobotKinematics.py

This module defines the ArmRobot class, which represents an arm robot with multiple joints.
It provides functionality to add links to the arm, move individual joints, update the
Denavit-Hartenberg (DH) table, and perform forward kinematics to compute the end-effector
position and orientation.

Author: Ryan Barry
Date created: June, 26 2023
"""

import numpy as np  # Importing the NumPy library for mathematical operations

PRISMATIC = 0
REVOLUTE = 1


class ArmRobotKinematics:
    def __init__(self):
        self.num_joints = 0  # Initialize the number of joints to 0
        self.__theta = []  # Private list to store joint angles
        self.__d = []  # Private list to store d parameters
        self.__a = []  # Private list to store a parameters
        self.__alpha = []  # Private list to store alpha parameters
        self.dhTable = None  # Initialize DH table as None

    # Add a link to the arm
    # Parameters:
    #   joint_type:
    #       - REVOLUTE
    #       - PRISMATIC
    #   length (meters)
    def addLink(self, joint_type, length):
        if joint_type is not PRISMATIC or joint_type is not REVOLUTE:
            print(f"Invalid Joint Type for joint {self.num_joints}")
            return
        self.num_joints += 1  # Increment the number of joints
        self.__joint_type.append(joint_type)  # Append the joint type to the private list
        self.__joint_length.append(length)  # Append the joint length to the private list
        self.updateDHTable()  # Update the DH table

    def moveJoint(self, joint, angle_or_distance):
        if joint < self.num_joints:  # Check if the joint number is valid
            if self.__joint_type[joint] == REVOLUTE:  # Check if the joint type is revolute
                self.__theta[joint] = angle_or_distance  # Set the joint angle
            elif self.__joint_type[joint] == PRISMATIC:  # Check if the joint type is prismatic
                self.__d[joint] = angle_or_distance  # Set the d parameter
            else:
                print(
                    f"Invalid joint type at joint {joint}"
                )  # Print an error message for invalid joint type
                return None
            self.updateDHTable()  # Update the DH table
        else:
            print("Invalid Joint Number")  # Print an error message for invalid joint number

    def updateDHTable(self):
        self.__theta = [0] * self.num_joints  # Initialize theta as a list of zeros
        self.__d = [0] * self.num_joints  # Initialize d as a list of zeros
        self.__a = [0] * self.num_joints  # Initialize a as a list of zeros
        self.__alpha = [0] * self.num_joints  # Initialize alpha as a list of zeros

        for i in range(self.num_joints):
            if self.__joint_type[i] == REVOLUTE:  # Check if the joint type is revolute
                self.__a[i] = self.__joint_length[i]  # Set the a parameter
            elif self.__joint_type[i] == PRISMATIC:  # Check if the joint type is prismatic
                self.__d[i] = self.__joint_length[i]  # Set the d parameter
            else:
                print(
                    f"Invalid joint type at joint {i}"
                )  # Print an error message for invalid joint type
                return None

        self.dhTable = np.column_stack(
            (self.__theta, self.__d, self.__a, self.__alpha)
        )  # Create the DH table using NumPy

    def forward_kinematics(self):
        self.__A = []  # Initialize A matrices as empty list
        self.__T = np.identity(4)  # Initialize the transformation matrix as an identity matrix

        for i in range(self.num_joints):
            theta = self.__theta[i]  # Get the joint angle
            d = self.__d[i]  # Get the d parameter
            a = self.__a[i]  # Get the a parameter
            alpha = self.__alpha[i]  # Get the alpha parameter

            if self.__joint_type[i] == REVOLUTE:  # Check if the joint type is revolute
                ct = np.cos(theta)  # Compute the cosine of theta
                st = np.sin(theta)  # Compute the sine of theta
                ca = np.cos(alpha)  # Compute the cosine of alpha
                sa = np.sin(alpha)  # Compute the sine of alpha

                self.__A.append(
                    np.array(
                        [
                            [ct, -st * ca, st * sa, a * ct],  # Create the transformation matrix A
                            [st, ct * ca, -ct * sa, a * st],
                            [0, sa, ca, d],
                            [0, 0, 0, 1],
                        ]
                    )
                )

            elif self.__joint_type[i] == PRISMATIC:  # Check if the joint type is prismatic
                ct = np.cos(theta)  # Compute the cosine of theta
                st = np.sin(theta)  # Compute the sine of theta
                ca = np.cos(alpha)  # Compute the cosine of alpha
                sa = np.sin(alpha)  # Compute the sine of alpha

                self.__A.append(
                    np.array(
                        [
                            [ct, -st * ca, st * sa, ct * d],  # Create the transformation matrix A
                            [st, ct * ca, -ct * sa, st * d],
                            [0, sa, ca, a],
                            [0, 0, 0, 1],
                        ]
                    )
                )
            else:
                print(
                    f"Invalid joint type at joint {i}"
                )  # Print an error message for invalid joint type
                return None

            self.__T = np.dot(self.__T, self.__A[i])  # Multiply the transformation matrix T by A

        return self.__T  # Return the final transformation matrix

    def inverse_kinematics(self, target_position, target_orientation):
        pass
