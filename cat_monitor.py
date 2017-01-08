import cv2, time, datetime, dropbox, psutil
import numpy as np

def deltaImages(imgArray):
    d1 = cv2.absdiff(imgArray[2], imgArray[1])
    d2 = cv2.absdiff(imgArray[1], imgArray[0])
    #print np.max(cv2.bitwise_and(d1, d2))
    return cv2.bitwise_and(d1, d2)

def upload2dropbox(file_name, subdir=''):
    client = dropbox.client.DropboxClient('d50Ajk8DloAAAAAAAAAACztbiP6V5T3s6c3yj75ITszctP1nDU4PSQPSt2Lm3eWy')
    f = open (file_name,'rb')
    response = client.put_file('/' + subdir+ file_name, f)
    print 'uploaded: ', response
    f.close()
    return response

i = 0
frames = []
detected = False
cap = cv2.VideoCapture(0)
fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
while True: #detected == False


    if i == 0:
        #_, frame =cap.read()
        frame = cv2.cvtColor(cap.read()[1],cv2.COLOR_RGB2GRAY)
        detect_time_old = ''
    for j in range(0,3):
            frames.append(frame)
    else:
        for j in range(0,3):
            frame = cv2.cvtColor(cap.read()[1],cv2.COLOR_RGB2GRAY)	
            frames[j]=frame
            #cv2.imshow('frame',frame)#fcaprames[0])
            #cv2.imshow('diff',deltaImages(frames))
            time.sleep(0.06)

            
        #If movement detected...
        if np.average(deltaImages(frames)) > 0.8:
            print 'movement detected' + str(datetime.datetime.now())
            print psutil.phymem_usage()
            height , width  =  frames[0].shape
            detected = True
            detect_time = str(datetime.datetime.now())[0:16]

            if not(detect_time == detect_time_old):

                for pic in range(0,3):
                    #for it in range(0,50):
                    #framev = cap.read()[1] #cv2.cvtColor(cap.read()[1],cv2.COLOR_RGB2GRAY)
                    #cv2.imwrite(detect_time + '_pic_' + str(pic+3) + '.png', framev)
                    cv2.imwrite(detect_time + '_pic_' + str(pic) + '.png', frames[pic])

                for pic in range(0,3): #6):
                    file2upload = detect_time + '_pic_' + str(pic) + '.png'
                    upload2dropbox(file2upload,'cat_monitor/')
                detect_time_old = detect_time

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
  	

    
    i+=1
    
cv2.destroyAllWindows()
#video.release()
cap.release()

