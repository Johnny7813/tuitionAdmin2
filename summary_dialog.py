# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
import  ui_summary
#from    settings import settings
#import  re
#import  sys


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
class summary_Dialog(QtWidgets.QDialog, ui_summary.Ui_Dialog):
    def __init__(self, model, parent=None):
        super(summary_Dialog, self).__init__(parent)
        self.setupUi(self)
        
        self.model          = model
        labels              = ["month", "tutoring\nincome", "business\nmileage",
                               "private\nmileage", "preparation\nhours"]
        
        self.tableWidget.setRowCount(6);
        self.tableWidget.setColumnCount(5);
        
        self.tableWidget.setColumnWidth(0,145)
        self.tableWidget.setColumnWidth(1,100)
        self.tableWidget.setColumnWidth(2,100)
        self.tableWidget.setColumnWidth(3,100)
        self.tableWidget.setColumnWidth(4,100)
        self.tableWidget.setHorizontalHeaderLabels(labels)
        
        self.populate()
        
    # populate table
    def populate(self):
        today = QtCore.QDate.currentDate()
        
        date   = QtCore.QDate(today.year(), today.month(), 1)
        date   = date.addMonths(-5)
        print("Date:", date.toString("dd.MM.yyyy") )
        income               = self.calculate_income(date)
        [busi_mil, priv_mil] = self.calculate_mileage(date)
        hours                = self.calculate_prep_hours(date)
        
        for i in range(0,6):
            self.tableWidget.setItem(i,0,QtWidgets.QTableWidgetItem(date.toString("MMMM yy")))
            self.tableWidget.setItem(i,1,QtWidgets.QTableWidgetItem("{0:.1f}".format(income[i])))
            self.tableWidget.setItem(i,2,QtWidgets.QTableWidgetItem("{0:.1f}".format(busi_mil[i])))
            self.tableWidget.setItem(i,3,QtWidgets.QTableWidgetItem("{0:.1f}".format(priv_mil[i])))
            self.tableWidget.setItem(i,4,QtWidgets.QTableWidgetItem("{0:.1f}".format(hours[i])))
            date = date.addMonths(1)
    
    
    # find how many months away date is from rdate where date>bdate
    # where bdate is the minimal base date
    def _find_month(self, bdate, date):
        if date < bdate: return -1
        
        bm  = bdate.month()
        m   = date.month()
        by  = bdate.year()
        y   = date.year()
        
        if y==by:     return m-bm
        elif y==by+1: return m+(12-bm)
        else:         return -1
    
    
    # calculate income summary
    def calculate_income(self,bdate):
        sums  = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        rows  = self.model.tuition.rowCount()
        
        for i in range(0,rows):
            rec   = self.model.tuition.record(i)
            rdate = rec.value("tuition_date")
            val   = rec.value("total_cost")
            
            m     = self._find_month(bdate, rdate)
            if m<0 or m>5 : continue
            sums[m] += val
            
                
        print("Sums:", sums)
        return sums
        
        
    # calculate mileage summary
    def calculate_mileage(self,bdate):
        # find right index
        
        bsums  = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        psums  = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
         
        rows  = self.model.mileage.rowCount()
        
        for i in range(0,rows):
            rec   = self.model.mileage.record(i)
            rdate = rec.value("travel_date")
            
            m     = self._find_month(bdate, rdate)
            if m<0 or m>5 : continue
        
            start = rec.value("start_mileage")
            end   = rec.value("end_mileage")
            why   = rec.value("category")
            val   = end - start
            
            if why=="business": bsums[m] += val
            if why=="private" : psums[m] += val 
            
        return [bsums, psums]
            

    # calculate preparation hours
    def calculate_prep_hours(self,bdate):
        hours  = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        rows  = self.model.time.rowCount()
        
        for i in range(0,rows):
            rec   = self.model.time.record(i)
            rdate = rec.value("start_date")
            
            m     = self._find_month(bdate, rdate)
            if m<0 or m>5 : continue
        
            mins      = rec.value("time_span")
            hours[m] += round(mins/60.0,2)
            
        return hours

        
        
