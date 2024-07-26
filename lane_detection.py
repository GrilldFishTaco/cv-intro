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

    def detect_lanes(self, lines, slopes, intercepts):
        lanes = []
        for i in slopes:
            if abs(slopes[i] - slopes[i + 1]) <= 3 and abs(intercepts[i] - intercepts[i + 1]) <= 3:
                lane = lines[i].append(lines[i + 1]) # lane = [x1, y1, x2, y2, x3, x4, y3, y4] ??
                lanes.append(lane)

        return lanes
    
    def draw_lanes(img, lanes):
        for lane in lanes:
            for line in lane:
                cv2.line(img, (0, 0), (100, 100), (255, 0, 0), 5)
        return img


def main(args=None):
    rclpy.init(args=args)
    lane_detection()
    

if __name__ == "__main__":
    main()