# -*- coding: utf-8 -*-
from PyQt5 import QtCore


## deployed version
class settings(object):
    dev_version     = True
    invoice_dir     = "/home/hannes/Documents/Private Tuition/Administration/invoices"
    receipt_dir     = "/home/hannes/Documents/Private Tuition/Administration/receipts"
    database        = "private_tuition_v3"
    sqlite_db       = "/home/hannes/Database/SQLite/private_tuition_d3.sqlite"
    receipts_left   = 0
    
    time_recording  = True
    time_span       = 2000  #in milliseconds  30 seconds
    time_rep        = 900   #450 # how many times to repeat
    time_treshold   = 30.0 #minutes to new entry
    start_time      = QtCore.QTime(9, 0)
    end_time        = QtCore.QTime(21, 0)
    
    
    # private_tuition_s$cycle-1.bak
    # private_tuition_s$span-1.bak
    backup_active   = False
    backup_cycle    = 9     # every day we do a new backup and after this number we start over
    backup_span     = 10    # every 10 days we do a new backup
    backup_dir      = "/home/hannes/Dropbox/DB_Backup"  # we write the backups in here
    backup_time     = 10     # make a call every 10 minutes

    #pdf viewer program to use to display pdf invoices and receipts
    #pdf_viewer      = "/usr/bin/pdfmod"
    pdf_viewer      = "/usr/bin/okular"
