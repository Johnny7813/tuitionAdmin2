# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
import  ui_add_schedule_entry
from    settings import settings
from    invoice_factory import *
import  re
import  sys


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
class add_schedule_Dialog(QtWidgets.QDialog, ui_add_schedule_entry.Ui_Dialog):
    def __init__(self, model, parent=None):
        super(add_schedule_Dialog, self).__init__(parent)
        self.setupUi(self)
        
        self.model           = model
        self.schedule_entry  = model.schedule.record(0)
        self.statusBar       = model.statusBar
        
        self.comboBox_11.insertItems(0, self.model.lnames)
        self.comboBox_12.insertItems(0, self.model.helperLists["help_weekday"])
        self.comboBox_21.insertItems(0, self.model.helperLists["help_extracost"])
        self.comboBox_22.insertItems(0, self.model.helperLists["help_extracost"])
        self.comboBox_23.insertItems(0, self.model.helperLists["help_payment"])
        self.comboBox_24.insertItems(0, self.model.helperLists["help_transport"])
        
        self.setWindowTitle("Add Schedule Appointment")
        
        self.comboBox_11.currentIndexChanged.connect(self._init_form)
        self.pButton_Add.clicked.connect(self.add_schedule_entry)
        self.pButton_Add_more.clicked.connect(self.add_more_schedule_entry)
        self.comboBox_11.setCurrentIndex(0)
        self._init_form(0)
    
    
    #initialise the form with general data
    def _init_form(self, ind):
        index            = self.model.imap[ind]
        self.student_idx = index
        record           = self.model.student.record(index)
    
        #self.model.dump_record(record)
        self.feesPH         = record.value("fees_ph")
        self.discount       = record.value("discount")
        self.duration       = record.value("usual_duration")
        self.weekday        = record.value("usual_day")
        self.startTime      = record.value("usual_start_time")
        self.ecostType1     = record.value("extra_cost1_type")
        self.ecostAmount1   = record.value("extra_cost1_amount")
        self.ecostType2     = record.value("extra_cost2_type")
        self.ecostAmount2   = record.value("extra_cost2_amount")
        self.paymentMethod  = record.value("payment_method")
        self.travelMethod   = record.value("usual_travel_method")
        self.address        = record.value("address")
        
        #print("usual day: ", self.weekday)
        next_entry          = self._next_index()
        self.lcdNumber.display(next_entry)
        self.comboBox_12.setCurrentIndex(self.comboBox_12.findText(self.weekday))
        self.timeEdit.setTime(self.startTime)
        self.spinBox_11.setValue(self.duration)
        self.spinBox_12.setValue(self.feesPH)
        self.doubleSpinBox_13.setValue(self.discount)
        self.comboBox_21.setCurrentIndex(self.comboBox_21.findText(self.ecostType1))
        self.doubleSpinBox_21.setValue(self.ecostAmount1)
        self.comboBox_22.setCurrentIndex(self.comboBox_22.findText(self.ecostType2))
        self.doubleSpinBox_22.setValue(self.ecostAmount2)
        self.comboBox_23.setCurrentIndex(self.comboBox_23.findText(self.paymentMethod))
        self.comboBox_24.setCurrentIndex(self.comboBox_24.findText(self.travelMethod))
        self.addressLineEdit.setText(self.address)
        
        
    
    # produce an QSqlTableRecord with the form data
    def fill_record(self):
        self.schedule_entry.setValue("entry_nr", self.lcdNumber.intValue())      #entry_nr
        name            = self.comboBox_11.currentText()
        #student_id      = self.model.imap[ind]+1
        self.schedule_entry.setValue("last_name", name )                     #student_id
        self.schedule_entry.setValue("weekday", self.comboBox_12.currentText())  #tuition_weekday
        self.schedule_entry.setValue("start_time", self.timeEdit.time())           #start_time
        self.schedule_entry.setValue("duration", self.spinBox_11.value())           #duration
        self.schedule_entry.setValue("fees_ph", self.spinBox_12.value())         #fees_ph
        self.schedule_entry.setValue("discount", self.doubleSpinBox_13.value())   #discount
        self.schedule_entry.setValue("extra_cost1_type", self.comboBox_21.currentText())   #extra cost 1 type
        self.schedule_entry.setValue("extra_cost1_amount", self.doubleSpinBox_21.value())   ##extra cost 1 amount
        self.schedule_entry.setValue("extra_cost2_type", self.comboBox_22.currentText())   #extra cost 1 type
        self.schedule_entry.setValue("extra_cost2_amount", self.doubleSpinBox_22.value())   ##extra cost 1 amount
        self.schedule_entry.setValue("payment_method", self.comboBox_23.currentText())    #charge_for_website
        self.schedule_entry.setValue("travel_method", self.comboBox_24.currentText())    #travel_method
        self.schedule_entry.setValue("address", self.addressLineEdit.text())    #address
        
        
    
    # add the record from the dialog to the model.schedule
    def _add_schedule_entry(self):
        self.fill_record()

        # insert the record from the dialog into the main table (not database yet)
        if self.model.schedule.insertRecord(-1, self.schedule_entry):
            self.statusBar.showMessage("Schedule entry successfully inserted in table", 3000)
        else:
            QtWidgets.QMessageBox.critical(self, "error", "schedule record could not be inserted in table")
    
    
    
    # add the record from the dialog to the model.schedule and close the Dialog
    def add_schedule_entry(self):
        self._add_schedule_entry()
        self.model.schedule.dirtyData = True
        self.accept()    
        self.done(0)
    
    
    # add the record from the dialog to the model.schedule and close the Dialog
    def add_more_schedule_entry(self):
        self._add_schedule_entry()
        self.model.schedule.dirtyData = True
    
    # next entry number
    def _next_index(self):
        elist = [0]
        size  = self.model.schedule.rowCount()
        for i in range(size):
            elist.append(self.model.schedule.data3(i,"entry_nr"))
        
        mval  = max(elist)+1
        #print("MVal:",mval, "Size:",size)
        return mval


