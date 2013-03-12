import sys
import numpy as np
import cv2
from cv2 import cv



def match(img, tmpl, threshold=.05, method=cv.CV_TM_SQDIFF_NORMED):
    image = cv2.imread(img)
    template = cv2.imread(tmpl)

    result = cv2.matchTemplate(template, image, method)
    print np.amax(result,axis=None), np.amin(result,axis=None)
    #r_sorted = np.sort(result,axis=None);
    #threshold = r_sorted[number]
    matches = np.where(result<=threshold)
    
    for i in xrange(matches[1].size):
        MPx = matches[1][i]
        MPy = matches[0][i]
        trows,tcols = template.shape[:2]
        cv2.rectangle(image, (MPx,MPy),(MPx+tcols,MPy+trows),(255,0,0),2)
           
    cv2.imshow('output',image)
    cv2.imwrite('output.png',image)
    print 'print any key on the image...'
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    match(sys.argv[1], sys.argv[2])
    
