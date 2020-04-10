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
from mpl_toolkits.mplot3d import Axes3D

def plane_fit(hypo_inliers):
    A = hypo_inliers[0]
    B = hypo_inliers[1]
    C = hypo_inliers[2]

    AB = B - A
    AC = C - A
    normal = np.cross(AB, AC)
    d = - (normal[0]*A[0] + normal[1]*A[1] + normal[2]*A[2])

    params = np.append(normal,d)

    return params

def point_to_plane(plane_params, point):
    nu = math.fabs(plane_params[0]*point[0]+plane_params[1]*point[1]+plane_params[2]*point[2]+plane_params[3])
    de = np.linalg.norm(plane_params[:3])
    return nu/de
    
def alsoInliers(data_in, plane_params, threshold):
    count = 0
    alsoinliers = np.array([])
    for i in range(0, data_in.shape[0]):
        dis = point_to_plane(plane_params, data_in[i])
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
    file = open('test_plane.csv', 'r')
    csvCursor = csv.reader(file)
    i = 0    
    for row in csvCursor:
        if i==1:
            row = [float(x) for x in row[0:3]]
            A1 = np.array(row[0:3])
        elif i>1:
            row = [float(x) for x in row[0:3]]
            A1 = np.row_stack((A1, row))
        i=i+1
    file.close()

    # In this test data, it would be easier to fit the desire plane if normalize the raw data
    normalize_1 = (A1[:,0] - np.mean(A1[:,0]))/np.std(A1[:,0])
    normalize_2 = (A1[:,1] - np.mean(A1[:,1]))/np.std(A1[:,1])
    normalize_3 = (A1[:,2] - np.mean(A1[:,2]))/np.std(A1[:,2])
    
    data_in = normalize_1;
    data_in = np.column_stack((data_in, normalize_2))
    data_in = np.column_stack((data_in, normalize_3))

#    data_in = downsample(data_in, 0.1)

    # parameters
    max_iterations = 1000
    threshold = 0.2
    fit_prob = 0.99
    max_count = 0
    inliers = data_in

    for i in range(0, max_iterations):
        choice = np.random.choice(data_in.shape[0],3,replace=False)
        hypo_inliers = data_in[choice]
        plane_params = plane_fit(hypo_inliers)

        temp_inliers = alsoInliers(data_in, plane_params, threshold)

        if temp_inliers.shape[0] > max_count:
            max_count = temp_inliers.shape[0]
            inliers = temp_inliers
            best_plane = plane_params
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
        
    x = np.linspace(res[:,0].min(), res[:,0].max(), 30)
    y = np.linspace(res[:,1].min(), res[:,1].max(), 30)
    xx, yy = np.meshgrid(x, y)
    z = (-best_plane[0] * xx - best_plane[1] * yy - best_plane[3]) * 1. /best_plane[2]

    plt3d = plt.figure().gca(projection='3d')
    plt3d.plot_surface(xx, yy, z, alpha=0.2)

    ax = plt.gca()
    ax.set_aspect('equal')
    ax.scatter(res[:,0], res[:,1], res[:,2], marker='o', c = res[:,3])


    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.title("Result of ransac")



    plt.show()