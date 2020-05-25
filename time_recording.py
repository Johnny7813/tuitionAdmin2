# -*- coding: utf-8 -*-


####################################################################################
# Author:   Hannes Buchholzer
# purpose:  implement a class that takes care of time recording
#
#
#
####################################################################################


from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
from settings import *
from decimal  import *
import time_recording_dialog
import re
import sys


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


# records
class tRecord(object):
    def __init__(self, trep, tspan):
        self.stimes = []    # list with start times, QDateTime
        self.etimes = []    # list with stop times
        self.msecs  = []    # list of the time spans between start and stop time
        self.lstart = 0     # last timer start, QDateTime
        self.rep    = 0
        self.mspan  = 0
        self.trep   = trep  # how many timer events
        self.tspan  = tspan # fixed time span between timer events
        self.total  = 0     # total time elapsed
        self.size   = 0     # number of start and end times, size of above lists
        self.wtime  = 0     # time worked 
        self.reset()
        
        
        
    # reset all values
    def reset(self):
        self.lstart = QtCore.QDateTime.currentDateTime()
        #self.worked = 0
        self.rep    = 0
        self.size   = 1
        self.mspan  = 0
        self.total  = 0
        self.wtime  = 0
        self.stimes = [ self.lstart ]
        self.etimes = [ self.lstart ]
        self.msecs  = [ 0 ]

    def update(self):
        now = QtCore.QDateTime.currentDateTime()
        
        self.mspan      = self.lstart.msecsTo(now)
        self.rep       += 1
        
        if (self.mspan > (1.5*self.tspan)) and (self.rep < self.trep) :
            self.msecs[-1] += self.tspan
            self.total     += self.tspan
            self.stimes.append( now )
            self.etimes[-1] = self.lstart.addMSecs(self.tspan)
            self.etimes.append( now )
            self.msecs.append( 0 )
            self.size      += 1
        else :    
            self.msecs[-1] += self.mspan
            self.total     += self.mspan
            self.etimes[-1] = now
        
        #reset last start
        self.lstart     = now

            
    def printout(self):
        print("Start times:\t", self.stimes)
        print("End times:\t", self.etimes)
        print("Time spans:\t", self.msecs)
        print("Total elapsed time:\t\t", self.total)





# multiple inheritance
class time_recording(QtCore.QObject):
    def __init__(self, model, desktop, parent=None):
        super().__init__()
        
        self.desktop = desktop
        self.parent  = parent
        self.model   = model
        
        # set settings
        self.active  = settings.time_recording
        tspan        = settings.time_span
        trep         = settings.time_rep
        self.running = False
        
        # lists to administrate the data
        self.trec    = tRecord(trep, tspan)
        
        # start and end time for the timer
        self.start_time   = settings.start_time
        self.end_time     = settings.end_time
        self.past_time    = QtCore.QTime.currentTime()
        self.now_time     = QtCore.QTime.currentTime()
        
        # set up a timer
        self.timer   = QtCore.QTimer()
        self.timer.timeout.connect(self.processor)
        
        self.timer2  = QtCore.QTimer()
        self.timer2.timeout.connect(self.control)
        
        if self.active:
            self.init_timer()
        
    
    
    def init_timer(self):
        self.timer2.start(10000)  # 10 seconds
        self.past_time    = QtCore.QTime.currentTime()
        self.now_time     = QtCore.QTime.currentTime()
        
    
    
    # check to start the timer
    def control(self):
        self.now_time.start()
        print( "Now Time: ", self.now_time)
        print( "Past Time: ", self.past_time)
        diff1  =  self.past_time.msecsTo( self.start_time ) 
        diff2  =  self.now_time.msecsTo( self.start_time ) 
        diff   =  diff1*diff2
        if( diff < 0 ) :
            if  not self.active : 
                print("Time recording started!")
                self.checked.emit(True)
                self.active = True
                self.started(True)
        
        diff1  =  self.past_time.msecsTo( self.end_time ) 
        diff2  =  self.now_time.msecsTo( self.end_time ) 
        diff   =  diff1*diff2
        if( diff < 0 ) :
            if  self.active :  
                print("Time recording interrupted!")
                self.end()
            
        self.past_time.start()
    
    
    # start time measurment
    def start(self):
        self.trec.reset()
        self.timer.start(self.trec.tspan)
        self.lock_tick.emit(True)
        self.running = True
        
    
    
    ## slot for activating time recording
    @QtCore.pyqtSlot(bool)
    def started(self, bval):
        if bval == True:
            self.model.statusBar.showMessage("Time Recording started!", 3000)
            self.start()
            
    
    
    # process timer information
    def processor(self):
        self.trec.update()
        if  self.trec.rep >= self.trec.trep:
            self.end()
        
    
    # record data into the database from self.trec
    def recording(self):
        row  = self.model.time.rowCount()-1
        rrec = self.model.time.record(row)
        
        #self.model.dump_model(6)
        #self.model.dump_record(rrec, "Time Recording record")
        entry       = rrec.value("entry_nr") + 1
        end_time    = rrec.value("stop_time")
        start_date  = rrec.value("start_date")
        start_time  = rrec.value("start_time")
        end_date    = QtCore.QDateTime(start_date, end_time)
        entry_add   = 0
        
        ## calculate partition
        partition   = []
        stotal      = float(sum(self.trec.msecs))
        for i in range(0,self.trec.size):
            partition.append(round(self.trec.msecs[i]/stotal,2))
        #print("Partition:\t", partition)
        
        
        # cycle through the 
        for i in range(0,self.trec.size):
            #print("Wtime:\t", self.trec.wtime)
            if self.trec.wtime == 0:
                continue
            
            dist = end_date.secsTo( self.trec.stimes[i] ) / 60.0
            
            if( dist > settings.time_treshold ):
                print("\nnew record case!\n")
                record      = QtSql.QSqlRecord( rrec );
                record.setValue("entry_nr", entry+entry_add)
            
                val1 = self.trec.stimes[i].date()
                record.setValue("start_date", val1)
            
                val2 = self.trec.stimes[i].time()
                record.setValue("start_time", val2)
            
                val3 = self.trec.etimes[i].time()
                record.setValue("stop_time", val3)
                
                
                val = round(self.trec.wtime*partition[i],2)
                record.setValue("time_span", round(val,2))
            
                self.model.time.insertRecord(-1, record)
                
                entry_add += 1
                
                #set a new end time
                #end_date = QtCore.QDateTime(val1, val3)
            
                
            else :
                print("\nold record case!\n")
                val  = rrec.value("time_span")
                val += round(self.trec.wtime*partition[i],2)
                rrec.setValue("time_span", round(val,2))
                val  = self.trec.etimes[i].time()
                rrec.setValue("stop_time", val)
                
                self.model.time.setRecord(row, rrec)
            # set end time for next round
            end_date = self.trec.etimes[i]
            row  = self.model.time.rowCount()-1
            rrec = self.model.time.record(row)
            
    
    
    
    # finish time stopping cycle
    def end(self):
        self.timer.stop()
        self.running = False
        
        time_rec_dialog = time_recording_dialog.time_recording_Dialog(self.trec, self.desktop, self.parent)
        ret             = time_rec_dialog.exec()
        
        #print("Timer recording stopped. Worked time is:\t", self.trec.wtime)
        #self.trec.printout()
        
        # shall time recording continue?
        if  1 <= ret <= 2:  # no we stop time recording
            self.active = False
            self.lock_tick.emit(False)
            self.checked.emit(False)
            self.model.statusBar.showMessage("Time Recording stopped!", 3000);
        else:               # yes we will continue time recording
            self.active = True
            self.model.statusBar.showMessage("Time Recording continues!", 3000);
        
        # shall we record the worked time that the user has put in?
        if  2 <= ret <= 3:
            self.recording()
        
        if self.active :
            self.start()
    
    
    
    # produce a new time record with generic data     
    def new_time_record(self):
        # get last record
        record  = self.model.time.record(self.model.time.rowCount()-1)
        # set date as today
        today   = QtCore.QDateTime.currentDateTime()
        today_date = today.date()
        today_time = today.time()
        entry_nr   = record.value(0)
        record.setValue(0, entry_nr+1)
        record.setValue(1, today_date)
        record.setValue(2, today_time)
        record.setValue(3, 0)
        record.setValue(4, today_time)
        
        self.model.time.insertRecord(-1, record)
        return record
       
            
            
    
    
    # this signal is now called lock_tick, it locks the tick in the tools menu
    lock_tick   = QtCore.pyqtSignal(bool)
    
    # this signal is now called checked, it checks or unchecks the tick in the tools menu
    checked     = QtCore.pyqtSignal(bool)


