# Kalman Filter implementation using FilterPy
# Reference: https://filterpy.readthedocs.io/en/latest/kalman/KalmanFilter.html

from filterpy.kalman import KalmanFilter
import numpy as np
import time

class IP_KF():
    '''
    Implements a Kalman Filter for pixel coordinates
    '''
    def __init__(self, init_x, init_y):
        '''
        Initializes the system matrix, measurement matrix, covariance matrix and noise matrices
        '''
        
        # System and Measurement model
        # x = [x_postition, x_velocity, y_position, y_velocity] : system states
        # x = [x_postition, y_position] : Measurement states
        
        self.dt = 0.001
        self.F = np.array([                     # system matrix
        [1, self.dt, 0,  0],
        [0,  1, 0,  0],
        [0,  0, 1, self.dt],
        [0,  0, 0,  1]], dtype=np.float)
        
        self.H = np.array([                     # measurement matrix
        [1, 0, 0, 0],
        [0, 0, 1, 0]])

        # self.H = np.array([                     # measurement matrix
        # [1, 0],
        # [0, 1]])
        
        self.Q = 0.9*np.eye(4, dtype=np.float)  # system error matrix
        self.R = np.array([                     # measurement error matrix
        [100, 0],
        [0, 100]], dtype=np.float)
    
        # Kalman filter using filterpy
        
        self.kf = KalmanFilter (dim_x=4, dim_z=2)
        self.kf.x = np.array([[init_x], [0], [init_y], [0]])                         
        self.kf.F = self.F
        self.kf.H = self.H
        self.kf.Q = self.Q
        self.kf.R = self.R
        self.kf.P *= 1000.
        
        self.prev_time = 0
        
    def update(self, x, y):
        '''
        Implements the predict and update steps using the system model and received measurements
        '''
        # self.dt = 0.001
        curr_time = time.time()
        dt = self.prev_time - curr_time
        self.kf.F = np.array([                     # system matrix
        [1, dt, 0,  0],
        [0,  1, 0,  0],
        [0,  0, 1, dt],
        [0,  0, 0,  1]], dtype=np.float)

        
        z = np.array([[x], [y]])
        self.kf.predict()
        self.kf.update(z)
        self.prev_time = curr_time
        return self.kf.x
    
class PP_KF():
    def __init__(self):
        # states: X=(x,y,z,x˙,y˙,z˙,x¨,y¨,z¨,ψ,θ,ϕ,ψ˙,θ˙,ϕ˙,ψ¨,θ¨,ϕ¨)T
        
        dt = 0.001
        dt2 = 0.5*pow(0.001, 2) 
        
        F = [[1, 0, 0, dt,  0,  0, dt2,   0,   0, 0, 0, 0,  0,  0,  0,   0,   0,   0],
            [0, 1, 0,  0, dt,  0,   0, dt2,   0, 0, 0, 0,  0,  0,  0,   0,   0,   0],
            [0, 0, 1,  0,  0, dt,   0,   0, dt2, 0, 0, 0,  0,  0,  0,   0,   0,   0],
            [0, 0, 0,  1,  0,  0,  dt,   0,   0, 0, 0, 0,  0,  0,  0,   0,   0,   0],
            [0, 0, 0,  0,  1,  0,   0,  dt,   0, 0, 0, 0,  0,  0,  0,   0,   0,   0],
            [0, 0, 0, 0,  0,  1,   0,   0,  dt, 0, 0, 0,  0,  0,  0,   0,   0,   0],
            [0, 0, 0,  0,  0,  0,   1,   0,   0, 0, 0, 0,  0,  0,  0,   0,   0,   0],
            [0, 0, 0,  0,  0,  0,   0,   1,   0, 0, 0, 0 , 0,  0,  0,   0,   0,   0],
            [0, 0, 0,  0,  0,  0,   0,   0,   1, 0, 0, 0,  0,  0,  0,   0,   0,   0],
            [0, 0, 0,  0,  0,  0,   0,   0,   0, 1, 0, 0, dt,  0,  0, dt2,   0,   0],
            [0, 0, 0,  0,  0,  0,   0,   0,   0, 0, 1, 0,  0, dt,  0,   0, dt2,   0],
            [0, 0, 0,  0,  0,  0,   0,   0,   0, 0, 0, 1,  0,  0, dt,   0,   0, dt2],
            [0, 0, 0,  0,  0,  0,   0,   0,   0, 0, 0, 0,  1,  0,  0,  dt,   0,   0],
            [0, 0, 0,  0,  0,  0,   0,   0,   0, 0, 0, 0,  0,  1,  0,   0,  dt,   0],
            [0, 0, 0,  0,  0,  0,   0,   0,   0, 0, 0, 0,  0,  0,  1,   0,   0,  dt],
            [0, 0, 0,  0,  0,  0,   0,   0,   0, 0, 0, 0,  0,  0,  0,   1,   0,   0],
            [0, 0, 0, 0,  0,  0,   0,   0,   0, 0, 0, 0,  0,  0,  0,   0,   1,   0],
            [0, 0, 0,  0,  0,  0,   0,   0,   0, 0, 0, 0,  0,  0,  0,   0,   0,   1]]        
        
        H =  [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]]
        
        Q = 0.999*np.eye(18, dtype=np.float)  # system error matrix
        R = 0.999*np.eye(6, dtype=np.float)  # system error matrix

        # Kalman filter using filterpy
        
        self.kf = KalmanFilter (dim_x=18, dim_z=6)
        self.kf.x = np.array([[0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0], [0]])                         
        self.kf.F = np.array(F)
        self.kf.H = np.array(H)
        self.kf.Q = np.array(Q)
        self.kf.R = np.array(R)
        self.kf.P *= 1000.
        
        self.prev_time = 0


    def update(self, x, y, z, roll, pitch, yaw):
        curr_time = time.time()
        dt = self.prev_time - curr_time
        # print(x, y, z, roll, pitch, yaw)
        z = np.array([[x], [y], [z], [roll], [pitch], [yaw]])
        print(z)
        self.kf.predict()
        self.kf.update(z)
        self.prev_time = curr_time
        return self.kf.x
