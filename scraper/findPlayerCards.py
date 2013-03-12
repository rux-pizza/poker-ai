import sys, argparse
import numpy as np
import cv2
from cv2 import cv


############
SuitTemplates = dict()
for suit in ['h','d','c','s']:
    template = cv2.imread('suits/'+suit+'.png')
    if template==None:
        raise Exception('Template for suit %s not found\n' % suit)

    SuitTemplates[suit] = template

NumTemplates = dict()
for num in xrange(1,13):
    template = cv2.imread('numbers/%d.png' % num)
    if template==None:
        raise Exception('Template for number %d not found\n' % num)

    NumTemplates[num] = template
############


def findPlayerLoc ( table, pseudo ):
    template = cv2.imread('pseudos/'+pseudo+'.png')
    if template==None:
        raise Exception('template file for pseudo %s non found\n' % pseudo)

    corrs = cv2.matchTemplate(template, table, cv.CV_TM_CCORR_NORMED)
    _, max_corr, _, loc = cv2.minMaxLoc(corrs)

    if max_corr < .99:
       raise Exception('template not found (max coor %f)\n' % max_corr)
    
    return loc


def findBestMatch ( canvas, templates ):
    bestCorr = 0
    best = -1

    for (i, template) in templates.items():
        corrs = cv2.matchTemplate(canvas, template, cv.CV_TM_CCORR_NORMED)
        c = corrs.max(axis=None)
        if c > bestCorr:
            bestCorr = c
            best = i

    if bestCorr < .98:
        raise Exception('no best suit found (best coor %f)\n' % bestCorr)

    return best

            
def findPlayerCards ( table, pseudo ):
    ext = 4 # add padding to be more robust

    # get player location
    pLoc = findPlayerLoc(table, pseudo)
    x = pLoc[0]
    y = pLoc[1]

    # boundaries for searching suits and numbers
    s1_x0 = x - ext; s1_x1 = x + 32 + ext; s1_y0 = y - 32 - ext; s1_y1 = y + ext;
    s2_x0 = x + 96 - ext; s2_x1 = x + 96 + 32 + ext; s2_y0 = y - 32 - ext; s2_y1 = y + ext;
    n1_x0 = x - ext; n1_x1 = x + 32 + ext; n1_y0 = y - 64 - ext; n1_y1 = y - 32 + ext;
    n2_x0 = x + 96 - ext; n2_x1 = x + 96 + 32 + ext; n2_y0 = y - 64 - ext; n2_y1 = y - 32 + ext;

    # search
    suit1 = findBestMatch(table[s1_y0:s1_y1, s1_x0:s1_x1, :], SuitTemplates)
    suit2 = findBestMatch(table[s2_y0:s2_y1, s2_x0:s2_x1, :], SuitTemplates)
    num1 = findBestMatch(table[n1_y0:n1_y1, n1_x0:n1_x1, :], NumTemplates)
    num2 = findBestMatch(table[n2_y0:n2_y1, n2_x0:n2_x1, :], NumTemplates)

    return [ (suit1, num1), (suit2, num2) ]
    
    
if __name__ == '__main__':
    table = cv2.imread('table0.png')
    c = findPlayerCards(table, 'm1lo0u')
    print c
