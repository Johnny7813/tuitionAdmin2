# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
import ui_send_reminder
import sys
import invoice_factory
from   custom_modview import *


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



# multiple inheritance
class send_reminder_Dialog(QtWidgets.QDialog, ui_send_reminder.Ui_Dialog):
    def __init__(self, model, parent=None):
        super(send_reminder_Dialog, self).__init__(parent)
        self.setupUi(self)
        
        self.model   =  model
        self.records =  []
        self.rowCount=  0
        self.invfac  = invoice_factory.invoice_factory(model)
        #self.model.setTranslate(True)

        labels       = ["selected", "last name", "invoice id", "number of\nreminders", "last\nreminder" ]
        tickBoxDel   = tickBoxDelegate(self)
        
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(5)
        
        self.tableWidget.setColumnWidth(0,80)
        self.tableWidget.setColumnWidth(1,100)
        self.tableWidget.setColumnWidth(2,100)
        self.tableWidget.setColumnWidth(3,120)
        self.tableWidget.setHorizontalHeaderLabels(labels)
        self.tableWidget.setItemDelegateForColumn(0, tickBoxDel)
        self.tableWidget.horizontalHeader().setFixedHeight(60)
        
        
        
        #self.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.process_reminders)
        self.buttonBox.accepted.connect(self.process_reminders)
        
        self.populate()
        
    
    # populate table with entries 
    def populate(self):
        start  = self.model.invoice.rowCount()-1
        stop   = max(start-60,0)
        row    = 0
        today  = QtCore.QDate.currentDate()
        invMod = self.model.invoice
        remMod = self.model.reminder
        stdMod = self.model.student
        
        for i in range(start,stop,-1):
            
            #irec   = self.model.invoice.record(i)
            
            #print("invMod", invMod.data2(i,"invoice_paid_yn"))
            #print("invMod", invMod.data2(i,"invoice_paid_yn",False))
            
            
            #print("iteration: ",i)
            #if  (irec.value("invoice_paid_yn") == "yes") or (irec.value("invoice_send_yn") == "no") : 
             #   continue
            
            if  (invMod.data3(i,"invoice_paid_yn") == "yes") or (invMod.data3(i,"invoice_send_yn") == "no") : 
                continue
            
            date = invMod.data3(i,"invoice_send_date")
            
            invoice_id  =  invMod.data3(i,"invoice_id")
            ### here is the problem! translate yes or no
            #student_id  =  invMod.data3(i,"student_id",False)
            student_id  =  invMod.data3(i,"last_name",False)
            inv_send_yn =  invMod.data3(i,"invoice_send_yn")
            sindex      =  self.model.findStudentKey(student_id)
            #srec        =  self.model.student.record(sindex)
            lname       =  stdMod.data3(sindex,"last_name")
            
            
            print("\n\nunpaid invoice_id: ", invoice_id)
            print("invoice send: ", inv_send_yn)
            print("Send date: ", date)
            
            rval  =  invMod.data3(i,"reminder_entry")
            print("reminder_entry: ", rval)
            if rval == 0:
                reminders = 0
            else :
                # we need to find the entry in reminder_records
                r2   = self.model.findReminderKey(rval)
                rrec = self.model.reminder.record(r2)
                reminders = remMod.data3(i,"reminders")
                date      = remMod.data3(i,"last_reminder")
                print("Reminders: ", reminders)
                print("Date: ", date.toString())
            
            # last reminder or invoice send date must be send at least 7 days ago
            if  (date.daysTo(today) < 7):
                continue
            
            
            rec    = [0, invoice_id, i, student_id, reminders, date, rval]
            self.records.append(rec)
            item0  =  QtWidgets.QTableWidgetItem(0)
            item0.setData(QtCore.Qt.EditRole, 0)
            item1  =  QtWidgets.QTableWidgetItem(lname)
            item1.setFlags(QtCore.Qt.NoItemFlags)
            item2  =  QtWidgets.QTableWidgetItem(invoice_id)
            item2.setFlags(QtCore.Qt.NoItemFlags)
            item3  =  QtWidgets.QTableWidgetItem("{0}".format(reminders))
            item3.setFlags(QtCore.Qt.NoItemFlags)
            item4  =  QtWidgets.QTableWidgetItem(date.toString("dd/MM/yyyy"))
            item4.setFlags(QtCore.Qt.NoItemFlags)
            
            self.tableWidget.setItem(row,0,item0)
            self.tableWidget.setItem(row,1,item1)
            self.tableWidget.setItem(row,2,item2)
            self.tableWidget.setItem(row,3,item3)
            self.tableWidget.setItem(row,4,item4)
            
            row = row + 1
        
        
        self.tableWidget.setRowCount(row)
        self.rowCount = row

    
    # update data in self.records
    def update_internal_data(self):
        print("\n\nupdate_internal_data called")
        
        for i in range(0, self.rowCount):
            item = self.tableWidget.item(i,0)
            rec  = self.records[i]
            
            if item.data(QtCore.Qt.EditRole) == 1:
                rec[0] = 1
                self.records[i] = rec
                
            print("Record : ", rec)
        
        print("\n\n")
    
    
    # process one invoice Record
    # change the tables
    def updateRecord(self,i):
        rec = self.records[i]
        
        invoice_id = rec[1]
        student_id = rec[3]
        iindex     = rec[2]
        today      = QtCore.QDate.currentDate()
        
        self._inc_stdreminder_counter(student_id)
        
        ## there is already a reminder record for this invoice
        if rec[6]>0 :
            entry_nr = rec[6]
            ind      = self.model.findReminderKey(entry_nr)
            rrec     = self.model.reminder.record(ind)
            rrec.setValue("reminders", rec[4]+1)
            rrec.setValue("last_reminder", today)
            self.model.reminder.setRecord(ind, rrec)
            
        # we need a new reminder record    
        else:    
            entry_nr = self._read_reminder_counter()
            self._inc_reminder_counter()
            rrec     = self.model.reminder.record(1)
            rrec.setValue("entry_nr", entry_nr)
            rrec.setValue("invoice_id", invoice_id)
            rrec.setValue("student_id", student_id)
            rrec.setValue("reminders", 1)
            rrec.setValue("last_reminder", today)
            self.model.reminder.insertRecord(-1, rrec)
            irec     = self.model.invoice.record(iindex)
            irec.setValue("reminder_nr", entry_nr)
            self.model.invoice.setRecord(iindex, irec)
            #print("We are here! Entry_nr: ", entry_nr)
        
    
    
    # process reminders
    def process_reminders(self):
    
        self.update_internal_data()
        ret = 0
    
        for i in range(0, self.rowCount):
            rec        = self.records[i]
            invoice_id = rec[1]
            student_id = rec[3]
            inv_idx    = rec[2]
            reminder   = rec[4]
            if rec[0] == 1: ## reminder box ticked
              if not self.invfac.send_invoice_reminder(invoice_id, inv_idx, student_id, reminder):
                  ret += 1
              else :
                  self.updateRecord(i)
        
        if ret == 0:
            QtWidgets.QMessageBox.information(self, "Reminders send", "All reminders have been send successfully!")
        else :
            QtWidgets.QMessageBox.information(self, "Reminders send", "There was a problem with some of the reminders")
            
    
    # increase reminder counter in invoice_counter
    def _inc_reminder_counter(self):
        rec       = self.model.invcount.record(0)
        counter   = rec.value("reminder_counter")
        counter  += 1
        rec.setValue("reminder_counter", counter)
        self.model.invcount.setRecord(0, rec)
        
    
    # read reminder counter in invoice_counter
    def _read_reminder_counter(self):
        rec       = self.model.invcount.record(0)
        counter   = rec.value("reminder_counter")
        return counter
    
    
    # increase invoice counter in student_counters
    def _inc_stdreminder_counter(self, student_id):
        index = self.model.findStdcountKey(student_id)
        # now we need to increase the counter in the database
        rec       = self.model.stdcount.record(index)
        counter   = rec.value("total_reminders")
        counter  += 1
        rec.setValue("total_reminders", counter)
        self.model.stdcount.setRecord(index, rec)
        

