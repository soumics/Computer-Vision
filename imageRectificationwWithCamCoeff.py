import cv2
import glob
import argparse
import math
from numpy import genfromtxt
import matplotlib.pyplot as plt
import numpy as np
import os.path
from scipy import ndimage
import os
import shutil

def imageRectifyWithCamCoeff(cameraMatrix1,distCoeffs1,cameraMatrix2,distCoeffs2,rotationMatrix,transVector,unrectifiedImgFolder,oneUnrectifiedImgNameType):
	left = cv2.imread(unrectifiedImgFolder+oneUnrectifiedImgNameType, cv2.IMREAD_GRAYSCALE)
	#right = cv2.imread('./right/000000.ppm', cv2.IMREAD_GRAYSCALE)

	
	flags = cv2.CALIB_ZERO_DISPARITY
	image_size = left.shape[::-1]

	# print image_size

	R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, image_size, rotationMatrix, transVector, flags = flags, alpha=0)

	P=[]
	P.append(P1)
	P.append(P2)


	fpPoseOut = open('./calib_strass.txt', 'w')
	outtxt = ''
	cnt=0
	for val in P:
	    outtxt = outtxt +'P'+str(cnt)+': '
	    #print val.tolist()
	    for v in val.tolist():
		#print v
		for elem in v:
		   #print elem
		   outtxt = outtxt + '{0:06e}'.format(elem) + ' '
	    outtxt = outtxt + '\n'
	    cnt+=1

	print outtxt

	fpPoseOut.write(outtxt)
	fpPoseOut.close()


	leftmapX, leftmapY = cv2.initUndistortRectifyMap(cameraMatrix1, distCoeffs1, R1, P1, image_size, cv2.CV_32FC1)
	rightmapX, rightmapY = cv2.initUndistortRectifyMap(cameraMatrix2, distCoeffs2, R2, P2, image_size, cv2.CV_32FC1)

	path_left = './gray_rectified_left/'

	if os.path.exists(path_left):
		#shutil.rmtree(path)
		try:
		    #os.rmdir(path)
		    shutil.rmtree(path_left)
		except OSError:
		    print ("Deletion of the directory %s has failed" % path_left)
		else:
		    print ("Successfully deleted the directory %s" % path_left)

	try:
	    os.mkdir(path_left)
	except OSError:
	    print ("Creation of the directory %s has failed" % path_left)
	else:
	    print ("Successfully created the directory %s " % path_left)

	print ("Successfully converted the left camera video to left image sequences.....")

	path_right = './gray_rectified_right/'
	if os.path.exists(path_right):
		#shutil.rmtree(path)
		try:
		    #os.rmdir(path)
		    shutil.rmtree(path_right)
		except OSError:
		    print ("Deletion of the directory %s has failed" % path_right)
		else:
		    print ("Successfully deleted the directory %s" % path_right)

	try:
	    os.mkdir(path_right)
	except OSError:
	    print ("Creation of the directory %s has failed" % path_right)
	else:
	    print ("Successfully created the directory %s " % path_right)

	print ("Successfully converted the left camera video to left image sequences.....")

	files = os.listdir('./left/')

	start=0
	end=len(files)

	for i in range(start,end):
		left_image_path='./left/'+'{0:06d}'.format(i) + '.ppm'
		right_image_path='./right/'+'{0:06d}'.format(i) + '.ppm'

		left = cv2.imread(left_image_path, cv2.IMREAD_GRAYSCALE)
		right = cv2.imread(right_image_path, cv2.IMREAD_GRAYSCALE)

		left_remap = cv2.remap(left, leftmapX, leftmapY, cv2.INTER_LINEAR)
		right_remap = cv2.remap(right, rightmapX, rightmapY, cv2.INTER_LINEAR)

	

		left_image_path=path_left + 'gray-rectified-left-'+'{0:06d}'.format(i) + '.png'
		right_image_path=path_right + 'gray-rectified-right-'+'{0:06d}'.format(i) + '.png'
		print left_image_path
		cv2.imwrite(left_image_path, left_remap) 
		cv2.imwrite(right_image_path, right_remap)



	path_left = './color_rectified_left/'
	if os.path.exists(path_left):
		#shutil.rmtree(path)
		try:
		    #os.rmdir(path)
		    shutil.rmtree(path_left)
		except OSError:
		    print ("Deletion of the directory %s has failed" % path_left)
		else:
		    print ("Successfully deleted the directory %s" % path_left)

	try:
	    os.mkdir(path_left)
	except OSError:
	    print ("Creation of the directory %s has failed" % path_left)
	else:
	    print ("Successfully created the directory %s " % path_left)

	print ("Successfully converted the left camera video to left image sequences.....")

	path_right = './color_rectified_right/'
	if os.path.exists(path_right):
		#shutil.rmtree(path)
		try:
		    #os.rmdir(path)
		    shutil.rmtree(path_right)
		except OSError:
		    print ("Deletion of the directory %s has failed" % path_right)
		else:
		    print ("Successfully deleted the directory %s" % path_right)

	try:
	    os.mkdir(path_right)
	except OSError:
	    print ("Creation of the directory %s has failed" % path_right)
	else:
	    print ("Successfully created the directory %s " % path_right)

	print ("Successfully converted the left camera video to left image sequences.....")



	start=0
	end=len(files)
	for i in range(start,end):
		left_image_path='./left/'+'{0:06d}'.format(i) + '.ppm'
		right_image_path='./right/'+'{0:06d}'.format(i) + '.ppm'

		left = cv2.imread(left_image_path, cv2.IMREAD_UNCHANGED)
		right = cv2.imread(right_image_path, cv2.IMREAD_UNCHANGED)

		left_remap = cv2.remap(left, leftmapX, leftmapY, cv2.INTER_CUBIC)
		right_remap = cv2.remap(right, rightmapX, rightmapY, cv2.INTER_CUBIC)

		left_image_path=path_left + 'color-rectified-left-'+'{0:06d}'.format(i) + '.ppm'
		right_image_path=path_right + 'color-rectified-right-'+'{0:06d}'.format(i) + '.ppm'
		print left_image_path
		cv2.imwrite(left_image_path, left_remap) 
		cv2.imwrite(right_image_path, right_remap)



cameraMatrix1 = np.array([[1913.4392867125, 0, 980.08721981551], [0, 1913.4392867125, 603.53035141012], [0, 0, 1]])
distCoeffs1 = np.array([-0.43204070421352, 0.15583766015601, -0.0015171729318065, -0.00040819162190489, 0.22473732362631, 0, 0, 0])

cameraMatrix2 = np.array([[1907.8378008565, 0, 994.6584648387], [0, 1907.8378008565, 600.66131716102], [0, 0, 1]])
distCoeffs2 = np.array([-0.47300262035912, 0.50911301060951, 0.00020119713118458, -0.0023060822191042, -0.74111747899386, 0, 0, 0])

rotationMatrix = np.array([[0.99879441010511, -0.0026971268273365, 0.049014812553552], [0.0028890114846952, 0.99998843700745, -0.0038444068506452], [-0.049003876942788, 0.0039813764289816, 0.99879065308317]])
transVector = np.array([-1.1141123205391, 0.0010809872604165, 0.019605496554413])
essentialMatrix = np.array([[-0.00010961307139502, -0.019600966039004, 0.0011550514770701], [-0.035013962690261, 0.0043828220215124, 1.1137259319779], [-0.0042983673223768, -1.1140965225069, 0.0042301166495268]])
fundMatrix = np.array([[-3.0026603622514e-11, -5.3693453744262e-09, 3.8754159498257e-06], [-9.591469024393e-09, 1.2005982307868e-09, 0.00059243930531325], [3.5446815873034e-06, -0.00057762865778033, -0.0018738528381383]])

unrectifiedImgFolder='./right/'
oneUnrectifiedImgNameType='000000.ppm'
print unrectifiedImgFolder+oneUnrectifiedImgNameType
imageRectifyWithCamCoeff(cameraMatrix1,distCoeffs1,cameraMatrix2,distCoeffs2,rotationMatrix,transVector,unrectifiedImgFolder,oneUnrectifiedImgNameType)







