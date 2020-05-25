# -*- coding: utf-8 -*-


####################################################################################
# Author:   Hannes Buchholzer
# purpose:  implement a class that takes care of time recording
#
#
#
####################################################################################

#from PyQt4.QtCore import QObject, pyqtSignal
from PyQt5 import QtCore, QtGui, QtSql
from settings import *
import os
import re
import subprocess


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


# pattern for the file names
# private_tuition_s~cycle-1.bak
# private_tuition_s~span-1.bak


# records
class backup_Factory(object):
    def __init__(self, statusBar):
        self.prefix = settings.database
        self.suffix = "ebak"
        self.cycle  = settings.backup_cycle
        self.span   = settings.backup_span
        self.db     = settings.database
        self.active = settings.backup_active
        self.sBar   = statusBar
        
        self.bdir   = QtCore.QDir(settings.backup_dir)
        self.bdir.setFilter(QtCore.QDir.Files)
        self.today  = QtCore.QDate.currentDate()
        
        # set up a timer
        self.timer  = QtCore.QTimer()
        self.timer.timeout.connect(self.execute)
        self.timer.setInterval(settings.backup_time*60000)
        
        if self.active:
            self.start()
            
        
    # start the timer
    def start(self):
        self.timer.start()
        self.active = True
        print("Starting Backups")
        self.sBar.showMessage("Starting Backups!", 3000)
    
    # stop the timer
    def end(self):
        self.timer.stop()
        self.active = False
        print("Stopping Backups")
        self.sBar.showMessage("Stopping Backups!", 3000)
    
    
    def run(self, active):
        if active:
            self.start()
        else:
            self.end()
            
    
    
    # calculate the next cycle number
    def calculate_next_cycle(self):
        cmax     = 0
        pattern  = [self.prefix + "~cycle*." + self.suffix]
        self.bdir.setNameFilters(pattern)
        infoList =  self.bdir.entryInfoList()
        mprog    = re.compile(".*~cycle-([0-9]+)\.")
        lastDate = self.today.addDays((-2)*self.cycle) 
        
        
        for fileInfo in infoList:
            resRe = mprog.match(fileInfo.fileName())
            if resRe == None:
                return -1
            num   = int(resRe.group(1))
            mdate   = fileInfo.lastModified().date()
            if mdate > lastDate:
                lastDate = mdate
                cmax     = num
        
        if lastDate==self.today:
            return cmax
            
        if cmax < self.cycle:
            return cmax+1
        else:
            return 1
        
        
    # calculate the next span number
    def calculate_next_span(self):
        cmax     = 0
        pattern  = [self.prefix + "~span*." + self.suffix]
        self.bdir.setNameFilters(pattern)
        infoList =  self.bdir.entryInfoList()
        mprog    = re.compile(".*~span-([0-9]+)\.")
        lastDate = self.today.addDays((-3)*self.span) 
        
        for fileInfo in infoList:
            resRe = mprog.match(fileInfo.fileName())
            if resRe == None:
                return -1
            num   = int(resRe.group(1))
            mdate   = fileInfo.lastModified().date()
            if mdate > lastDate:
                lastDate = mdate
                cmax     = num
        
        if lastDate==self.today:
            return cmax
        
        rem = self.today.dayOfYear() % self.span
        
        if rem in [0,1]:
            if lastDate.daysTo(self.today) > int(self.span/2*3):
                return cmax+1
        return -1
        
    
    # make backups
    def execute(self):
        next_cycle = self.calculate_next_cycle()
        next_span  = self.calculate_next_span()
        abDir      = self.bdir.absolutePath()+"/"
        
        print("Backup executed!")
        command1   = "mysqldump --socket=/home/hannes/Database/DB/hannes_db.socket  "
        command1  += self.db + " | bzip2 --best > "
        
        password   = "gA$9VAdoF6pAvO2fiR@24*"
        command5   = "mysqldump --socket=/home/hannes/Database/DB/hannes_db.socket  " + self.db
        command5  += " | gpg2 -c --cipher-algo AES256 --compress-algo BZIP2  -z 9 --batch "
        command5  += " --passphrase '{0}' -o '{1}'  - "
        
        if next_cycle > 0 :
                backup_cycle_name   = self.prefix + "~cycle-{0:02d}.".format(next_cycle) + self.suffix 
                fileName            = abDir + backup_cycle_name
                #command             = command1 + fileName
                command             = command5.format(password, fileName)
                
                print("execute cycle command:\t", command)
                #os.lstat(path, *, dir_fd=None)
                if self.bdir.exists(fileName) :
                    os.remove(fileName)
                subprocess.check_call( command, shell=True, timeout=3)
        
        
        if next_span > 0 :
            backup_span_name  = self.prefix + "~span-{0:03d}.".format(next_span) + self.suffix
            fileName          = abDir + backup_span_name
            if next_cycle > 0 :
                command  = "cp -f -u " + abDir + backup_cycle_name
                command += "  " + fileName
                #print("execute span command1:\t", command)
                subprocess.check_call( command, shell=True, timeout=2)
            else :
                #command  = command1 + abDir + backup_span_name
                
                command             = command5.format(password, fileName)
                print("execute span command:\t", command)
                if self.bdir.exists(fileName) :
                    os.remove(fileName)
                subprocess.check_call( command, shell=True, timeout=3)
            
            
        
                
                

        
