# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
from PyQt5.QtCore   import QObject, pyqtSignal, pyqtSlot
from HSqlTableModel import *
from settings       import *
import re
import sys

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



## this class mainly serves as a container for the model classes
## and so that I can call them by reference
### order: invoice, tuition, mileage, student_info, student_counter, invoice_counter
class HModel(object): 
    def __init__(self,  statusBar):

        self.db = QtSql.QSqlDatabase.addDatabase("QODBC3");
        #connectString = "DRIVER=C:/Program Files\MariaDB/MariaDB ODBC Driver 64-bit/maodbcs.dll;" \
        #    "SERVERNODE=localport:3306;" \
        #    "UID=root;" \
        #    "PWD=test;" \
        #    "SCROLLABLERESULT=true"
        self.db.setDatabaseName("private_tuition_v3")
        self.db.setHostName("localhost")
        self.db.setPort(3306)
        self.db.setUserName("root")
        self.db.setPassword("test")


        if not self.db.open():
            print("Hannes an error happened!")
            QtWidgets.QMessageBox.warning(None, "Database log",
                           "Database Error: {0}".format(self.db.lastError().text()))
            sys.exit(1)
        
        self.setupHelperDBs()
        self.setupTableModels()
        self.statusBar = statusBar
        
        self.tab       = [self.student, self.stdcount, self.schedule, self.tuition, self.invoice, 
                           self.reminder, self.mileage, self.time, self.invcount]
        self.make_active_list()
        
        
     # produce 3 lists with first and last name of the students whom I have now
    def make_active_list(self):
        stdmod = self.student
        self.fnames = []    # first names of active students
        self.lnames = []    # last  names of active students
        self.imap   = []    # index map for active students
        self.active_student_ids   = []  # list of active student ids
        self.inactive_student_ids = []  # list of inactive student ids
        today       = QtCore.QDate.currentDate()
        
        for i in range(0, stdmod.rowCount()):
            #date      = stdmod.data3(i,"end_date")
            is_active = stdmod.data3(i,"is_active") # is_active column, can't use name because this column has been exchanged

            
            # make a list of active students
            if (is_active == "yes"):
                self.fnames.append(stdmod.data3(i,"first_name"))
                self.lnames.append(stdmod.data3(i,"last_name"))
                self.imap.append(i)
                self.active_student_ids.append(stdmod.data3(i,"student_id"))
            else :
                self.inactive_student_ids.append(stdmod.data3(i,"student_id"))
        
        print("fnames:", self.fnames)
        print("lnames:", self.lnames)
        print("imap:", self.imap)
        print("active student ids:", self.active_student_ids)
        print("inactive student ids:", self.inactive_student_ids)
    
    
    # word lists from the helper tables are inserted into
    # a dict. the table names are the key words
    def setupHelperDBs(self):
            self.helperTables = ["help_extracost", "help_payment", "help_transport", "help_travel_reason",
                              "help_vehicle", "help_weekday", "help_yesno"]
            
            self.helperLists = dict()
            
            for tableName in self.helperTables:
                qtext  = "SELECT word FROM {0};".format(tableName)
                query  = QtSql.QSqlQuery(qtext, self.db)
                listB = []
        
                while (query.next()):
                    b = query.value(0)
                    listB.append(b)
                    
                self.helperLists[tableName] = listB
                #print(listB)
        
    
    # set up all tables into table models
    # set up the header data
    def setupTableModels(self):
        
        # weekly schedule for tutoring
        self.schedule = HSqlTableModel(None, self.db)
        self.schedule.setTable("weekly_schedule")
        self.schedule.setReplacement(1, "student_info", "student_id", "last_name", True)
        self.schedule.setReplacement2(2, "help_weekday", True)
        self.schedule.setReplacement2(7, "help_extracost", True)
        self.schedule.setReplacement2(9, "help_extracost", True)
        self.schedule.setReplacement2(11, "help_transport", True)
        self.schedule.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.schedule.setSort(0, QtCore.Qt.AscendingOrder ) #ascending order for entry_nr
        self.schedule.setHeaderData(0, 1, "entry\nid")
        self.schedule.setHeaderData(7, 1, "1st extra\ncost type")
        self.schedule.setHeaderData(8, 1, "1st extra\ncost amount")
        self.schedule.setHeaderData(9, 1, "2nd extra\ncost type")
        self.schedule.setHeaderData(10, 1, "2nd extra\ncost amount")
        #self.schedule.setHeaderData(11, 1, "charge for\nwebsite")
        #self.schedule.setHeaderData(12, 1, "charge for\ntravel")
        self.schedule.select()
        
        
        #model for mileage recording
        self.mileage = HSqlTableModel(None, self.db)
        self.mileage.setTable("mileage_records")
        self.mileage.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.mileage.setSort(0, QtCore.Qt.AscendingOrder ) #ascending order for entry_nr
        self.mileage.setReplacement2(4, "help_travel_reason", True)
        self.mileage.setReplacement2(5, "help_vehicle", True)
        self.mileage.select()
        
        #model for student_info table
        self.student = HSqlTableModel(None, self.db)
        self.student.setTable("student_info")
        self.student.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.student.setSort(0, QtCore.Qt.AscendingOrder ) #ascending order
        self.student.setReplacement2(8,  "help_yesno", True)
        self.student.setReplacement2(18, "help_extracost", True)
        self.student.setReplacement2(20, "help_extracost", True)
        self.student.setReplacement2(22, "help_weekday", True)
        self.student.setReplacement2(25, "help_transport", True)
        self.student.setReplacement2(26, "help_payment", True)
        self.student.setHeaderData(0, 1, "student id")
        #self.student.setHeaderData(1, 1, "tuiton id prefix")
        #self.student.setHeaderData(2, 1, "first name")
        #self.student.setHeaderData(3, 1, "last name")
        #self.student.setHeaderData(4, 1, "parent first name")
        #self.student.setHeaderData(5, 1, " start date ")
        #self.student.setHeaderData(6, 1, "  end date  ")
        #self.student.setHeaderData(14, 1, "travel\ndistance")
        self.student.setHeaderData(18, 1, "extra cost 1\ntype")
        self.student.setHeaderData(19, 1, "extra cost 1\namount")
        self.student.setHeaderData(20, 1, "extra cost 2\ntype")
        self.student.setHeaderData(21, 1, "extra cost 2\namount")
        self.student.setHeaderData(23, 1, "usual\nstart time")
        self.student.setHeaderData(24, 1, "usual\nduration")
        self.student.setHeaderData(25, 1, "usual\ntravel method")
        self.student.setHeaderData(28, 1, "sessions\n  per invoice")
        self.student.select()
        
        
        #model for student_counters table 
        self.stdcount = HSqlTableModel(None, self.db)
        self.stdcount.setTable("student_counters")
        self.stdcount.setReplacement(1, "student_info", "student_id", "last_name", active=False)
        self.stdcount.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.stdcount.setSort(0, QtCore.Qt.AscendingOrder) #ascending order for student_id
        self.stdcount.setHeaderData(0, 1, "student\nid")
        self.stdcount.setHeaderData(1, 1, "last name")
        self.stdcount.setHeaderData(2, 1, "student\ncounter")
        self.stdcount.setHeaderData(3, 1, "receipt\ncounter")
        self.stdcount.setHeaderData(4, 1, "invoice\ncounter")
        self.stdcount.setHeaderData(5, 1, "active\ninvoice id")
        self.stdcount.setHeaderData(6, 1, "total\nreminders")
        self.stdcount.select()
        
        
        #model for invoice_counter table 
        self.invcount = HSqlTableModel(None, self.db)
        self.invcount.setTable("main_counters")
        self.invcount.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.invcount.setSort(1, QtCore.Qt.AscendingOrder )
        self.invcount.select()
        
        
        #model for tuition_records table
        self.tuition = HSqlTableModel(None, self.db)
        self.tuition.setTable("tuition_records")
        self.tuition.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.tuition.setReplacement(1, 'student_info', 'student_id', 'first_name', active=False)
        self.tuition.setReplacement(2, 'student_info', 'student_id', 'last_name', active=False)
        self.tuition.setReplacement2(4, 'help_weekday', active=True)
        self.tuition.setReplacement2(9, 'help_extracost', active=True)
        self.tuition.setReplacement2(11, 'help_extracost', active=True)
        self.tuition.setReplacement2(13, 'help_extracost', active=True)
        self.tuition.setReplacement2(17, 'help_transport', active=True)
        self.tuition.setReplacement2(18, 'help_payment', active=True)
        self.tuition.setReplacement2(19, 'help_yesno', active=True)
        self.tuition.setReplacement2(21, 'help_yesno', active=True)
        #self.tuition.setSort(0, QtCore.Qt.AscendingOrder ) #ascending order for tuition_id
        self.tuition.setHeaderData(0, 1, "tuition id")
        self.tuition.setHeaderData(1, 1, "student\nfirst name")
        self.tuition.setHeaderData(2, 1, "student\nlast name")
        self.tuition.setHeaderData(3, 1, " tuition date ")
        self.tuition.setHeaderData(4, 1, "tuition\nweekday")
        self.tuition.setHeaderData(5, 1, "start time")
        self.tuition.setHeaderData(7, 1, "travel\ndistance")
        self.tuition.setHeaderData(9, 1, "extra cost 1\ntype")
        self.tuition.setHeaderData(10, 1, "extra cost 1\namount")
        self.tuition.setHeaderData(11, 1, "extra cost 2\ntype")
        self.tuition.setHeaderData(12, 1, "extra cost 2\namount")
        self.tuition.setHeaderData(13, 1, "extra cost 3\ntype")
        self.tuition.setHeaderData(14, 1, "extra cost 3\namount")
        self.tuition.setHeaderData(19, 1, "payment\nreceived")
        self.tuition.setHeaderData(21, 1, "receipt\ncompleted")
        self.tuition.select()
        
        
        #model for invoice_records table
        self.invoice = HSqlTableModel(None, self.db)
        self.invoice.setTable("invoice_records")
        #self.invoice.setFilter(" invoice_id <= 'invb-0016'")
        self.invoice.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.invoice.setSort(0, QtCore.Qt.AscendingOrder ) #ascending order for tuition_date
        self.invoice.select()
        self.invoice.setReplacement(1, "student_info", "student_id", "last_name")
        self.invoice.setReplacement2(2, 'help_yesno', active=True)
        self.invoice.setReplacement2(3, 'help_yesno', active=True)
        # change horizontal header data maybe think of a more portable way to do this
        self.invoice.setHeaderData(2, 1, "invoice\nsent")
        self.invoice.setHeaderData(3, 1, "invoice\npaid")
        self.invoice.setHeaderData(4, 1, "invoice\nsend date")
        self.invoice.setHeaderData(5, 1, "invoice paid\ndate")
        self.invoice.setHeaderData(6, 1, "invoice\namount")
        self.invoice.setHeaderData(7, 1, "reference")
        self.invoice.setHeaderData(8, 1, "tuition id\nprefix")
        self.invoice.setHeaderData(9, 1, "tuition id\nnumbers")
        self.invoice.setHeaderData(10,1, "active\nsessions")
        self.invoice.setHeaderData(11,1, "total\nsessions")
        self.invoice.setHeaderData(12,1, "reminder\nentry")
        
        
        #model for time_recording table
        self.time = HSqlTableModel(None, self.db)
        self.time.setTable("time_recording")
        self.time.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.time.setSort(0, QtCore.Qt.AscendingOrder ) #ascending order for tuition_date
        self.time.select()
        # change horizontal header data maybe think of a more portable way to do this
        self.time.setHeaderData(0, 1, "entry_nr")
        self.time.setHeaderData(1, 1, "start date")
        self.time.setHeaderData(2, 1, "start time")
        self.time.setHeaderData(3, 1, "worked\ntime span")
        self.time.setHeaderData(4, 1, "end time")
        
        
        #model for the reminder_records table
        self.reminder = HSqlTableModel(None, self.db)
        self.reminder.setTable("reminder_records")
        self.reminder.setReplacement(2, "student_info", "student_id", "last_name")
        self.reminder.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.reminder.setSort(0, QtCore.Qt.AscendingOrder ) #ascending order for tuition_date
        self.reminder.select()
        
    
    
    # a few functions to search the tables
    
    # start, end are indexes in a column of a Table, we are searching
    # for the key in the column. It is assumed that the column is sorted
    # col is the column as number
    def _find1(self,start, end, key, model, col):
        sitem = model.data2(start,col)
        eitem = model.data2(end,col)
        
        #print("_find1, start", start, "end", end, "key", key, "sitem", sitem, "eitem", eitem)
        if( key == sitem ): return start
        if( key == eitem ): return end
        if( end - start <= 4 ):
            item = model.data2(start+1,col)
            if item == key: return start+1
            item = model.data2(start+2,col)
            if item == key: return start+2
            item = model.data2(start+3,col)
            if item == key: return start+3
            else: return -1
        else:
            i    = int((start+end)/2)
            item = model.data2(i,col)
            if (key.lower() < item.lower()):
                return self._find1(start, i, key, model, col)
            else:
                return self._find1(i, end, key, model, col)
    
    
    # For unsorted data also: search one by one from start to end both including
    # col is the column as number
    def _find1raw(self,start, end, key, model, col):
        for i in range(start,end+1):
            val     = model.data2(i,col)
            if  key == val:
                return i
        return -1
    
    
    # only for sorted data, convenience function
    # col is the column as number
    def _find1e(self, key, model, col):
        end   = model.rowCount()
        med   = end - 30   # -5
        ind   = self._find2(med, end, key, model, col)
        if ind>=0: return ind
        return self._find1raw(0, med, key, model, col) #+0
    
    
    # find by searching one by one from the end to start both including
    # col is the column as number
    def _find2(self, start, end, key, model, col):
        for i in range(end,start-1,-1):
            val     = model.data2(i,col)
            if key == val:
                return i
        return -1
        
        
    # find by searching one by one from rowCount()  to 0
    # col is the column as number
    def _find2e(self, key, model, col):
        start = 0
        end   = model.rowCount()
        return self._find2(0, end, key, model, col)
    
    
    # high level search functions for certain tables
    
    ## find keyword in primary key for table invoice_records
    def findInvoiceKey(self,key):
        index  =  int(re.match("\w+[-_]0*([1-9][0-9]*)", key ).group(1))-1
        invmod =  self.invoice
        col    =  invmod.fieldIndex("invoice_id")
        if  key == invmod.data2(index,col):
            return index
        index  = self._find2e(key, invmod, col)
        assert index >= 0, "findInvoiceKey: key not found!"
        return index
    
    ## find keyword in primary key for table tuition_records
    def findTuitionKey(self,key):
        tutmod  = self.tuition
        col    = tutmod.fieldIndex("tuition_id")
        index  = self._find1e(key, tutmod, col)
        assert index >= 0, "findTuitionKey: key {0} was not found!".format(key)
        return index
    
    ## find student_id in primary key for table student_info
    def findStudentKey(self,key):
        index  = int(key)-1
        stdmod = self.student
        col    = stdmod.fieldIndex("student_id")
        if  key == stdmod.data2(index,col):
            return index
        index  = self._find2e(key, model, col)
        assert index >= 0, "findStudentKey: key {0} not found!".format(key)
        return index
    
    
    ## find keyword in primary key for table student_counters
    def findStdcountKey(self,key):
        index  = int(key)-1
        sdcmod = self.stdcount
        col    = sdcmod.fieldIndex("student_id")
        #coldes = "student_id"
        if  key == sdcmod.data2(index,col):    #model.record(index).value(coldes):
            return index
        index  = self._find2e(key, model, coldes)
        assert index >= 0, "findStdcountKey: key not found!"
        return index
    
    
    ## find keyword in primary key for table weekly_schedule
    ## and weekday as secondary key
    def findScheduleKey(self, student_id, weekday):
        schmod = self.schedule
        col1   = schmod.fieldIndex("last_name")
        col2   = schmod.fieldIndex("weekday")
        size   = schmod.rowCount()

        for i in range(0,size):
            id2 = schmod.data2(i,col1, False)
            if student_id==id2 :
                day = schmod.data2(i,col2, False)
                if day == weekday: 
                    return i
                
        print("findScheduleKey: key not found!")
        return -1
    
    
    ## find keyword in primary key for table weekly_schedule
    ## the schedule table should have less than 20 entries
    ## we don't need a sophisticated search method
    def findScheduleKey2(self, student_id, start=0):
        schmod = self.schedule
        col    = schmod.fieldIndex("last_name")
        size   = schmod.rowCount()
        
        for i in range(start,size):
            id2 = schmod.data2(i,col, False)
            if student_id == id2 :
                return i
        
        return -1
    
    
    
    ## find keyword in primary key entry_nr for table reminder_records
    def findReminderKey(self, entry_nr, span=40):
        remmod = self.reminder
        col    = remmod.fieldIndex("entry_nr")
        start  = remmod.rowCount()
        end    = start - span
        if end < -1:   end=-1
        
        for i in range(start,end,-1):
            id2 = remmod.data2(i,col)
            if entry_nr==id2 :
                return i
        return -1
    
    
    
    
    
     # does this model contain unsaved data
    def hasUnsavedData(self):
        l     = len(self.tab)
        
        for i in range(0,l):
            if self.tab[i].hasUnsavedData(): return True
            
        return False
    
    
    
    # print functions
    def print_signature(self):
        print("model_invoice:", self.invoice)
        print("model_tuition:", self.tuition)
        print("model_mileage:", self.mileage)
        print("model_student:", self.student)
        print("model_stdcount:", self.stdcount)
        print("model_invcount:", self.invcount)
        
        
    def dump_model(self, index):
        model = self.tab[index]
        print("Dump of table", model)
        for i in range(0, model.rowCount()):
            rec = model.record(i)
            print("row {:02d} : ".format(i), end='')
            for j in range(0, rec.count()):
                print(rec.value(j),"  ", end='')
            print('\n')
            
            
    # print out a dump of record rec 
    def dump_record(self, rec, name = ""):
        print("Dump of record: ", name, "\n", end='')
        for i in range(0, rec.count()):
            print(rec.value(i),"  ", end='')
        print("\n")


