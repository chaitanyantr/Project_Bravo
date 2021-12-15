# Plots the pose of the camera with respect to Rubik's cube
# Reference: https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.html

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import time
from math import sin, cos

from numpy.lib.polynomial import roots

class Plotter():
    def __init__(self):
        '''
        Initializes 3D plotter
        '''
        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')
        
        self.x_buff = []
        self.y_buff = []
        self.z_buff = []
        self.buffer_len = 1

    def update(self, x, y, z, roll, pitch, yaw):
        '''
        Save the updated values in a buffer and plot the pose, camera frame and world frame in a 3D graph
        '''
        print(x, y, z, roll, pitch, yaw)
        self.ax.quiver([0],[0],[0],[1],[0],[0], colors='b')
        self.ax.quiver([0],[0],[0],[0],[1],[0], colors='r')
        self.ax.quiver([0],[0],[0],[0],[0],[-1], colors='g')
        
        self.ax.set_xlim((-5, 1))
        self.ax.set_ylim((-6, 0))
        self.ax.set_zlim((-5, 1))
        
        if len(self.x_buff) > 25:
            self.x_buff.pop(0)
            self.y_buff.pop(0)
            self.z_buff.pop(0)

        self.x_buff.append(-x)
        self.y_buff.append(-z)
        self.z_buff.append(y)
        
        # rot = np.array([[cos(yaw)*cos(pitch), -cos(yaw)*sin(pitch)*sin(roll)-sin(yaw)*cos(roll), -cos(yaw)*sin(pitch)*cos(roll)+sin(yaw)*sin(roll)],
        #                 [sin(yaw)*cos(pitch), -sin(yaw)*sin(pitch)*sin(roll)+cos(yaw)*cos(roll), -sin(yaw)*sin(pitch)*cos(roll)-cos(yaw)*sin(roll)],
        #                 [sin(pitch),          cos(pitch)*sin(roll),                            cos(pitch)*sin(roll)]])        

        rot = np.array([[cos(yaw)*cos(pitch), cos(yaw)*sin(pitch)*sin(roll)-sin(yaw)*cos(roll), cos(yaw)*sin(pitch)*cos(roll)+sin(yaw)*sin(roll)],
                        [sin(yaw)*cos(pitch), sin(yaw)*sin(pitch)*sin(roll)+cos(yaw)*cos(roll), sin(yaw)*sin(pitch)*cos(roll)-cos(yaw)*sin(roll)],
                        [-sin(pitch),         cos(pitch)*sin(roll),                             cos(pitch)*sin(roll)]])        

        rot_x = np.dot(rot, np.array([[1], [0], [0]]))
        rot_y = np.dot(rot, np.array([[0], [1], [0]]))
        rot_z = np.dot(rot, np.array([[0], [0], [1]]))

        rot_x = rot_x/sum(abs(rot_x))
        rot_y = rot_y/sum(abs(rot_y))
        rot_z = rot_z/sum(abs(rot_z))

        self.ax.quiver([-x],[-z],[y],[rot_x[0]],[rot_x[2]],[rot_x[1]], colors='b')
        self.ax.quiver([-x],[-z],[y],[rot_z[0]],[rot_z[2]],[rot_z[1]], colors='r')
        self.ax.quiver([-x],[-z],[y],[-rot_y[0]],[-rot_y[2]],[-rot_y[1]], colors='g')    
        
        self.ax.plot3D(self.x_buff, self.y_buff, self.z_buff, 'gray')

        plt.pause(0.05)
        self.ax.clear()
    
    def update_scatter(self, x, y, z):
        self.ax.scatter3D(x, y, z, cmap='Greens');
        plt.pause(0.05)

    def update_frame(self):
        pass

if __name__ == "__main__":
    plotter = Plotter()
    for i in range(100):
        plotter.update(-i, -i, -i)
    time.sleep(0.01)
