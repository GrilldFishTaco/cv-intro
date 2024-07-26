#!/usr/bin/env python3

import cv2
import numpy as np
import matplotlib.pyplot as plt
from dt_apriltags import Detector

class LaneDetection():
    # img = cv2.imread('cool_pool_test.png')
    def __init__(self, img):
        self.img = img

    def detect_lines(self, img, threshhold1=50, threshhold2=150, apertureSize=3, minLineLength=100, maxLineGap=10):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale
        edges = cv2.Canny(gray, threshhold1, threshhold2, apertureSize) # detect edges
        lines = cv2.HoughLinesP(
                        edges,
                        1,
                        np.pi/180,
                        100,
                        minLineLength,
                        maxLineGap,
                ) # detect lines
        print(lines)
        return lines
            
    def draw_lines(self, img, lines, color=(0, 255, 0)):
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), color, 2)
        return img

    def get_slopes_intercepts(self, lines):
        slopes = []
        intercepts = []
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            slopes.append((y2 - y1)/(x2 - x1))
            intercepts.append(x1 - y1 / (slopes[-1]))
        print(slopes)
        print(intercepts)
        return slopes, intercepts
        
    def combine_lines(self, slopes, intercepts):
        combined_lines = [] #contains lists of lines: [slope, intercept]
        for i in range(len(slopes) - 1):
            if abs(abs(slopes[i]) - abs(slopes[i + 1])) <= 3 and abs(intercepts[i] - intercepts[i + 1]) <= 3:
                combined_lines.append([slopes[i], intercepts[i]])
                slopes.pop(i + 1)
                intercepts.pop(i + 1)
                i -= 1
        return combined_lines #[[slope, intercept], [slope, intercept], ...]
            
    def detect_lanes(self, slopes, intercepts):
        combined_lines = self.combine_lines(self, slopes, intercepts)
        lanes = []
        for i in range(len(combined_lines)):
            if abs(abs(combined_lines[i][0]) - abs(combined_lines[i + 1][0])) <= 3:
                lane = [combined_lines[i][0], combined_lines[i][1], combined_lines[i + 1][1]] #slope, intercept1, intercept2
                lanes.append(lane)
        return lanes

    def draw_lanes(img, lanes, color = (0, 255, 0)):
        #lane = [slope, intercept1, intercept2]
        for lane in lanes:
            cv2.line(img, (lane[0], lane[1]), (lane[2], lane[3]), color, 2)
            cv2.line(img, (lane[4], lane[5]), (lane[6], lane[7]), color, 2)
        return img


def main():
    LaneDetection()
    
if __name__ == "__main__":
    main()