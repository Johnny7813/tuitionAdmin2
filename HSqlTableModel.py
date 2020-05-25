# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtSql
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


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


    
############################################################################


# a list with pairs made from two columns
# from a table from a database
# FIXME: maybe self.active and self.headerChanged should not be in here
class SqlList:
    # 
    def __init__(self, db, table, active, colA="entry", colB="word"):
        self.active = active
        if colA == "entry":
            self.headerChanged = False
        else:
            self.headerChanged = True
            
        self.colA = colA
        self.colB = colB
        qtext  = "SELECT {0},{1} FROM {2}".format(colA,colB,table)
        query  = QtSql.QSqlQuery(qtext, db)
        
        self.listA = []
        self.listB = []
        
        while (query.next()):
            a = query.value(0)
            b = query.value(1)
            self.listA.append(a)
            self.listB.append(b)
    
    def headerChanged(self):
        return self.headerChanged
    
    def isActive(self):
        return self.active
    
    def setActive(self,val):
        self.active = val
    
    def getBatAval(self, val):
        if val in self.listA:
            i = self.listA.index(val)
            return self.listB[i]
        else:
            return None
    
    def getAatBval(self, val):
        if val in self.listB:
            i = self.listB.index(val)
            return self.listA[i]
        else:
            return None
    
    def getAatInd(self,i):
        return self.listA[i]

    def getBatInd(self,i):
        return self.listB[i]
    
    def getPairAt(self,i):
        a = self.listA[i]
        b = self.listB[i]
        return (a,b)
    
    def addPair(self,entry,word):
        self.listA.append(entry)
        self.listB.append(word)
    
    def getListA(self):
        return self.listA
    
    def getListB(self):
        return self.listB
    
    def print(self):
        print("SqlList:")
        print("list A: ", self.listA)
        print("list B: ", self.listB)




#origRole = 17


#This is new TableModel
#It allows for one column to be none editable
#It allows for one column to be replaced by another
class HSqlTableModel(QtSql.QSqlTableModel):
    def __init__(self, parent, db):
        super().__init__(parent, db)
        self.translate  = True
        self.debug      = False
        self.dirtyData  = False
        self.rLib       = dict()  # this dict contains the replace info
        self.db         = db
        self.memory     = None    # copy of translate to save for later

    #TODO: do I still need the next few functions
    # set translate to true or false
    # this refers to translate return value for data() with editRole
    def setTranslate(self,b):
        pass
        #self.translate = b
    
    ## return the actual translate value
    def getTranslate(self):
        pass
        #return self.translate
    
    ## set translate value and save original value
    def setMemoryTranslate(self,b):
        pass
        #self.memory    = self.translate
        #self.translate = b
        
    def restoreMemoryTranslate(self):
        pass
        #if self.memory == None:
        #    print("Error in HSqlTableModel.restoreMemoryTranslate: ")
        #    print("memory should not be None!")
        #else:
        #    self.translate = self.memory
        #    self.memory    = None
    

    #in current table and column ind, replace from str_table, column str_fieldA with str_fieldB
    def setReplacement(self, ind, str_table, str_fieldA, str_fieldB, active=False):
        slist          = SqlList(self.db,str_table, active, colA=str_fieldA, colB=str_fieldB)
        self.rLib[ind] = slist
        self.replace   = True
    
    # a shorter version for helper tables,
    def setReplacement2(self, ind, str_table, active=False):
        slist          = SqlList(self.db,str_table, active)
        self.rLib[ind] = slist
        self.replace   = True


    # return the keys from the internal replacement lib 
    # these are the columns that are replaced
    def replacementKeys(self):
        return self.rLib.keys()
    
    # return the whole rLib
    def replacementLib(self):
        return self.rLib

    # mark a column as active or passive i.e. editable or
    # not editable
    def flags(self, modind):
        fl  = super().flags(modind)
        col = modind.column()
        if col in self.rLib:
            if not self.rLib[col].isActive():
                return fl^32
        return fl
    
    
    # set column with index col as val 
    # where val = True or False
    def setActive(self, col, val):
        self.rLib[col].setActive(val)
    
    
    # return Data
    def data(self, modind, role = QtCore.Qt.DisplayRole ):
        col = modind.column()
        var = super().data(modind, role)
        if self.debug:
            if role == QtCore.Qt.DisplayRole:
                print("Data: col=",col," var=",var," role=Display")
            elif role == QtCore.Qt.EditRole:
                print("Data: col=",col," var=",var," role=Edit")
        
        if (not col in self.rLib):
            return var
        
        if role == QtCore.Qt.EditRole:
            if self.translate:
                trValue = self.rLib[col].getBatAval(var)
                if self.debug: print("   translated var=",trValue)  
                return trValue
            else :
                return var
        elif role == QtCore.Qt.DisplayRole:
            trValue = self.rLib[col].getBatAval(var)
            if self.debug: print("   translated var=",trValue)
            return trValue
        elif role == QtCore.Qt.ForegroundRole:
            if self.rLib[col].isActive():
                blueText = QtGui.QBrush(QtCore.Qt.darkBlue)
                return blueText
        else : return var
        
    
    
    # return Data, with translate option and only Display role
    # row and col are int values
    def data2(self, row, col, translate=True):
        modind = self.index(row,col)
        value  = super().data(modind, QtCore.Qt.DisplayRole)
        if self.debug:
                print("Data2: col=",col," var=",var," role=Display")
        
        if (not col in self.rLib) or (not translate): return value
        
        trValue = self.rLib[col].getBatAval(value)
        if self.debug: print("   translated var=",trValue)
        
        return trValue
    
    
    # return Data, with translate option and only Display role
    # row is an int and col is a string
    def data3(self, row, colStr, translate=True):
        col = self.fieldIndex(colStr)
        assert col >= 0, print("Error in HSqlTableModel.data2")
            
        modind = self.index(row,col)
        value  = super().data(modind, QtCore.Qt.DisplayRole)
        if self.debug:
                print("Data3: col=",col," var=",var," role=Display")
        
        if (not col in self.rLib) or (not translate): return value
        
        trValue = self.rLib[col].getBatAval(value)
        if self.debug: print("   translated var=",trValue)
        
        return trValue
    
    
    
    
    
    #setData ( const QModelIndex & index, const QVariant & value, int role = Qt::EditRole )
    def setData(self, modind, value, role = QtCore.Qt.EditRole):
        col = modind.column()
        if self.debug:
            if role == QtCore.Qt.EditRole:
                print("#### setData: col=",col," var=",value," role=Edit")
        
        if (not role == QtCore.Qt.EditRole) or (not col in self.rLib):
            return self._setData(modind, value, role)
        
        if isinstance(value,int):
            return self._setData(modind, value, role)
            
        trValue = self.rLib[col].getAatBval(value)
        if self.debug: print("     transformed Value: ", trValue)
            
        if trValue == None:
            return False
        else:
            return self._setData(modind, trValue, role)
    
    
    #setData ( const QModelIndex & index, const QVariant & value, int role = Qt::EditRole )
    # here row and col are int values
    def setData2(self, row, col, value, translate=True):
        modind = self.index(row,col)
        if self.debug:
            if role == QtCore.Qt.EditRole:
                print("#### setData2: col=",col," var=",value," role=Edit")
        
        if (not col in self.rLib) or (not translate):
            return self._setData(modind, value, QtCore.Qt.EditRole)
        
        trValue = self.rLib[col].getAatBval(value)
        if self.debug: print("     transformed Value: ", trValue)
        assert trValue >= 0, print("Error in HSqlTableModel.setData2")
        
        if translate:
            return self._setData(modind, trValue, role)
        else:
            return self._setData(modind, value, role)
            

    #setData ( const QModelIndex & index, const QVariant & value, int role = Qt::EditRole )
    # here row is an int and col is a string
    def setData3(self, row, colStr, value, translate=True):
        col = self.fieldIndex(colStr)
        assert col >= 0, print("Error in HSqlTableModel.data3")
        modind = self.index(row,col)
        if self.debug:
            print("#### setData3: col=",col," var=",value," role=Edit")
        
        if (not col in self.rLib) or (not translate):
            return self._setData(modind, value, QtCore.Qt.EditRole)
        
        trValue = self.rLib[col].getAatBval(value)
        if self.debug: print("     transformed Value: ", trValue)
        assert trValue >= 0, print("Error in HSqlTableModel.setData3")
        
        if translate:
            return self._setData(modind, trValue, QtCore.Qt.EditRole)
        else:
            return self._setData(modind, value, QtCore.Qt.EditRole)
    
    
    # set internally with no tranlation
    # because internally super().setData(modind, value, role) calls
    # self.data(modind, value, role = QtCore.Qt.EditRole)
    # it seems it sets a whole row at once with the value from
    # EditRole
    def _setData(self, modind, value, role = QtCore.Qt.EditRole):
        self.translate = False
        ans = super().setData(modind, value, role)
        if ans == True:  self.dirtyData = True
        self.translate = True
        return ans
    
    
    
    #QSqlTableModel::headerData ( int section, Qt::Orientation orientation, int role = Qt::DisplayRole ) 
    def headerData(self, col, orient, role ):
        var = super().headerData(col, orient, role)
        if role != QtCore.Qt.DisplayRole or orient == 2: return var
    
        if  col in self.rLib:
            if self.rLib[col].headerChanged:
                return self.rLib[col].colB
            
        return var
    
    
    # own version of insertRecord, to mark Table as changed
    def insertRecord (self, row, record):
        ret = super().insertRecord(row, record)
        if ret:
            self.dirtyData = True
        return ret
    
    # own version for setRecord, to mark Table as changed
    # and to switch off data translation
    def setRecord(self,row, record):
        self.translate = False
        ret = super().setRecord(row, record)
        self.translate = True
        if ret:
            self.dirtyData = True
        return ret
    
    
    # own version for removeRecord, to mark Table as changed
    # and to switch off data translation
    def removeRows(self, row, count):
        self.translate = False
        ret = super().removeRows(row, count)
        self.translate = True
        if ret:
            self.dirtyData = True
        return ret
        
    
    
    
    #own version of submit to spot errors
    def submit(self):
        ans = super().submit()
        #print( self.lastError.text())
        if not ans:
            print("Error: ", self.lastError() )
        return ans
        
        
    #own version of submit to spot errors
    def submitAll(self):
        ans = super().submitAll()
        #print( self.query().executedQuery())
        if not ans:
            print("Error: ", self.lastError() )
        else :
            self.dirtyData = False
        return ans
        
        
    def hasUnsavedData(self):
        return self.dirtyData
        

