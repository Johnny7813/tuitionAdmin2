from PyQt5 import QtCore, QtGui, QtSql, QtWidgets
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



# this is an extended version for QTableView
# adapted for HSqlTableModel, 
class HTableView(QtWidgets.QTableView):
    def __init__(self, parent):
        super().__init__(parent)
    
    #adapt this to take into account the
    #columns that are foreign keys, that are replaced
    def setModel(self,model):
        if isinstance(model, QtCore.QAbstractProxyModel):
            rLib = model.sourceModel().replacementLib()
        else:
            rLib = model.replacementLib()
        super().setModel(model)
        
        
        for i in rLib.keys():
            cdel = comboDelegate(rLib[i].listB, self)
            super().setItemDelegateForColumn(i, cdel)



