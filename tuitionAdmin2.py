#! /usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtSql
import ui_tuitionAdmin2
import add_car_mileage_dialog
import add_tuition_dialog
import add_student_dialog
import add_schedule_dialog
import edit_invcount_dialog
import create_receipts_dialog
import view_student_info_dialog
import view_student_counters_dialog
import summary_dialog
import send_reminder
import invoice_factory
import backup_factory
from   custom_modview import *
from   Hmodel import *
from   settings import *
from   time_recording import *
import sys


__version__ = "2.0.1"


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



# multiple inheritance
class MainWindow(QtWidgets.QMainWindow, ui_tuitionAdmin2.Ui_MainWindow):
    def __init__(self, desktop):
        super(MainWindow, self).__init__()
        QtCore.QCoreApplication.addLibraryPath(".")
        self.setupUi(self)
        
        self.dev_version    = settings.dev_version
        if self.dev_version :
            self.setWindowTitle(_translate("MainWindow", "TuitionAdmin2 Development", None))
        else :
            self.setWindowTitle(_translate("MainWindow", "TuitionAdmin2 Deployed", None))
            
        self.desktop        = desktop
        #creating models and views    
        self.model          = HModel( self.statusBar()) 
        self.setupTableViews()
        # create time recording object
        self.time_rec = time_recording(self.model, self.desktop, self)
        #START backup process to make regular updates
        self.backup   = backup_factory.backup_Factory( self.statusBar() )
        
        # connect signals and slots
        #self.actionAdd_car_mileage.triggered().connect(self.add_car_mileage)
        self.actionAdd_car_mileage.triggered.connect(self.add_car_mileage)
        self.actionFilter_stdcounters.triggered.connect(self.filter_student_counters)
        self.actionAdd_tuition_record.triggered.connect(self.add_tuition)
        self.actionAdd_student_record.triggered.connect(self.add_student)
        self.actionAdd_schedule_entry.triggered.connect(self.add_schedule)
        self.actionCommit_all.triggered.connect(self.saveAll)
        self.actionCreate_receipts.triggered.connect(self.create_receipts)
        self.actionAbout_tuitionAdmin.triggered.connect(self.about_tuitionAdmin)
        self.actionAbout_Qt.triggered.connect(QtWidgets.QApplication.aboutQt)
        self.actionDelete_row.triggered.connect(self.delete_row)
        self.actionAdd_row.triggered.connect(self.add_row)
        self.actionReload_all.triggered.connect(self.reloadAll)
        self.actionShow_invoice_counter.triggered.connect(self.edit_invcount)
        self.actionSend_invoice.triggered.connect(self.send_invoice)
        self.actionCreate_invoice.triggered.connect(self.printTable)
        self.actionDisplay_summary.triggered.connect(self.create_summary)
        self.actionShow_student_info.triggered.connect(self.show_student_info)
        self.actionShow_student_counters.triggered.connect(self.show_student_counters)
        self.actionTime_Recording.toggled.connect(self.time_rec.started)
        self.actionMaking_Backups.toggled.connect(self.backup.run)
        self.actionCheck_records.triggered.connect(self.check_records)
        self.time_rec.lock_tick.connect(self.actionTime_Recording.setDisabled)
        self.time_rec.checked.connect(self.actionTime_Recording.setChecked)
        self.actionSend_reminders.triggered.connect(self.send_reminders)
        
        self.statusBar().showMessage("Ready", 3000)
        self.start_time_recording()
        self.tabWidget.setCurrentIndex(3)

    
    # should we start time recording when the programms start
    def start_time_recording(self):
        if settings.time_recording :
            self.time_rec.start()
            self.actionTime_Recording.setChecked(True)
            self.actionTime_Recording.setDisabled(True)
    
    
    # show student_info in a separate window
    def show_student_info(self):
        view_student_info = view_student_info_dialog.view_student_info_Dialog(self.model, self)
        view_student_info.exec()
        
    
    # show student counters in a separate window
    def show_student_counters(self):
        view_student_counters = view_student_counters_dialog.view_student_counters_Dialog(self.model, self)
        view_student_counters.exec()
    

    def setupTableViews(self):
        # create custom delegates for some columns of the tableView
        dateDel       = dateDelegate(self)
        yesnoDel      = comboDelegate(self.model.helperLists["help_yesno"], self)
        #timeDel       = timeDelegate(self)
        timeExtDel    = timeDelegate(self, True)
        yesnoTrigDel  = ynTriggerDelegate(self.model, self)
        dateTrigDel   = dateTriggerDelegate(self)
        tickBoxDel    = tickBoxDelegate(self)
        #nameDel       = comboDelegate(self.model.lnames, self)
        
        # delegate for a whole HSqlTableModel
        tuitionDel    = comboDelegate2(self.model.tuition, self)
        studentDel    = comboDelegate2(self.model.student, self)
        mileageDel    = comboDelegate2(self.model.mileage, self)
        scheduleDel   = comboDelegate2(self.model.schedule, self)
        invoiceDel    = comboDelegate2(self.model.invoice, self)
        
        
        process_ieffect = processInvoiceEffects(self.model, self)
        yesnoTrigDel.invoice_paid_trigger.connect(process_ieffect.handle_invoice_yn)
        dateTrigDel.invoice_paid_date_trigger.connect(process_ieffect.handle_payment_date)
        
        
        # TableView for student_info
        student_proxy  = QtCore.QSortFilterProxyModel(self)
        student_proxy.setSourceModel(self.model.student)
        self.student_view.setModel(student_proxy)
        self.student_view.resizeColumnsToContents()
        self.student_view.sortByColumn (0, QtCore.Qt.AscendingOrder )
        self.student_view.setSortingEnabled(True)
        self.student_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.student_view.setItemDelegate(studentDel)
        self.student_view.horizontalHeader().setFixedHeight(60)
        
        
        
        
        # setup TableView for student_counters table
        self.stdcount_proxy  = QtCore.QSortFilterProxyModel(self)
        self.stdcount_proxy.setSourceModel(self.model.stdcount)
        self.stdcount_view.setModel(self.stdcount_proxy)
        self.stdcount_view.resizeColumnsToContents()
        self.stdcount_view.setEditTriggers(QtWidgets.QAbstractItemView.CurrentChanged)
        self.stdcount_view.sortByColumn (0, QtCore.Qt.AscendingOrder )
        self.stdcount_view.setSortingEnabled(True)
        self.stdcount_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.stdcount_view.resizeColumnsToContents()
        # hide unnecessary rows
        self.filter_student_counters()
        self.stdcount_view.horizontalHeader().setFixedHeight(60)
        
        
        
        # TableView for weekly_schedule
        schedule_proxy  = QtCore.QSortFilterProxyModel(self)
        schedule_proxy.setSourceModel(self.model.schedule)
        #self.schedule_view.setModel(self.model.schedule)
        self.schedule_view.setModel(schedule_proxy)
        self.schedule_view.sortByColumn (0, QtCore.Qt.AscendingOrder )
        self.schedule_view.setSortingEnabled(True)
        self.schedule_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.schedule_view.setItemDelegate(scheduleDel)
        self.schedule_view.resizeColumnsToContents()
        self.schedule_view.horizontalHeader().setFixedHeight(60)
        self.schedule_view.scrollToBottom()
        
        
        
        # TableView for vehicle mileage
        mileage_proxy  = QtCore.QSortFilterProxyModel(self)
        mileage_proxy.setSourceModel(self.model.mileage)
        self.mileage_view.setModel(mileage_proxy)
        self.mileage_view.sortByColumn (0, QtCore.Qt.AscendingOrder )
        self.mileage_view.setSortingEnabled(True)
        self.mileage_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.mileage_view.setItemDelegateForColumn(1, dateDel)
        self.mileage_view.setItemDelegate(mileageDel)
        self.mileage_view.resizeColumnsToContents()
        self.mileage_view.horizontalHeader().setFixedHeight(60)
        self.mileage_view.scrollToBottom()
        
        
        # setup TableView for tuition_records table
        tuition_proxy  = QtCore.QSortFilterProxyModel(self)
        tuition_proxy.setSourceModel(self.model.tuition)
        self.tuition_view.setModel(tuition_proxy)
        self.tuition_view.resizeColumnsToContents()
        self.tuition_view.sortByColumn (4, QtCore.Qt.AscendingOrder )
        self.tuition_view.setSortingEnabled(True)
        self.tuition_view.sortByColumn (3, QtCore.Qt.AscendingOrder )
        self.tuition_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tuition_view.setItemDelegate(tuitionDel)
        self.tuition_view.horizontalHeader().setFixedHeight(60)
        self.tuition_view.scrollToBottom()
        
        
        # setup TableView for invoice_records table
        invoice_proxy  = QtCore.QSortFilterProxyModel(self)
        invoice_proxy.setSourceModel(self.model.invoice)
        self.invoice_view.setModel(invoice_proxy)
        self.invoice_view.resizeColumnsToContents()
        self.invoice_view.setItemDelegate(invoiceDel)
        self.invoice_view.setItemDelegateForColumn(2, yesnoTrigDel)
        self.invoice_view.setItemDelegateForColumn(3, yesnoTrigDel)
        self.invoice_view.setItemDelegateForColumn(4, dateDel)
        self.invoice_view.setItemDelegateForColumn(5, dateTrigDel)
        self.invoice_view.sortByColumn (0, QtCore.Qt.AscendingOrder )
        self.invoice_view.setSortingEnabled(True)
        self.invoice_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.invoice_view.horizontalHeader().setFixedHeight(60)
        self.invoice_view.scrollToBottom()
        
        
        # setup TableView for time_recording table
        time_proxy  = QtCore.QSortFilterProxyModel(self)
        time_proxy.setSourceModel(self.model.time)
        self.time_view.setModel(time_proxy)
        self.time_view.resizeColumnsToContents()
        self.time_view.setItemDelegateForColumn(1, dateDel)
        self.time_view.setItemDelegateForColumn(2, timeExtDel)
        self.time_view.setItemDelegateForColumn(4, timeExtDel)
        #self.time_view.sortByColumn (0, QtCore.Qt.AscendingOrder )
        #self.time_view.setSortingEnabled(True)
        self.time_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.time_view.horizontalHeader().setFixedHeight(60)
        self.time_view.scrollToBottom()
        
        # setup TableView for reminder_records
        reminder_proxy  =  QtCore.QSortFilterProxyModel(self)
        reminder_proxy.setSourceModel(self.model.reminder) 
        self.reminder_view.setModel(reminder_proxy)
        self.reminder_view.resizeColumnsToContents()
        self.reminder_view.setColumnWidth(4,120)
        self.reminder_view.setItemDelegateForColumn(4, dateDel)
        
        
        
    def add_car_mileage(self):
        self.tabWidget.setCurrentIndex(6)
        add_car_mileage_form = add_car_mileage_dialog.add_mileage_Dialog(self.model, self)
        add_car_mileage_form.exec()
        
        
    def add_tuition(self):
        self.tabWidget.setCurrentIndex(3)
        add_tuition_form = add_tuition_dialog.add_tuition_Dialog(self.model,  self)
        add_tuition_form.exec()


    def add_student(self):
        self.tabWidget.setCurrentIndex(0)
        add_student_form = add_student_dialog.add_student_Dialog(self.model, self)
        add_student_form.exec()
        self.model.make_active_list()
    
    
    def add_schedule(self):
        self.tabWidget.setCurrentIndex(2)
        add_schedule_form= add_schedule_dialog.add_schedule_Dialog(self.model, self)
        add_schedule_form.exec()
    
    
    
    # filter student counters for active students
    def filter_student_counters(self):
        # hide unnecessary rows
        for i in range(0,self.model.stdcount.rowCount()):
            ind = self.stdcount_proxy.index(i,0)
            #print("stdcount", self.model.stdcount.data(ind, 0))
            s   = int(self.model.stdcount.data(ind, 0))
            if s not in self.model.active_student_ids:
                self.stdcount_view.hideRow(i)
                
    
    # create create receipts dialog
    def create_receipts(self):
        create_receipts_form = create_receipts_dialog.create_receipts_Dialog(self.model, self)
        create_receipts_form.exec()
    
    
    # create summary dialog
    def create_summary(self):
        summary_form = summary_dialog.summary_Dialog(self.model, self)
        summary_form.exec()
    
    
    def edit_invcount(self):
        edit_invcount_form = edit_invcount_dialog.edit_invcount_Dialog(self.model, self)
        edit_invcount_form.exec()
    
    
    # delete a row in one of the tables
    def delete_row(self):
        #i      = self.tabWidget.currentIndex()
        view   = self.tabWidget.currentWidget().findChild(QtWidgets.QTableView)
        ilist  = view.selectedIndexes()
        
        print("Delete row called!")
        if len(ilist) == 0:
            QtWidgets.QMessageBox.information(self, "No Selection", "You need to select the row you want to delete!", QtWidgets.QMessageBox.Ok )
        
        else :
            proxy = view.model()
            model = proxy.sourceModel()
            row   = proxy.mapToSource(ilist[0]).row()
            ans   = QtWidgets.QMessageBox.information(self, "Delete row", 
                      "Do you really want to delete row {0}?".format(row+1), QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No )
            if ans == QtWidgets.QMessageBox.Yes :
                #model.translate = False
                model.removeRows(row, 1)
                #model.translate = True
                
    
    
    # add a row in one of the tables, with heuristic generic values
    def add_row(self):
        view   = self.tabWidget.currentWidget().findChild(QtWidgets.QTableView)
        
        if view == None :
            QtWidgets.QMessageBox.information(self, "Error", "View selection error!", QtWidgets.QMessageBox.Ok )
            return
        
        proxy   = view.model()
        model   = proxy.sourceModel()  # we have found the model
        
        if model == self.model.time :
            self.time_rec.new_time_record()
        else :
            QtWidgets.QMessageBox.information(self, "Incomplete!", "This function is not yet implemented!", QtWidgets.QMessageBox.Ok )
    
    
    #send an invoice for marked row in the invoice records table
    def send_invoice(self):
        ilist  = self.invoice_view.selectedIndexes()
        invfac = invoice_factory.invoice_factory(self.model, self)
        
        if len(ilist) == 0:
            QtWidgets.QMessageBox.information(self, "No Selection", 
                      "You need to select the row for which you want to send the invoice!", QtWidgets.QMessageBox.Ok )
        
        else :
            proxy = self.invoice_view.model()
            row   =  proxy.mapToSource(ilist[0]).row()
            ans   = QtWidgets.QMessageBox.information(self, "Send Invoice", 
                      "Do you You want to produce an invoice for row {0}?".format(row+1), 
                            QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No )  
            if ans == QtWidgets.QMessageBox.Yes:
                invfac.send_invoice(row)
    
    
    
    # check for and send reminders
    def send_reminders(self):
        #print("send reminders executed!")
        reminder_form = send_reminder.send_reminder_Dialog(self.model, self)
        reminder_form.exec()
    
    
    
    # check if invoice payments have been put in correctly in tuition records
    def check_records(self):
            invfac = invoice_factory.invoice_factory(self.model, self)
            res    = invfac.check_paid_invoice_carry_over()


    # print table
    def printTable(self):
        i      = self.tabWidget.currentIndex()
        name   = self.model.tab[i].tableName()
        self.model.dump_model(i)
    
    
    def saveAll(self):
        error_str = ""
        total_ok  = True
        size      = len(self.model.tab)
        
        for i in range(0,size):
            if self.model.tab[i].dirtyData:
                ok = self.model.tab[i].submitAll()
                if not ok:  
                    total_ok   = False
                    error_str += self.model.tab[i].lastError().text()
                else:
                    self.model.tab[i].dirtyData = False
                    #self.model.dump_model(i)
       
        if total_ok:
             self.statusBar().showMessage("All tables successfully stored in database!", 3000)
        else :
            QtWidgets.QMessageBox.warning(self, "SQL Error", error_str, QtWidgets.QMessageBox.Ok )
        
        self.filter_student_counters()

        
    
    def reloadAll(self):
        total_ok = True
        size     = len(self.model.tab)
        for i in range(0,size):
            ok = self.model.tab[i].select()
            if ok:
                self.model.tab[i].dirtyData=True
            else:
                total_ok = False
        if total_ok:
            self.statusBar().showMessage("All tables reloaded from database", 3000)
        # set up everything again
        self.model.make_active_list()
        self.filter_student_counters()
    
    
    def about_tuitionAdmin(self):
        text   = "This is tuitionAdmin2 programmed by Hannes Buchholzer.\n"
        text  += "This is version " + __version__ + "\n";
        text  += "This is a new development version with new technology that is currently rewritten.\n"
        text  += "This Version has student_info and student_counters as seperate dialog windows.\n"
        text  += "Time Recording is implemented in this version.\n"
        text  += "But Sqlite is not yet implemented.\n"
        text  += "This program uses the mysql database: '" + settings.database + "'"
        QtWidgets.QMessageBox.information(self,"About tuitionAdmin", text, QtWidgets.QMessageBox.Ok)


    # deal with the close event
    def closeEvent(self, event):
               
        if self.model.hasUnsavedData() :
            ans = QtWidgets.QMessageBox.question( self, "Save data?", "There is unsaved data, do you want to save it?" , 
                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel, QtWidgets.QMessageBox.Yes)
            if    ans == QtWidgets.QMessageBox.Yes :
                self.saveAll()
                event.accept()
            elif  ans == QtWidgets.QMessageBox.Cancel :
                event.ignore()
            elif  ans == QtWidgets.QMessageBox.No :
                event.accept()
        else :
            event.accept()
        
        # do a final backup when programm exits
        if self.backup.active:
            self.backup.execute()


if __name__ == "__main__":
    app     = QtWidgets.QApplication(sys.argv)
    desktop = app.desktop()
    
    main = MainWindow(desktop)
    main.show()
    
    app.exec_()

sys.exit(0)
