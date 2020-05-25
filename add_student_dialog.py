# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
import ui_add_student
from settings import *
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



# multiple inheritance
class add_student_Dialog(QtWidgets.QDialog, ui_add_student.Ui_Dialog):
    def __init__(self, model, parent=None):
        super(add_student_Dialog, self).__init__(parent)
        self.setupUi(self)
        
        # safe important data
        self.model           = model
        self.sqlList_extra   = self.model.student.rLib[18]
        self.sqlList_yesno   = self.model.student.rLib[8]
        self.sqlList_weekday = self.model.student.rLib[22]
        
        self.statusBar      = parent.statusBar()
        self.student_record = model.student.record(1)
        
        # initiate combo boxes and date
        self.comboBox_21.insertItems(0, self.model.helperLists["help_extracost"])
        self.comboBox_22.insertItems(0, self.model.helperLists["help_extracost"])
        self.comboBox_23.insertItems(0, self.model.helperLists["help_weekday"])
        self.comboBox_24.insertItems(0, self.model.helperLists["help_transport"])
        self.comboBox_25.insertItems(0, self.model.helperLists["help_payment"])
        self.dateEdit.setDate(QtCore.QDate.currentDate()) #set date as today
        
        self.pButton_Add.clicked.connect(self.add_student_record)
        
        # initiate lcd number with next student_id
        record = self.model.student.record(self.model.student.rowCount() - 1)
        val    = record.value(0) + 1;
        self.lcdNumber.display(val)
        self._init_form()
    
        
    # initiate the form with simple values
    def _init_form(self):
        self.lineEdit_11.setText("")
        self.lineEdit_12.setText("")
        self.lineEdit_13.setText("")
        self.lineEdit_14.setText("")
        self.lineEdit_15.setText("")
        self.lineEdit_16.setText("")
        self.lineEdit_17.setText("")
        self.lineEdit_18.setText("")
        self.lineEdit_19.setText("")
        self.lineEdit_1A.setText("")
        self.lineEdit_1B.setText("")
        self.lineEdit_21.setText("")
        self.lineEdit_22.setText("")
        self.comboBox_21.setCurrentIndex(self.comboBox_21.findText("travel"))
        self.comboBox_22.setCurrentIndex(self.comboBox_22.findText("unused"))
        self.comboBox_24.setCurrentIndex(self.comboBox_24.findText("car"))
        self.comboBox_25.setCurrentIndex(self.comboBox_25.findText("bank transfer"))
        self.doubleSpinBox_11.setValue(5.0)
        self.doubleSpinBox_21.setValue(30.0)
        self.spinBox_25.setValue(60)
        self.spinBox_26.setValue(2)
        self.timeEdit.setTime(QtCore.QTime(16,0))
    
    
        
    # produce an QSqlTableRecord with the form data
    def fill_record(self):
        self.student_record.setValue("student_id", self.lcdNumber.intValue()) #student_id
        self.student_record.setValue("tuition_id_prefix", self.lineEdit_11.text())           #unique_tuition_id_prefix
        self.student_record.setValue("first_name", self.lineEdit_12.text())
        self.student_record.setValue("last_name", self.lineEdit_13.text())
        self.student_record.setValue("parent_name", self.lineEdit_14.text())
        self.student_record.setValue("extra_info", self.lineEdit_15.text())
        self.student_record.setValue("start_date", self.dateEdit.date())
        self.student_record.setValue("end_date", self.dateEdit_2.date())
        self.student_record.setValue("is_active", "yes")
        self.student_record.setValue("address", self.lineEdit_16.text())
        self.student_record.setValue("postcode", self.lineEdit_17.text())
        self.student_record.setValue("phone_student", self.lineEdit_18.text())
        self.student_record.setValue("email_student", self.lineEdit_19.text())
        self.student_record.setValue("phone_parent", self.lineEdit_1A.text())
        self.student_record.setValue("email_parent", self.lineEdit_1B.text())
        self.student_record.setValue("travel_distance", self.doubleSpinBox_11.value())     # travel distance
        
        self.student_record.setValue("fees_ph", self.doubleSpinBox_21.value())     # fees ph
        self.student_record.setValue("discount", self.doubleSpinBox_22.value()) 
        self.student_record.setValue("extra_cost1_type", self.comboBox_21.currentText())
        self.student_record.setValue("extra_cost1_amount", self.doubleSpinBox_23.value())
        self.student_record.setValue("extra_cost2_type", self.comboBox_22.currentText())
        self.student_record.setValue("extra_cost2_amount", self.doubleSpinBox_24.value())
        self.student_record.setValue("usual_day", self.comboBox_23.currentText())
        self.student_record.setValue("usual_start_time", self.timeEdit.time())           # usual start_time
        self.student_record.setValue("usual_duration", self.spinBox_25.value())
        self.student_record.setValue("usual_travel_method", self.comboBox_24.currentText())
        self.student_record.setValue("payment_method", self.comboBox_25.currentText())
        self.student_record.setValue("invoice_email", self.lineEdit_21.text())
        self.student_record.setValue("sessions_per_invoice", self.spinBox_26.value())
        self.student_record.setValue("invoice_to", self.lineEdit_22.text())
        
    

         
    def _create_student_counters(self):
        rec        = self.model.stdcount.record(0)
        student_id = self.student_record.value("student_id")
        
        rec.setValue("student_id", student_id)
        rec.setValue("last_name", student_id)
        rec.setValue("student_counter", 1)
        rec.setValue("receipt_counter", 1)
        rec.setValue("invoice_counter", 0)
        rec.setValue("active_invoice_id", "")
        rec.setValue("total_reminders", 0)
        return rec
    
        
    # add the record from the dialog to the model_tuition
    def add_student_record(self):
        self.fill_record()

        # insert the record from the dialog into the main table (not database yet)
        if self.model.student.insertRecord(-1, self.student_record):
            self.statusBar.showMessage("Student record successfully inserted in table", 3000)
            stdcount_record = self._create_student_counters()
            if self.model.stdcount.insertRecord(-1, stdcount_record):
                last_name  = self.student_record.value("last_name")
                student_id = self.student_record.value("student_id")
                self.model.stdcount.rLib[1].addPair(student_id, last_name)
        else:
            QtWidgets.QMessageBox.critical(self, "error", "student record could not be inserted in table")
    
        self.accept()    
        self.done(0)
    

            
        
