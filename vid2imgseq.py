import os
import cv2
import shutil

# define the name of the directory to be created
path = './left/'
video_path='video_1.mkv'
img_format='ppm'

if os.path.exists(path):
	#shutil.rmtree(path)
	try:
	    #os.rmdir(path)
	    shutil.rmtree(path)
	except OSError:
	    print ("Deletion of the directory %s has failed" % path)
	else:
	    print ("Successfully deleted the directory %s" % path)

try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s has failed" % path)
else:
    print ("Successfully created the directory %s " % path)

print ("Successfully converted the left camera video to left image sequences.....")

vidcap = cv2.VideoCapture(video_path)
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite(path+'{0:06d}'.format(count)+'.'+img_format, image)     
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1

# define the name of the directory to be created
path = './right/'
video_path='video_2.mkv'

if os.path.exists(path):
	#shutil.rmtree(path)
	try:
	    #os.rmdir(path)
	    shutil.rmtree(path)
	except OSError:
	    print ("Deletion of the directory %s has failed" % path)
	else:
	    print ("Successfully deleted the directory %s" % path)

try:
    os.mkdir(path)
except OSError:
    print ("Creation of the directory %s has failed" % path)
else:
    print ("Successfully created the directory %s " % path)

vidcap = cv2.VideoCapture(video_path)
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite(path+'{0:06d}'.format(count)+'.'+img_format, image)     
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1

print ("Successfully converted the right camera video to right image sequences.....")
