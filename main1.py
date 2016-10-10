#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  hyfn1248
# Created: 2016-05-12 16:00

import requests
import datetime
import time
import os
import sys
import threading

import CLLog as log
import clog

HOME = 'http://live.game.163.com/xylive/live/content.do?liveId=2&stand1=0&stand2=0&hasBarrage=0'

my_log = clog.getLogger()

class RobotThread(threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.robot = robot
    
    def run(self):
        while True:
            print '%s start home_page' % self.robot
            sys.stdout.flush()
            
            start = time.time()

            my_log.start("home_page", uid=self.robot)
            try:
                r = requests.get(HOME, params={})
            except Exception, e:
                r = None
                log.log(self.robot, 'action', 'home_page', 'finish', 'fail', str(e))

            if r and (r.status_code == requests.codes.ok):
                my_log.success("home_page", uid=self.robot)
            else:
                my_log.error("home_page", uid=self.robot)
                if r:
                    log.log(self.robot, 'action', 'home_page', 'finish', 'fail', r.text)

            end = time.time()

            if (end - start) < 1:
                time.sleep(1-(end - start))

def main():
    flag = False
    while True:
        if not flag:
            for i in range(50):
                print 'Robot %d start' % (i)
                sys.stdout.flush()
                robot_name = 'robot'+str(i)
                robot = RobotThread(robot_name)
                robot.setDaemon(True)
                robot.start()

            flag = True
        else:
            time.sleep(60)


if __name__ == '__main__':
    main()