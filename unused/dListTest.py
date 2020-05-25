

from PyQt5 import QtCore, QtGui, QtSql


# a list with pairs made from two columns
# from a table from a database
class SqlList:
    # 
    def __init__(self, db, table, colA, colB, active=False):
        self.init2(db,table,colA,colB)
        self.active = active
    
    # init helper tables with colA = entry and colB = word
    def __init__(self, db, table, active=False):
        self.init2(db,table,"entry","word")
        self.active = active
    
    
    def init2(self,db,table,colA,colB):
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
    
    def isActive(self):
        return self.active

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
    
    def print(self):
        print(self.listA)
        print(self.listB)


db = QtSql.QSqlDatabase.addDatabase("QMYSQL")
db.setHostName("localhost");
db.setDatabaseName("private_tuition_v3") # operates on a copy for my real database
db.setConnectOptions("UNIX_SOCKET=/home/hannes/Database/DB/hannes_db.socket")
db.open()

li = dList(db,"help_travel")

li.print()

print(li.getBatAval(3))
print(li.getBatInd(3))


        
