#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 13:39:17 2019

@author: ee904-itri-white
"""

import matplotlib.pyplot as plt
import csv
import numpy as np
import math

def curve_fit(hypo_inliers):
    p1 = hypo_inliers[0]
    p2 = hypo_inliers[1]
    p3 = hypo_inliers[2]

    m = np.array([p1[0]*p1[0], p1[0], 1])
    m = np.row_stack((m, np.array([p2[0]*p2[0], p2[0], 1])))
    m = np.row_stack((m, np.array([p3[0]*p3[0], p3[0], 1])))
    y = np.array([[p1[1]], [p2[1]], [p3[1]]])
    
    print(m)
    print(m.shape)
    print(y)
    print(y.shape)
    params = np.dot(np.linalg.inv(m), y)
    print(params.shape)
    return params

def point_to_curve(curve_params, point):
    y = point[1]
    y_ = curve_params[0]*point[0]*point[0] + curve_params[1]*point[0] + curve_params[2]

    return math.fabs(y-y_)
    
def alsoInliers(data_in, plane_params, threshold):
    count = 0
    alsoinliers = np.array([])
    for i in range(0, data_in.shape[0]):
        dis = point_to_curve(plane_params, data_in[i])
        if (dis < threshold):
            if count == 0:
                alsoinliers = i
            else:
                alsoinliers = np.append(alsoinliers, i)
            count = count + 1

    return alsoinliers;

def downsample(data, distance):
    new_data = np.array([])
    for i in range(0, data.shape[0]):
        if i == 0:
            new_data = data[i]
        else:
            available = True
            for j in range(0, new_data.shape[0]):
                if np.linalg.norm(data[i]-new_data[j]) < distance:
                    available = False
            if available == True:
                new_data = np.row_stack((new_data, data[i]))
    return new_data

if __name__=='__main__':
    #read data
    file = open('test1.csv', 'r')
    csvCursor = csv.reader(file)
    i = 0    
    for row in csvCursor:
        if i==1:
            row = [float(x) for x in row[0:6]]
            A1 = np.array(row[0:6])
        elif i>1:
            row = [float(x) for x in row[0:6]]
            A1 = np.row_stack((A1, row))
        i=i+1
    file.close()

    
    data_in = A1[:,1];
    data_in = np.column_stack((data_in, A1[:,5]))

    data_in = downsample(data_in, 0.1)

    # parameters
    max_iterations = 100
    threshold = 0.3
    fit_prob = 0.99
    max_count = 0
    inliers = data_in
    max_curve = np.zeros((3,1))

    for i in range(0, max_iterations):
        choice = np.random.choice(data_in.shape[0],3,replace=False)
        hypo_inliers = data_in[choice]
        curve_params = curve_fit(hypo_inliers)
        temp_inliers = alsoInliers(data_in, curve_params, threshold)
        if temp_inliers.shape[0] > max_count:
            max_count = temp_inliers.shape[0]
            max_curve = curve_params
            inliers = temp_inliers
        if (inliers.shape[0]/data_in.shape[0] > fit_prob):
            break
    idx = 0
    for i in range(0, data_in.shape[0]):
        row = data_in[i]
        if idx < inliers.shape[0] and inliers[idx] == i:
            idx = idx + 1
            row = np.append(row, 1)
        else:
            row = np.append(row, 0)
        if i == 0:
            res = row
        else:
            res = np.row_stack((res, row))
    print("inliers/all = " + str(inliers.shape[0]) + "/" + str(data_in.shape[0]))
    
    x_c = np.linspace(-45,45,100)
    y_c = np.array(max_curve[0] * np.multiply(x_c, x_c) + max_curve[1] * x_c + max_curve[2])

    plt.figure()
    
    plt.scatter(A1[:,1], A1[:,5], marker='o', c = A1[:,0])
    
    plt.xlabel('theta')
    plt.ylabel('velocity')
    plt.axis('equal')
    plt.title("Result of pcl ransac")
    plt.show()
    

    plt.figure()
    
    plt.scatter(res[:,0], res[:,1], marker='o', c = res[:,2])
    plt.plot(x_c, y_c, c = 'red')
    
    plt.xlabel('theta')
    plt.ylabel('velocity')
    plt.axis('equal')
    plt.title("Result of our ransac")
    plt.xlim(-45,45)
    plt.show()