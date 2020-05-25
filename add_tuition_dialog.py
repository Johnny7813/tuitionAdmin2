# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
import  ui_add_tuition
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
class add_tuition_Dialog(QtWidgets.QDialog, ui_add_tuition.Ui_Dialog):
    def __init__(self, model, parent=None):
        super(add_tuition_Dialog, self).__init__(parent)
        self.setupUi(self)
        
        self.model          = model
        self.tuition_record = model.tuition.record(0)
        self.statusBar      = parent.statusBar()
        self.student_idx    = 0 # index of the student that is selected, == stuent_id -1
        self.ifactory       = invoice_factory(self.model, self)
        
        self.comboBox_1.insertItems(0, self.model.fnames)
        self.comboBox_2.insertItems(0, self.model.lnames)
        self.comboBox_13.insertItems(0, self.model.helperLists["help_weekday"])
        self.comboBox_19a.insertItems(0, self.model.helperLists["help_extracost"])
        self.comboBox_21a.insertItems(0, self.model.helperLists["help_extracost"])
        self.comboBox_22a.insertItems(0, self.model.helperLists["help_extracost"])
        self.comboBox_24b.insertItems(0, self.model.helperLists["help_transport"])
        self.comboBox_25b.insertItems(0, self.model.helperLists["help_payment"])
        self.comboBox_26b.insertItems(0, self.model.helperLists["help_yesno"])
        self.comboBox_28b.insertItems(0, self.model.helperLists["help_yesno"])
        
        self.setWindowTitle("Add Tuition Record")
        today = QtCore.QDate.currentDate()
        self.dateEdit_11.setDate(today)
        ind   = today.dayOfWeek()%7
        self.comboBox_13.setCurrentIndex(ind)
        
        self.comboBox_1.currentIndexChanged.connect(self._fill_form1a)
        self.comboBox_2.currentIndexChanged.connect(self._fill_form1b)
        self.pButton_Add.clicked.connect(self.add_tuition_record)
        self.pButton_Add_more.clicked.connect(self.add_more_tuition_record)
        self.dateEdit_11.dateChanged.connect(self.date_changed)
        self.spinBox_15.valueChanged.connect(self.set_total_cost1)
        self.spinBox_17.valueChanged.connect(self.set_total_cost2)
        self.doubleSpinBox_18.valueChanged.connect(self.set_total_cost3)
        self.doubleSpinBox_19b.valueChanged.connect(self.set_total_cost4)
        self.doubleSpinBox_21b.valueChanged.connect(self.set_total_cost5)
        self.doubleSpinBox_22b.valueChanged.connect(self.set_total_cost6)
        self.comboBox_25b.currentIndexChanged.connect(self.payment_changed)
        # fill form with data
        self._fill_form1a(0)
        self.comboBox_1.setCurrentIndex(0)
        #self.check_record()
        
       
    
    #adjust weekday comboBox if date has changed
    def date_changed(self, date):
        day_ind     = date.dayOfWeek()%7
        sind        = self.comboBox_2.currentIndex()
        #student_idx = self.model.imap[sind]
        #print("date_changed:", date, "\tday_ind:", day_ind, " sind:", sind)
        self.comboBox_13.setCurrentIndex(day_ind)
        self._fill_form3(sind, day_ind)
    
    
    #set total cost in form according to duration
    def set_total_cost1(self,duration):
        #print("set_total_cost:", duration)
        self.duration      = duration
        self.totalCost     = float(self.duration)/60.0 * self.feesPH + self.ecost1_amount
        self.totalCost    += self.ecost2_amount + self.ecost3_amount - self.discount
        self.doubleSpinBox_23b.setValue(self.totalCost)
        
        
    #set total cost in form according to fees per hour
    def set_total_cost2(self, fees):
        #print("set_total_cost:", duration)
        self.feesPH        = fees
        self.totalCost     = float(self.duration)/60.0 * self.feesPH + self.ecost1_amount
        self.totalCost    += self.ecost2_amount + self.ecost3_amount - self.discount
        self.doubleSpinBox_23b.setValue(self.totalCost)


    
    #set total cost in form according to discount
    def set_total_cost3(self, discount):
        #print("set_total_cost:", duration)
        self.discount      = discount
        self.totalCost     = float(self.duration)/60.0 * self.feesPH + self.ecost1_amount
        self.totalCost    += self.ecost2_amount + self.ecost3_amount - self.discount
        self.doubleSpinBox_23b.setValue(self.totalCost)
    
    
    #set total cost in form according to ecost1_amount
    def set_total_cost4(self, ecost):
        #print("set_total_cost:", duration)
        self.ecost1_amount = ecost
        self.totalCost     = float(self.duration)/60.0 * self.feesPH + self.ecost1_amount
        self.totalCost    += self.ecost2_amount + self.ecost3_amount - self.discount
        self.doubleSpinBox_23b.setValue(self.totalCost)
        
    
    #set total cost in form according to ecost2_amount
    def set_total_cost5(self, ecost):
        #print("set_total_cost:", duration)
        self.ecost2_amount = ecost
        self.totalCost     = float(self.duration)/60.0 * self.feesPH + self.ecost1_amount
        self.totalCost    += self.ecost2_amount + self.ecost3_amount - self.discount
        self.doubleSpinBox_23b.setValue(self.totalCost)
        
    
    #set total cost in form according to ecost3_amount
    def set_total_cost6(self, ecost):
        #print("set_total_cost:", duration)
        self.ecost3_amount = ecost
        self.totalCost     = float(self.duration)/60.0 * self.feesPH + self.ecost1_amount
        self.totalCost    += self.ecost2_amount + self.ecost3_amount - self.discount
        self.doubleSpinBox_23b.setValue(self.totalCost)

    
    # payment method changed slot
    def payment_changed(self, ind):
        paymentVal = self.model.tuition.rLib[18].getBatInd(ind)
        #print("Index: ", ind, "paymentVal: ", paymentVal)
        if paymentVal == "bank transfer":
            self.lineEdit_29b.setText(self.ifactory.get_invoice_id(self.student_idx)) #set invoice id
        else:
            self.lineEdit_29b.setText("")
    

    # pre-fill the form with good heuristic data
    # when person first name is changed
    def _fill_form1a(self, ind):
        #print("Index:", ind)
        index            = self.model.imap[ind]
        self.comboBox_2.setCurrentIndex(ind)
        self.student_idx = index
        day_ind          = self.comboBox_13.currentIndex()
        self._fill_form3(ind, day_ind)
        
    # pre-fill the form with good heuristic data
    # when person last name is changed
    def _fill_form1b(self, ind):
        #print("Index:", ind)
        index            = self.model.imap[ind]
        self.comboBox_1.setCurrentIndex(ind)
        self.student_idx = index
        day_ind          = self.comboBox_13.currentIndex()
        self._fill_form3(ind, day_ind)
    
    
    
    # update pre-fill the form with good heuristic data after "add more"
    def _fill_form2(self):
        student_id      = self.student_idx+1
        record          = self.model.student.record(self.student_idx)
        cind            = self.model.findStdcountKey(student_id)
        counter         = self.model.stdcount.record(cind).value("student_counter")
        tuitionIdPref   = record.value("tuition_id_prefix")
        tuition_id      = tuitionIdPref + "{:03d}".format(counter)
        
        if self.paymentM == "bank transfer" :  # bank transfer
            word = self.ifactory.get_invoice_id(self.student_idx)
            #print("_fill_form2: bank transfer selected. Word=", word)
            self.lineEdit_29b.setText(word) #set invoice id
        else: # anything but bank transfer
            self.lineEdit_29b.setText("") #no invoice_id needed
            #print("_fill_form2: bank transfer NOT selected")
            
        self.lineEdit_11.setText(tuition_id)
        
    
    
    
    
    # pre-fill the form with good heuristic data
    # ind: index from student name comboBox , day: weekday from comboBox
    def _fill_form3(self, ind, day_ind):
        index              = self.model.imap[ind]
        student_id         = self.student_idx+1
        #translate index from comboBox into day inter value
        day                = self.model.schedule.rLib[2].getAatInd(day_ind)
        sindex             = self.model.findScheduleKey(student_id, day)
        self.ecost3_amount = 0.0
        #self.comboBox_1.setCurrentIndex(ind)
        #self.comboBox_2.setCurrentIndex(ind)
        
        # no entry found in weekly_schedule
        if sindex == -1: 
            print("Fill Form with general info from student_info")
            self._fill_form5(index)
        else :
            print("Fill Form with info from weekly schedule")
            self._fill_form4(sindex)
            
    
    
    
    # fill form with data from weekly_schedule        
    def _fill_form4(self, sindex):
        student_rec         =  self.model.student.record(self.student_idx)
        schedule_rec        =  self.model.schedule.record(sindex)
    
        tuitionIdPref       = student_rec.value("tuition_id_prefix")
        self.feesPH         = schedule_rec.value("fees_ph")
        self.duration       = schedule_rec.value("duration")
        self.ecost1_type    = schedule_rec.value("extra_cost1_type")
        self.ecost1_amount  = schedule_rec.value("extra_cost1_amount")
        self.ecost2_type    = schedule_rec.value("extra_cost2_type")
        self.ecost2_amount  = schedule_rec.value("extra_cost2_amount")
        self.discount       = schedule_rec.value("discount")
        self.travelM        = schedule_rec.value("travel_method")
        self.paymentM       = student_rec.value("payment_method")
        self.totalCost      = self.duration/60.0 * self.feesPH + self.ecost1_amount + self.ecost2_amount - self.discount
        cind                = self.model.findStdcountKey(self.student_idx+1)
        counter             = self.model.stdcount.record(cind).value("student_counter")
        tuition_id          = tuitionIdPref + "{:03d}".format(counter)
        
        # set stuff
        self.lcdNumber.display(student_rec.value("student_id"))
        self.lineEdit_11.setText(tuition_id)
        self.timeEdit_14.setTime(schedule_rec.value("start_time"))
        self.spinBox_15.setValue(self.duration)
        self.doubleSpinBox_16.setValue(student_rec.value("travel_distance"))
        self.spinBox_17.setValue(self.feesPH)
        self.doubleSpinBox_19b.setValue(self.ecost1_amount)
        self.doubleSpinBox_21b.setValue(self.ecost2_amount)
        self.doubleSpinBox_18.setValue(self.discount)
        self.doubleSpinBox_23b.setValue(self.totalCost)
        self.doubleSpinBox_22b.setValue(0.0)
        self.comboBox_19a.setCurrentIndex(self.comboBox_19a.findText(self.ecost1_type))
        self.comboBox_21a.setCurrentIndex(self.comboBox_21a.findText(self.ecost2_type))
        self.comboBox_22a.setCurrentIndex(self.comboBox_22a.findText("unused"))
        self.comboBox_24b.setCurrentIndex(self.comboBox_24b.findText(self.travelM))
        self.comboBox_25b.setCurrentIndex(self.comboBox_25b.findText(self.paymentM))
        self.comboBox_26b.setCurrentIndex(1)
        self.comboBox_28b.setCurrentIndex(1)
        
        #now we need the invoice_id, either from student_counters or we make a new one 
        if self.paymentM == "bank transfer" :  # bank transfer
            word = self.ifactory.get_invoice_id(self.student_idx)
            #print("_fill_form4: bank transfer selected. Word=", word)
            self.lineEdit_29b.setText(word) #set invoice id
        else: # anything but bank transfer
            self.lineEdit_29b.setText("") #no invoice_id needed
            #print("_fill_form4: bank transfer NOT selected")
        
        
    
    
    
    # fill form with data from student_records        
    def _fill_form5(self, student_idx):
        #self.model.student.setTranslate(True)
        record              = self.model.student.record(student_idx)
        tuitionIdPref       = record.value("tuition_id_prefix")
        self.feesPH         = record.value("fees_ph")
        self.duration       = record.value("usual_duration")
        self.weekday        = record.value("usual_day")
        self.ecost1_type    = record.value("extra_cost1_type")
        self.ecost1_amount  = record.value("extra_cost1_amount")
        self.ecost2_type    = record.value("extra_cost2_type")
        self.ecost2_amount  = record.value("extra_cost2_amount")
        self.discount       = float(record.value("discount"))
        self.paymentM       = record.value("payment_method")
        self.travelM        = record.value("usual_travel_method")
        #print("payment method: ", self.paymentM, "   , student_idx: ", student_idx)
        self.totalCost      = self.duration/60.0 * self.feesPH + self.ecost1_amount + self.ecost2_amount - self.discount
        cind                = self.model.findStdcountKey(student_idx+1)
        counter             = self.model.stdcount.record(cind).value("student_counter")
        tuition_id          = tuitionIdPref + "{:03d}".format(counter)
        
        # set stuff
        self.lcdNumber.display(record.value("student_id"))
        self.lineEdit_11.setText(tuition_id)
        self.timeEdit_14.setTime(record.value("usual_start_time"))
        self.spinBox_15.setValue(self.duration)
        self.doubleSpinBox_16.setValue(record.value("travel_distance"))
        self.spinBox_17.setValue(self.feesPH)
        self.doubleSpinBox_19b.setValue(self.ecost1_amount)
        self.doubleSpinBox_21b.setValue(self.ecost2_amount)
        self.doubleSpinBox_18.setValue(self.discount)
        self.doubleSpinBox_23b.setValue(self.totalCost)
        self.doubleSpinBox_22b.setValue(0.0)
        self.comboBox_19a.setCurrentIndex(self.comboBox_19a.findText(self.ecost1_type))
        self.comboBox_21a.setCurrentIndex(self.comboBox_21a.findText(self.ecost2_type))
        self.comboBox_22a.setCurrentIndex(self.comboBox_22a.findText("unused"))
        self.comboBox_24b.setCurrentIndex(self.comboBox_24b.findText(self.travelM))
        self.comboBox_25b.setCurrentIndex(self.comboBox_25b.findText(self.paymentM))
        self.comboBox_26b.setCurrentIndex(1)
        self.comboBox_28b.setCurrentIndex(1)
        
        #now we need the invoice_id, either from student_counters or we make a new one 
        if self.paymentM == "bank transfer" :  # bank transfer
            word = self.ifactory.get_invoice_id(self.student_idx)
            #print("_fill_form5: bank transfer selected. Word=", word)
            self.lineEdit_29b.setText(word) #set invoice id
            
        else: # anything but bank transfer
            self.lineEdit_29b.setText("") #no invoice_id needed
            #print("_fill_form5: bank transfer NOT selected")
    
    
    # check tuition record: see if tuition id exists
    def check_record(self,record):
        print("tuition check!")
        tutMod     = self.model.tuition
        size       = tutMod.rowCount()
        tutMod.sort(3,0)
        student_id = self.lcdNumber.intValue()
        #tuition_id = 
        
        for i in range(size,size-50,-1):
            tuition_id = tutMod.data3(i,"tuition_id")
            sid        = tutMod.data3(i,"last_name",False)
            if sid == student_id:
                print("Index: ",i,"   tuition id: ", tuition_id)
        
        
    
    # produce an QSqlTableRecord with the form data
    def fill_record(self):
        #self.tuition_record.setValue(0, self.lcdNumber.intValue()) #student_id
        ind                = self.comboBox_1.currentIndex()
        self.student_idx   = self.model.imap[ind]
        student_id         = self.student_idx+1
        self.tuition_record.setValue(0, self.lineEdit_11.text())           # tuition_id
        self.tuition_record.setValue(1, self.student_idx+1)                # first name
        self.tuition_record.setValue(2, self.student_idx+1)                # last name
        self.tuition_record.setValue(3, self.dateEdit_11.date())           # tuition date
        self.tuition_record.setValue(4, self.comboBox_13.currentText())    # tuition weekday
        self.tuition_record.setValue(5, self.timeEdit_14.time())           # start_time
        self.tuition_record.setValue(6, self.spinBox_15.value())           # duration
        self.tuition_record.setValue(7, self.doubleSpinBox_16.value())     # travel distance
        self.tuition_record.setValue(8, self.spinBox_17.value())           # fees_ph
        self.tuition_record.setValue(9, self.comboBox_19a.currentText())   # extra cost 1 type
        self.tuition_record.setValue(10, self.doubleSpinBox_19b.value())   # extra cost 1 amount
        self.tuition_record.setValue(11, self.comboBox_21a.currentText())  # extra cost 2 type
        self.tuition_record.setValue(12, self.doubleSpinBox_21b.value())   # extra cost 2 amount
        self.tuition_record.setValue(13, self.comboBox_22a.currentText())  # extra cost 3 type
        self.tuition_record.setValue(14, self.doubleSpinBox_22b.value())   # extra cost 3 amount
        self.tuition_record.setValue(15, self.doubleSpinBox_18.value())    # discount
        self.tuition_record.setValue(16, self.doubleSpinBox_23b.value())   # total cost
        self.tuition_record.setValue(17, self.comboBox_24b.currentText())  # travel method
        self.tuition_record.setValue(18, self.comboBox_25b.currentText())  # payment method
        self.tuition_record.setValue(19, self.comboBox_26b.currentText())  # payment received
        self.tuition_record.setValue(20, self.dateEdit_27b.date())         # payment date
        self.tuition_record.setValue(21, self.comboBox_28b.currentText())  # receipt completed
        self.tuition_record.setValue(22, self.lineEdit_29b.text())         # invoice_number
    
    
    
    
    
    # increase the student counter for student with student_id idx
    def inc_student_counter(self,idx):
        ind      = self.model.findStdcountKey(idx+1)
        counter  = self.model.stdcount.data3(ind,"student_counter")
        counter += 1
        self.model.stdcount.setData3(ind,"student_counter", counter)
        #print("student_idx ", idx, "Index ", index)
    
   
   
    # add the record from the dialog to the model.tuition
    def _add_tuition_record(self):
        self.fill_record()
        
        if self.tuition_record.value("payment_method") == "bank transfer": #we need to process invoice data
            if not self.ifactory.check_invoice(self.student_idx, self.tuition_record):
                QtWidgets.QMessageBox.information(self, "tuition record error", "tuition record was NOT added!",
                    QtWidgets.QMessageBox.Ok)
                return
        
        # insert the record from the dialog into the main table (not database yet)
        if self.model.tuition.insertRecord(-1, self.tuition_record):
            self.statusBar.showMessage("Tuition record successfully inserted in table", 3000)
        else:
            QtWidgets.QMessageBox.warning(self, "tuition record error", "tuition record could not be inserted in table",
                    QtWidgets.QMessageBox.Ok)
            
            
        # we need to increase the student counter
        self.inc_student_counter(self.student_idx)
        
        if self.tuition_record.value("payment_method") == "bank transfer": #we need to process invoice data
            tut_idx = self.model.tuition.rowCount()-1
            res     = self.ifactory.process_invoice(self.student_idx, tut_idx)
   
   
   
    
    # add the record from the dialog to the model.tuition
    def add_tuition_record(self):
        self._add_tuition_record()
        self.model.tuition.dirtyData = True
        self.accept()    
        self.done(0)
        self.test_for_receipts(settings.receipts_left)
        

    # add several records from the dialog to the model.tuition
    def add_more_tuition_record(self):
        self._add_tuition_record()
        self.model.tuition.dirtyData = True
        self._fill_form2()
        self.test_for_receipts(settings.receipts_left)


    # test if there are receipts left and brind up a message to report it
    def test_for_receipts(self, treshold, message=True):
        result      = []
        difference  = []
        total       = len(self.model.imap)
        studentMod  = self.model.student
        scountMod   = self.model.stdcount
        
        for i in self.model.imap:
            
            if (studentMod.data3(i,"usual_travel_method") == "no travel"):
                continue
            receipts    = scountMod.data3(i,"receipt_counter")
            sessions    = scountMod.data3(i,"student_counter")
            
            diff        = receipts-sessions
            if  (diff <= treshold):
                result.append(i)
                difference.append(diff)
        
        if message and len(result)>0:
            text  = ""
            text1 = "For {0} there are {1} receipts left.\n"
            text2 = "For {0} there is 1 receipt left.\n"
            #print("Result", result, "  ,Imap", self.model.imap, "  ,Difference", difference)
            for i in range(0,len(result)):
                j           = result[i]
                name        = scountMod.data3(j,"last_name")
                
                #print("test_for_receipts, name: ", name, "  ,  index", j, "  ,  difference", difference[i])
                if difference[i] == 1:
                    text   += text2.format(name)
                else:
                    text   += text1.format(name, difference[i])
            QtWidgets.QMessageBox.information( self, "receipts left", text, QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok )
        
        return result

