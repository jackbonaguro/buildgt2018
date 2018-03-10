from __future__ import division
import cv2
import numpy as np

objects = []

class Object():
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        
    def __str__(self):
        return "Object[x="+str(self.x)+",y="+str(self.y)+",r="+str(self.r)+"]"
    
    def compare(self, other):
        try:
            #x, y, and r should be within 10% of each other
            if (float(self.x) == 0 or float(other.x) == 0):
                dx = 1
            if (float(self.y) == 0 or float(other.y) == 0):
                dy = 1
            if (float(self.r) == 0 or float(other.r) == 0):
                dr = 1
            
            dx = float(self.x) / float(other.x)
            dy = float(self.y) / float(other.y)
            dr = float(self.r) / float(other.r)

            xt = (dx > .9 and dx < 1.1)
            yt = (dy > .9 and dy < 1.1)
            rt = (dr > .9 and dr < 1.1)

            return xt and yt and rt
        except ZeroDivisionError:
            return true
        

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    """#ret,thresh = cv2.threshold(gray,127,255,0)
    #im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    img_filt = cv2.medianBlur(gray, 5)
    img_th = cv2.adaptiveThreshold(img_filt,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    im2, contours, hierarchy = cv2.findContours(img_th, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(gray, contours, -1, (0,255,0), 3)
    cv2.circle(gray,(447,63), 63, (0,0,255), -1)
    
    # Display the resulting frame"""
    img_filt = cv2.medianBlur(frame, 33)

    ret, threshed_img = cv2.threshold(cv2.cvtColor(img_filt, cv2.COLOR_BGR2GRAY),
                127, 255, cv2.THRESH_BINARY)

    #img_filt = cv2.medianBlur(threshed_img, 33)
    
    # find contours and get the external one
    image, contours, hier = cv2.findContours(threshed_img, cv2.RETR_TREE,
                    cv2.CHAIN_APPROX_SIMPLE)
     
    # with each contour, draw boundingRect in green
    # a minAreaRect in red and
    # a minEnclosingCircle in blue
    newobjects = []
    for c in contours:
        # get the bounding rect
        x, y, w, h = cv2.boundingRect(c)
        # draw a green rectangle to visualize the bounding rect
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
     
        # get the min area rect
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        # convert all coordinates floating point values to int
        box = np.int0(box)
        # draw a red 'nghien' rectangle
        cv2.drawContours(frame, [box], 0, (0, 0, 255))
     
        # finally, get the min enclosing circle
        (x, y), radius = cv2.minEnclosingCircle(c)
        # convert all values to int
        center = (int(x), int(y))
        radius = int(radius)
        # and draw the circle in blue
        img = cv2.circle(frame, center, radius, (255, 0, 0), 2)

        """thisobj = None
        #thisindex = None
        
        for i in range(len(objects)):
            if objects[i].compare(Object(x, y, w)):
                thisobj = objects[i]
                #thisindex = i
                break
        if thisobj is  None:
            thisobj = Object(x, y, w)
        newobjects.append(thisobj)
        #thisindex = len(newobjects
        cv2.putText(frame,str(thisobj),(int(x),int(y)),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,.5,(225,255,255))
        cv2.putText(frame,str(len(newobjects)-1),(int(x),int(y)+10),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,1.0,(225,255,255))
        
    objects = newobjects"""
        
            

    console = threshed_img
    #cv2.rectangle(frame, (0,0), (console.width, console.height), (0,0,0), 2)
    #wh,ww = vis.shape
    #vis2 = cv2.CreateMat(wh, ww, cv.CV_32FC3)
    #console = #cv2.fromarray(vis)
    cv2.putText(console,"Objects:"+str(len(objects)),(10,20),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,.5,(225,255,255))
    for i in range(len(objects)):
        output = str(objects[i]) + "\n"
        cv2.putText(console, output,(10, 20+(i*10)),
                cv2.FONT_HERSHEY_COMPLEX_SMALL,.5,(225,255,255))
    
    cv2.imshow('console',console)
    cv2.imshow("blur", img_filt)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
