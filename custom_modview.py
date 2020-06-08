# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from HSqlTableModel  import  SqlList
import re

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


# my combo box that implements my helper tables
# it displays text but saves the number keys
class HComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(HComboBox,self).__init__(parent)
        super().setEditable(False)

    
    # use this for standard helper tables that have exactly
    # tow columns one called entry and one called word
    def populateItems(self, db, table):
        self.sList = SqlList(db, table, True)
        
        super().insertItems(0, self.sList.listB)


# This is a QDate Delegate
class dateDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(dateDelegate,self).__init__(parent)

    def createEditor(self,parent, option, index):
        editor = QtWidgets.QDateEdit(parent)
        editor.setCalendarPopup(True)
        editor.setDisplayFormat("dd/MM/yyyy")
        return editor
    
    def setModelData(self, editor, model, index):
        model.setData( index, editor.date(),  QtCore.Qt.EditRole )
        
    def setEditorData(self, editor, index):
        date = index.data()
        #print("setEditorData: ", date)
        editor.setDate(date)



# This is a QDate Trigger Delegate
# this is a Delegate particularly for the invoice_records.invoice_payment_date column
# it changes the tuition_records.payment_date
class dateTriggerDelegate(dateDelegate):
    invoice_paid_date_trigger = pyqtSignal(QtCore.QModelIndex, QtCore.QDate)
    
    def __init__(self, parent=None):
        super(dateDelegate,self).__init__(parent)
        
    # set Model Data from editor to model and emit signal
    def setModelData(self, editor, model, index):
        pdate  = editor.date()
        model.setData( index, pdate,  QtCore.Qt.EditRole )
        index2 = model.mapToSource(index) ## translate proxy index to original index
        self.invoice_paid_date_trigger.emit(index2, pdate)
        

# This is a QTime Delegate
class timeDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None, extended=False):
        super(timeDelegate,self).__init__(parent)
        self.extended = extended

    def createEditor(self,parent, option, index):
        editor = QtWidgets.QTimeEdit(parent)
        #editor.setCalendarPopup(True)
        if self.extended == True :
            editor.setDisplayFormat("HH:mm:ss")
        else :
            editor.setDisplayFormat("HH:mm")
        return editor
    
    
    ## C++ signature:paint( QPainter * painter, const QStyleOptionViewItem & option, const QModelIndex & index )
    def paint( self, painter, option, index ):
        if self.extended == False :
            super().paint(painter, option, index)
            return
        
        painter.save()
        if (option.state & QtWidgets.QStyle.State_Selected):
            painter.fillRect(option.rect, option.palette.highlight())
            #painter.setBrush(option.palette.light())
            painter.setPen(option.palette.light().color())

        time        = index.data()
        if not time == None:
            timestr     = time.toString("HH:mm:ss")
            center      = QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
            painter.drawText( option.rect, center, timestr )
        painter.restore()

    
    def setModelData(self, editor, model, index):
        model.setData( index, editor.time() )
        
    def setEditorData(self, editor, index):
        time = index.data()
        editor.setTime(time)


# This is a QComboBox Delegate that must be initated with
# a string list that make it's items
class comboDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, string_list, parent=None):
        super(comboDelegate,self).__init__(parent)
        self.__items = string_list

    def createEditor(self,parent, option, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems( self.__items)
        return editor
    
    def setModelData(self, editor, model, index):
        model.setData( index, editor.currentText(), QtCore.Qt.EditRole )
        
    def setEditorData(self, editor, index):
        word = index.data(QtCore.Qt.DisplayRole)
        ind  = editor.findText(word)
        editor.setCurrentIndex(ind)


# This is a QComboBox Delegate that must be initated with
# a string list that make it's items
class comboDelegate2(QtWidgets.QStyledItemDelegate):
    def __init__(self, tmodel, parent=None):
        super(comboDelegate2,self).__init__(parent)
        self.tmodel  = tmodel

    def createEditor(self,parent, option, index):
        col    = index.column()
        if not col in self.tmodel.rLib:
            return super().createEditor(parent, option, index)
        else:
            editor = QtWidgets.QComboBox(parent)
            editor.addItems(self.tmodel.rLib[col].getListB())
            return editor
    
    def setModelData(self, editor, model, index):
        col  = index.column()
        if not col in self.tmodel.rLib:
            super().setModelData(editor, model, index)
        else:
            model.setData( index, editor.currentText(), QtCore.Qt.EditRole )
        
    def setEditorData(self, editor, index):
        col  = index.column()
        if not col in self.tmodel.rLib:
            super().setEditorData(editor, index)
        else:
            word = index.data(QtCore.Qt.DisplayRole)
            ind  = editor.findText(word)
            editor.setCurrentIndex(ind)


# this is a Delegate particularly for the invoice_records.invoice_paid column
# it changes the invoice_paid_date
class ynTriggerDelegate(comboDelegate, QObject):
    invoice_paid_trigger = pyqtSignal(QtCore.QModelIndex, int)
    
    def __init__(self, hmodel, parent=None):
        self.choices = hmodel.helperLists["help_yesno"]
        super().__init__(self.choices, parent)
    
    def setModelData(self, editor, model, index):
        text   = editor.currentText()
        eindex = editor.currentIndex()
        orig   = model.data(index, QtCore.Qt.EditRole)
        index2 = model.mapToSource(index)
        
        if  text == orig:
            return
        
        row    = index2.row()
        print("text: ",text, "orig: ",orig, "row: ", row)
        self.invoice_paid_trigger.emit(index2, eindex)
        model.setData(index, text, QtCore.Qt.EditRole)
        

# This is a delegate for true/false or yes/no options
# it basically is a tick box, the underlying data is 0 or 1
class tickBoxDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(tickBoxDelegate,self).__init__(parent)
        #self.tickBox = QtWidgets.QCheckBox()
        self.sF      = 18  #scaleFactor
        
    def createEditor(self,parent, option, index):
        # return our tickBox as editor
        editor = QtWidgets.QCheckBox(parent)
        editor.setAutoFillBackground ( True )
        epal   = editor.palette()
        brush  = QtGui.QBrush(QtGui.QColor(255,255,255))
        epal.setBrush(QtGui.QPalette.Button, brush)
        editor.setPalette(epal)
        #print( "Background role: ", editor.backgroundRole() )
        return editor
    
    
    ## C++ signature:paint( QPainter * painter, const QStyleOptionViewItem & option, const QModelIndex & index )
    def paint( self, painter, option, index ):
        
        painter.save();

        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setPen(QtCore.Qt.SolidLine)
        
        # gives my the rectangle of the cell
        rect = option.rect        

        yOffset = (rect.height() - self.sF) / 2
        painter.translate(rect.x()+2, rect.y() + yOffset)
        
        painter.drawRoundedRect(0,0,self.sF, self.sF, 3,3)
        
        if index.data() == 1 :
            painter.fillRect(3,3,self.sF-6, self.sF-6, QtGui.QColor(0,0,0))

        painter.restore()


    def setModelData(self, editor, model, index):
        if editor.isChecked() :
            model.setData( index, 1 )
        else :
            model.setData( index, 0 )
        
        
    def setEditorData(self, editor, index):
        val = index.data()
        if val == 0 :
            editor.setChecked(False)
        else :
            editor.setChecked(True)
    
    
    # returns the minimum size we need
    def sizeHint(self, option, index ):
        #rect = option.rect
        return QtCore.QSize(self.sF, self.sF) 


## This class handles the invoice paid effects on the tuition_records table
class processInvoiceEffects(QObject):
    def __init__(self, model, parent):
        super().__init__(parent)
        self.model   = model   # this is my model class
        self.yesno   = self.model.helperLists["help_yesno"]    #["no","yes"]
        self.yncols  = [2 ,3]
        self.dcol    = 5
        self.irow    = 0
        self.icol    = 0
        
        
    @pyqtSlot(QtCore.QModelIndex, int)
    def handle_invoice_yn(self, index, ans):
        row            = index.row()
        col            = index.column()
        self.irow      = row
        self.icol      = col
        word           = self.yesno[ans]
        
        print("processInvoiceEffects, handle invoice yn: row: ", row, ", column: ", col)
        print("       ans: ", ans)
        
        if not col in self.yncols: 
            print("processInvoiceEffects: wrong column, nothing happens!")
            return
        ## set relevant invoice_record
        self.invoice_record = self.model.invoice.record(row)
        
        if   col == self.yncols[0]:
            self.set_invoice_sent_date(word)
        elif col == self.yncols[1]:
            self.set_invoice_paid_date(word)
            
            tuition_ids         = self._extract_tuition_ids(self.irow)
            for i in range(0, len(tuition_ids)):
                self.set_tuition_info(tuition_ids[i], word)
        

    #@pyqtSlot(QtCore.QModelIndex, QtCore.QDate)
    def handle_payment_date(self, index, date):
        irow        = index.row()
        icol        = index.column()
        
        #print("processInvoiceEffects, handle payment: row: ", irow, ", column: ", icol)
        
        # Is this the right column for the paid date
        if not icol == self.dcol: 
            print("processInvoiceEffects: wrong column, nothing happens!")
            return
    
        ## set relevant invoice_record
        tuition_ids         = self._extract_tuition_ids(irow)
    
        #print("tuition ids:", tuition_ids)
        for i in range(0, len(tuition_ids)):
            trow    = self.model.findTuitionKey(tuition_ids[i])
            self.model.tuition.setData3(trow, "payment_date", date )
    

    # make a list with tuition ids from a invoice_record
    def _extract_tuition_ids(self, irow):
        invMod          = self.model.invoice
        id_numbers      = invMod.data3(irow,"tuition_id_numbers")
        tuition_numbers = re.split('#', id_numbers)
        tuition_ids     = []
        pref            = invMod.data3(irow,"tuition_id_prefix")
        for i in range(0, len(tuition_numbers)):
            tuition_ids.append(pref+"{:03d}".format(int(tuition_numbers[i])))
        return tuition_ids
    

    # set payment data in tuition records
    def set_tuition_info(self, tuition_id, word):
        tutMod = self.model.tuition
        trow   = self.model.findTuitionKey(tuition_id)
        #print("set_tuition_info: ", word, " tuition_id: ", tuition_id)
        
        tutMod.setData3(trow, "payment_received", word)
        if word == "yes":
            tutMod.setData3(trow, "payment_date", QtCore.QDate.currentDate())
        else :
            tutMod.setData3(trow, "payment_date", QtCore.QDate(2000,1,1))
            
    
    # sets the invoice sent date in invoice_records
    def set_invoice_paid_date(self, ans):
        invMod = self.model.invoice
        if ans == "yes":
            #print("processInvoiceEffects: set sent date as default")
            invMod.setData3(self.irow, "invoice_paid_date", QtCore.QDate.currentDate())
        else :
            #print("processInvoiceEffects: set sent date as today")
            invMod.setData3(self.irow, "invoice_paid_date", QtCore.QDate(2000,1,1))
    

    # sets the invoice sent date in invoice_records
    def set_invoice_sent_date(self, ans):
        invMod = self.model.invoice
        if ans == "yes":
            #print("processInvoiceEffects: set sent date as default")
            invMod.setData3(self.irow, "invoice_send_date", QtCore.QDate.currentDate())
        else :
            #print("processInvoiceEffects: set sent date as today")
            invMod.setData3(self.irow,"invoice_send_date", QtCore.QDate(2000,1,1))
    
