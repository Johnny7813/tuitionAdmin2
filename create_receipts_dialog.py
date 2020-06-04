# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_create_receipt_dialog.ui'
#
# Created by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5    import QtCore, QtGui, QtWidgets
from settings import *
from decimal  import *
import ui_create_receipts
import subprocess
import re
import os

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
class create_receipts_Dialog(QtWidgets.QDialog, ui_create_receipts.Ui_Dialog):
    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.model = model
        self.receipt_count = 2
        self.student_idx   = self.model.imap[0]
        self.student_id    = self.student_idx+1
        self.receipt_list  = ["2", "4", "6", "8", "10"]
        self.date_list     = []
        self.options       = dict(payment=True, transfer=True, year=True, minutes=False)
        self.year          = QtCore.QDate.currentDate().toString("yyyy")
        
        self.checkBox_1.setChecked(self.options['payment'])
        self.checkBox_2.setChecked(self.options['transfer'])
        self.checkBox_3.setChecked(self.options['year'])
        self.checkBox_4.setChecked(self.options['minutes'])
        
        self.comboBox_1.insertItems(0, self.model.lnames)
        self.comboBox_2.insertItems(0, self.receipt_list)
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        
        
        self.comboBox_2.currentIndexChanged.connect(self.set_receipt_count)
        self.comboBox_1.currentIndexChanged.connect(self.set_student_idx)
        self.pushButton_1.clicked.connect(self.add_date)
        self.pushButton_2.clicked.connect(self.delete_date)
        self.buttonBox.accepted.connect(self.create_receipts)
        
        self.set_receipt_count(0)


    # from weekly_schedule record calculate the correct payment amount
    # sidx is the index of the record in the schedule table (row index)
    def _get_payment_amount(self, sidx):
        schedule = self.model.schedule
        setcontext(Context(prec=60, rounding=ROUND_HALF_DOWN))
        fees_ph = Decimal(schedule.data3(sidx, "fees_ph"))
        self.duration = Decimal(schedule.data3(sidx, "duration"))
        extra_cost1 = schedule.data3(sidx, "extra_cost1_amount")
        extra_cost2 = schedule.data3(sidx, "extra_cost2_amount")
        discount = schedule.data3(sidx, "discount")
        amount = fees_ph * self.duration / Decimal(60) - Decimal(discount)
        amount += Decimal(extra_cost1) + Decimal(extra_cost2)

        remainder = amount % Decimal(1)
        if remainder == 0:
            amount_str = "{0:.0f}".format(amount)
        else:
            amount_str = "{0:.2f}".format(amount)

        return amount_str


    # from student_info record calculate the correct payment amount
    # idx is the row index in the student_info table
    def _get_payment_amount2(self, idx):
        student = self.model.student
        setcontext(Context(prec=60, rounding=ROUND_HALF_DOWN))
        fees_ph = Decimal(student.data3(idx, "fees_ph"))
        self.duration = Decimal( student.data3(idx, "usual_duration"))
        extra_cost1 = student.data3(idx, "extra_cost1_amount")
        extra_cost2 = student.data3(idx, "extra_cost2_amount")
        discount =  student.data3(idx, "discount")

        amount = fees_ph * self.duration / Decimal(60) + Decimal(extra_cost1)
        amount += Decimal(extra_cost2) - Decimal(discount)

        remainder = amount % Decimal(1)
        if remainder == 0:
            amount_str = "{0:.0f}".format(amount)
        else:
            amount_str = "{0:.2f}".format(amount)

        return amount_str
        
        
    # assemble date from the dialog in variables
    def _assemble_data(self):
        self.options['payment']  = self.checkBox_1.isChecked()
        self.options['transfer'] = self.checkBox_2.isChecked()
        self.options['year']     = self.checkBox_3.isChecked()
        self.options['minutes']  = self.checkBox_4.isChecked()
        student = self.model.student  # abbreviation
        i = self.comboBox_2.currentIndex()
        self.receipt_count = int(self.receipt_list[i])
        
        ## read data from student_info
        std_index = self.model.findStudentKey(self.student_id)
        assert (std_index >= 0), "Student index could not be found!"
        
        ## read data from weekly_schedule
        sch_index = self.model.findScheduleKey2(self.student_id)
        #print("schedule index: ", sch_index)
        #print("student index: ", std_index)
        if sch_index < 0 :  # index not found
            self.amount           = self._get_payment_amount2(std_index)
            pre_address           = student.data3(std_index, "address")
        else:
            ## test for a different schedule entry for this student
            sch_index2 = self.model.findScheduleKey2(self.student_id, sch_index+1)
            if sch_index2 >= 0:
                # more than one schedule entry for this student -> we don't print the amount
                self.options['pay'] = False
            self.amount           = self._get_payment_amount(sch_index)
            pre_address           = self.model.schedule.data3(sch_index, "address")
        
        
        self.last_name        = student.data3(std_index, "last_name")
        pre_name              = student.data3(std_index, "first_name") + " " + self.last_name
        pre_name              = re.sub("&", "and", pre_name)
        
        pre_prefix            = student.data3(std_index, "tuition_id_prefix")
        self.postcode         = student.data3(std_index, "postcode")
        self.prefix           = re.sub("\_", "\\_", pre_prefix)
        self.name             = re.sub("\_", "\\_", pre_name)
        self.address          = re.sub("(.{20,30}),","\\1,\\\\\\\\ & ", pre_address) 
        
        # read in the student counter
        cindex                = self.model.findStdcountKey(self.student_id)
        counter_rec           = self.model.stdcount.record(cindex)
        self.base_num         = counter_rec.value("receipt_counter")
        self.base_num = self.model.stdcount.data3(cindex, "receipt_counter")
        return True

    
    # update the value of the receipt_counter in student_counters
    def _update_receipt_counter(self):
        cindex                = self.model.findStdcountKey(self.student_id)
        counter_rec           = self.model.stdcount.record(cindex)
        receipt_counter       = counter_rec.value("receipt_counter")
        receipt_counter      += self.receipt_count
        counter_rec.setValue("receipt_counter", receipt_counter)
        self.model.stdcount.setRecord(cindex, counter_rec)
    
    
    
    # set the receipt_count variable
    def set_receipt_count(self, c):
        #self.receipt_count = 2*(int(c)+1)
        self.receipt_count = int(self.receipt_list[c])
        
        

    # sets student_id and student_idx
    def set_student_idx(self, c):
        self.student_idx = self.model.imap[c]
        self.student_id  = self.student_idx+1
        
    
    def add_date(self):
        cdate = self.dateEdit.date()
        
        if len(self.date_list)>=1 :
            ldate = self.date_list[-1]
            if cdate <= ldate :
                QtWidgets.QMessageBox.information( self, "insertion", "New date must be later then last date!", 
                                                            QtWidgets.QMessageBox.Ok)
                return
            
        self.date_list.append(cdate)
        self.listWidget.addItem(cdate.toString("dddd, dd MMMM yyyy"))
    
    
    
    def delete_date(self):
        ilist    = self.listWidget.selectedIndexes()
        if len(ilist) == 0:
            QtWidgets.QMessageBox.information( self, "selection", "You need to select the element you want to delete!", 
                                           QtWidgets.QMessageBox.Ok)
            return
        
        selected = ilist[0].row()
        self.listWidget.takeItem(selected)
        self.date_list.pop(selected)
        
        print("You have chosen Element:", selected)
        
        
    
    
    def _create_receipt_table(self, di):
        
        # create the tex date string
        if di < len(self.date_list) :
            date_str = self.date_list[di].toString("dd/MM/yyyy")
        elif self.options['year'] :
            date_str = "\\rule{{1cm}}{{0.6pt}}/\\rule{{1cm}}{{0.6pt}}/{0}".format(self.year)
        else :
            date_str = "\\rule{1cm}{0.6pt}/\\rule{1cm}{0.6pt}/\\rule{1cm}{0.6pt}"
        
        num          = self.base_num + di
        tuition_id   = self.prefix + "{0:03d}".format(int(num))
        
        tstring      = "\\begin{Large}\n\\begin{tabular}{p{8cm}p{8cm}}\n"
        tstring     += "unique tuition id: & {0} \\\\\n".format(tuition_id)
        tstring     += "name of tutor: &  Hannes Buchholzer \\\\\n"
        tstring     += "name of student: &  {0} \\\\\n".format(self.name)
        tstring     += "address where tuition given: & {0}, {1} \\\\\n".format(self.address, self.postcode)
        tstring     += "date of tuition given: & {0}  \\\\\n".format(date_str)
        tstring     += "duration of a lesson: & "
        if  self.options["minutes"] :     tstring += "{0:.0f} minutes \\\\\n".format(self.duration)
        else :                            tstring += " \\rule{1cm}{0.6pt}0 minutes \\\\\n"
        tstring     += "tuition fee amount: &  £ " 
        if  self.options["payment"] :     tstring += "{0} \\\\\n".format(self.amount)
        else :                            tstring += "\\rule{1.5cm}{0.6pt} \\\\\n"
        if  not self.options["transfer"]: tstring += "amount paid: &  £ \\rule{1.5cm}{0.6pt} \\\\\n"
        else :                            tstring += "payment  &  by bank transfer \\\\\n"
        tstring     += "signature of student/parent: &  \\rule{6cm}{0.6pt} \\\\\n"
        tstring     += "signature of tutor: &  \\rule{6cm}{0.6pt} \\\\\n"
        tstring     += "\\end{tabular}\n\\end{Large}\n"
        
        return tstring
        
    
    
    def create_receipt_string(self):
        fixed   = [ 
                 "\\documentclass[12pt,english]{scrreprt}\n\\areaset{20cm}{26cm}\n"
               + "\\linespread{1}\n\\usepackage[T1]{fontenc}\n\\usepackage[utf8]{inputenc}\n"
               + "\\usepackage{longtable}\n\\usepackage{babel}\n\\pagestyle{empty}\n"
               + "\\setparsizes{0pt}{0pt}{0pt}\n\\flushbottom\n\\begin{document}\n" ,
                 "\\begin{center}\n\\vspace*{1.5cm}\n"
               + "{\\Huge \\bfseries   tuition fee receipt for maths tuition }\n\\vspace{1cm}\n" ,
                 "\\vfill\n\\begin{center}\n"
               + "{\\Huge \\bfseries  tuition fee receipt for maths tuition }\n\\vspace{1cm}\n" ,
                 "\\newpage\n" ,
                 "\\end{document}\n\n" ,
                 "\\end{center}\n\n" ]
        
        # assemble the string
        rstring = fixed[0]
        
        k  = 0
        rc = int(self.receipt_count/2)
        for i in range(0, rc) :
            if i > 0 : rstring += fixed[3]
            rstring += fixed[1]
            rstring += self._create_receipt_table(k)
            k       += 1
            rstring += fixed[5]
            rstring += fixed[2]
            rstring += self._create_receipt_table(k)
            rstring += fixed[5]
            k       += 1
  
        rstring += fixed[4]
        return rstring

    
    def create_receipts(self):
        res = self._assemble_data()
        if res == False:  #error in assembling data, no schedule entry found
            i    = self.comboBox_1.currentIndex()
            name = self.model.lnames[i]
            QtWidgets.QMessageBox.warning( self, "no schedule entry", "No schedule entry found for {0:s}!".format(name))
            return
        
        receipt_tex  = self.create_receipt_string()
        #print("Receipt string \n:", receipt_tex)
        
        output_dir   = settings.receipt_dir
        fname        = output_dir + "/tuition-fee_receipt-{}.tex".format(self.last_name)
        fname2       = re.sub("tex","pdf",fname)
        
        fhandle      = open(fname, 'w')
        fhandle.write(receipt_tex)
        fhandle.close()
        
        os.chdir(output_dir)
        
        exitcode = subprocess.call(["/usr/bin/pdflatex", fname])
        if exitcode==0 :
            
            okular = subprocess.Popen(["/usr/bin/okular", fname2])
            ans    = QtWidgets.QMessageBox.information( self, "keep receipt?", "Mark this receipt as created?", 
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
            if ans == QtWidgets.QMessageBox.Yes :
                self._update_receipt_counter()
        
        return
        
    
  
        
        
