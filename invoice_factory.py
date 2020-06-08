# -*- coding: utf-8 -*-


from PyQt5 import QtCore, QtGui, QtWidgets
import os
import subprocess
from Hmodel   import *
import smtplib
import mimetypes
import os.path
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from reportlab_invoice import *
import enter_password_dialog


class invoice_factory(object):
    def __init__(self, model, parent=None):
        self.model          = model
        self.has_active_ir  = False #student has active invoice record
        self.parent_widget  = parent
        

            
    # public function: return the invoice id
    def get_invoice_id(self, student_idx):
        invoice_id    = self.model.stdcount.data3(student_idx,"active_invoice_id")
        if invoice_id == "":
            #prefix     = self.model.invcount.data3(0,"invoice_number_prefix")
            #counter    = self.model.invcount.data3(0,"invoice_counter")
            invoice_id = self._new_invoice_id()  #prefix + "{:04d}".format(counter)
        return invoice_id
            
            
    # private function, make a new invoice id, does not update any counters
    def _new_invoice_id(self):
        prefix     = self.model.invcount.data3(0, "invoice_number_prefix")
        counter    = self.model.invcount.data3(0, "invoice_counter")
        invoice_id = prefix + "{:04d}".format(counter)
        return invoice_id
    
    
    # increase invoice counter in student_counters
    def _inc_stdinv_counter(self):
        counter   = self.model.stdcount.data3(self.student_idx, "invoice_counter")
        counter  += 1
        self.model.stdcount.setData3(self.student_idx, "invoice_counter", counter)
        
        
    
    # increase global invoice counter in invoice_counter
    def _inc_invoice_counter(self):
        counter   = self.model.invcount.data3(0, "invoice_counter")
        counter  += 1
        self.model.invcount.setData3(0, "invoice_counter", counter)

    
    # private function that makes a new invoice record
    # based on the tuition record referenced by the index
    # tut_idx
    def _produce_invoice_record(self, tut_idx):
        tutMod              = self.model.tuition
        total_pay           = tutMod.data3(tut_idx,"total_cost")
        tuition_id          = tutMod.data3(tut_idx,"tuition_id")
        match               = re.match("(\w+_)0*([1-9][0-9]*)", tuition_id ) 
        (tutpref, tutcount) = (match.group(1), match.group(2)) 
        max_sessions        = self.model.student.data3(self.student_idx, "sessions_per_invoice")
        
        #produce new invoice record
        record = self.model.invoice.record(0)
        record.clearValues() # all values set to Null
        record.setValue("invoice_id" , self.invoice_id )
        record.setValue("last_name" , self.student_id )
        record.setValue("invoice_send_yn" , "no" ) # invoice_send_yn
        record.setValue("invoice_paid_yn" , "no" ) # invoice_paid_yn
        record.setValue("invoice_send_date" , QtCore.QDate(2000,1,1) )           # invoice_send_date
        record.setValue("invoice_paid_date" , QtCore.QDate(2000,1,1) )           # invoice_paid_date
        record.setValue("invoice_amount" , total_pay ) 
        record.setValue("reference_string" , " " ) # reference string
        record.setValue("tuition_id_prefix" , tutpref ) #tuition_id_prefix
        record.setValue("tuition_id_numbers" , tutcount ) #tuition_id counter == student_counter
        record.setValue("active_sessions" , 1 ) # total sessions for invoice 
        record.setValue("total_sessions" , max_sessions )  # max sessions 
        record.setValue("reminder_entry" , 0 ) #reminder entry number
        return record
    
    
    
    # update student counter
    def update_student_counter(self, student_id, coldes, value):
        sdcMod = self.model.stdcount
        sdcIdx = self.model.findStdcountKey(student_id)
        
        if sdcIdx >= 0 :
            sdcMod.setData3(sdcIdx,coldes,value)
            return True
        else :
            print("update_student_counter failed!\n\n")
            return False
    
    
    # write new invoice_id in the field active_invoice_id of student_counters 
    def _set_invoice_id(self, word):
        coldes = "active_invoice_id"
        self.update_student_counter(self.student_id, coldes, word)
        
    
    ## assemble all relevant data to produce an invoice
    def _make_invoice_data2(self, tuition_ids):
        model = self.model.tuition
        end   = len(tuition_ids)
        tind  = []

            
        for key in tuition_ids:
            print(key)
            tind.append(self.model.findTuitionKey(key))
        
        total    = 0
        tutmod   = self.model.tuition
        header   = [end , 0]
        tdata    = []
        tdata.append(header)
        
        
        for j in tind:
            body = []
            body.append(tutmod.data3(j,"tuition_date").toString("dd/MM/yyyy"))
            body.append(tutmod.data3(j,"tuition_id"))
            name    = tutmod.data3(j,"first_name")
            name   += " " + tutmod.data3(j,"last_name")
            name    =  re.sub("&", "and", name)
            body.append(name)
            cost    = tutmod.data3(j,"total_cost")
            total  += cost
            body.append(cost)
            span    = tutmod.data3(j,"duration")/60.0 
            body.append(span)
            fees_ph = tutmod.data3(j,"fees_ph")
            body.append(fees_ph)
            body.append(fees_ph*span)
            body.append(tutmod.data3(j,"extra_cost1_type"))
            body.append(tutmod.data3(j,"extra_cost1_amount"))
            body.append(tutmod.data3(j,"extra_cost2_type"))
            body.append(tutmod.data3(j,"extra_cost2_amount"))
            body.append(tutmod.data3(j,"extra_cost3_type"))
            body.append(tutmod.data3(j,"extra_cost3_amount"))
            body.append(tutmod.data3(j,"discount"))
            tdata.append(body)
        
        
        header[1]= total
        idata    = []
        idata.append(self.model.student.data3(self.student_idx,"invoice_to"))
        name     = self.model.student.data3(self.student_idx,"first_name")
        name    += " " + self.model.student.data3(self.student_idx,"last_name")
        idata.append(re.sub("&", "and", name))
        idata.append(self.invoice_id)
        idata.append(QtCore.QDate.currentDate().toString("dd/MM/yyyy"))
        
        #print("tdata: ", tdata)
        #print("idata: ", idata)
        
        return (idata, tdata)


    ## assemble all relevant data to produce an invoice
    def _make_invoice_data(self, tuition_ids):
        # number of lessons
        print("Make Invoice Data")
        nLessons = len(tuition_ids)
        tind = []

        for key in tuition_ids:
            print(key)
            tind.append(self.model.findTuitionKey(key))

        grand_total = 0.0
        tutmod = self.model.tuition

        name = self.model.student.data3(self.student_idx, "first_name") + " " + \
                    self.model.student.data3(self.student_idx, "last_name")
        name = re.sub("&", "and", name)

        invoiceData = []
        # invoiceHeader = [invoice_date, invoice_to, invoice_for, invoice_ref, number of lessons, total]
        invoiceHeader = []
        invoiceHeader.append(QtCore.QDate.currentDate().toString("dd/MM/yyyy"))
        invoiceHeader.append(self.model.student.data3(self.student_idx, "invoice_to"))
        invoiceHeader.append(name)
        invoiceHeader.append(self.invoice_id)
        invoiceHeader.append(nLessons)
        invoiceHeader.append(0.0)
        invoiceData.append(invoiceHeader)

        # lesson = [date, tuition_ref, hours, rate, amount, reason1, money1, ...,
        #       discount, discount_money]
        for j in tind:
            lesson_total = tutmod.data3(j, "total_cost")
            lesson_duration = tutmod.data3(j, "duration") / 60.0
            fees_ph = tutmod.data3(j, "fees_ph")
            lesson_amount = lesson_duration*fees_ph
            lesson_discount = tutmod.data3(j, "discount")
            extra_cost_amount = [tutmod.data3(j, "extra_cost1_amount"),
                        tutmod.data3(j, "extra_cost2_amount"), tutmod.data3(j, "extra_cost3_amount")]
            extra_cost_type = [tutmod.data3(j, "extra_cost1_type"), tutmod.data3(j, "extra_cost2_type"),
                               tutmod.data3(j, "extra_cost3_type")]
            #print(extra_cost_amount)
            #print(extra_cost_type)
            lesson = []
            lesson.append(tutmod.data3(j, "tuition_date").toString("dd/MM/yyyy"))
            lesson.append(tutmod.data3(j, "tuition_id"))
            lesson.append(lesson_duration)
            lesson.append(fees_ph)
            lesson.append(lesson_amount)
            for amount, type in zip(extra_cost_amount, extra_cost_type):
                if amount > 0.0:
                    lesson.append(type)
                    lesson.append(amount)
            if lesson_discount > 0.0:
                lesson.append("discount")
                lesson.append(-lesson_discount)

            invoiceData.append(lesson)
            grand_total += lesson_total

        invoiceData[0][-1] = grand_total

        return invoiceData

    
    # This function is called by the "Create Receipt" buttons
    # It uses the preset data in studentData and Fixme 
    ## arg 1: tuition_ids
    ## arg 2: output dir
    ## arg 3: optional start okular
    def create_invoice(self, tuition_ids, output_dir, start_okular=True):
        #print(tuition_ids)
        fname = output_dir + "/tuition-invoice-{0}.pdf".format(self.invoice_id)
        invoiceData = self._make_invoice_data(tuition_ids)
        #print("invoice_data:", invoiceData)
        invDoc = InvoiceDocument(fname, invoiceData)
        invDoc.compileInvoice()

        if start_okular:
            okular = subprocess.Popen(["/usr/bin/okular", fname])
        
        return fname


    # make a list with tuition ids from a invoice_record
    def _extract_tuition_ids(self, invoice_record):
        id_numbers      = invoice_record.value("tuition_id_numbers")
        tuition_numbers = re.split('#', id_numbers)
        tuition_ids     = []
        pref            = invoice_record.value("tuition_id_prefix")
        for i in range(0, len(tuition_numbers)):
            tuition_ids.append(pref+"{:03d}".format(int(tuition_numbers[i])))
        return tuition_ids
    
    
    # make a list with tuition ids from an invoice_id that 
    # defines an invoice record
    def _extract_tuition_ids2(self, invoice_index):
        invMod          = self.model.invoice
        id_numbers      = invMod.data3(invoice_index,"tuition_id_numbers")
        pref            = invMod.data3(invoice_index,"tuition_id_prefix")
        tuition_numbers = re.split('#', id_numbers)
        tuition_ids     = []
        for n in tuition_numbers:
            tuition_ids.append(pref+"{:03d}".format(int(n)))
        return tuition_ids
    

    # make a list with tuition ids from a string
    # returns just the numbers
    def _extract_tuition_nums(self, id_string):
        tuition_strings = re.split('#', id_string)
        tuition_numbers = []
        for sn in tuition_strings:
            tuition_numbers.append(int(sn))
        return tuition_numbers


    # return email password
    # here is the place to change
    # the account string displayed
    def get_email_password(self):
        # I only use the secrets.py file on my
        # local machine
        if os.path.isfile("secrets.py"):
            import secrets
            return secrets.email_password
        else:
            import enter_password_dialog

            passwordDialog = enter_password_dialog.PasswordDialog(
                                self.parent_widget, "buchholzer.hannes@gmail.com")

            ans = passwordDialog.exec()

            if ans == QtWidgets.QDialog.Accepted:
                return passwordDialog.password()
            else:
                return ""


    ########################################################
    ## this python function sends emails using my gmail account
    ## you can use either plain or html text in the body
    ## the attachemnt should be a pdf file. it works!
    # send email with attachment invoice_file
    # return true if invoice should be marked as sent
    # newest version
    def _send_email(self, student_id, invoice_file, question=True):
        #assert
        student_idx = self.model.findStudentKey( student_id )
        stdMod      = self.model.student
        
        emaildat    = []
        emaildat.append(stdMod.data3(student_idx,"invoice_to"))
        emaildat.append(re.sub("&","and",stdMod.data3(student_idx,"first_name")))
        emaildat.append(stdMod.data3(student_idx,"invoice_email"))
        
        msg = MIMEMultipart()
        
        ctype, encoding   = mimetypes.guess_type(invoice_file)
        maintype, subtype = ctype.split("/", 1)
        
        #print("Email Dat: ", emaildat)
        #print("ctype: ",ctype, "\nencoding: ", encoding)
        #print("maintype: ", maintype, "  /   subtype: ", subtype)
        
        email_text  = "Dear {0}\n\nAttached to this email is an ".format(emaildat[0])
        email_text += "invoice for the recent tutoring sessions for {0}.\n".format(emaildat[1])
        email_text += "On the invoice you will find all necessary payment instructions.\n"
        email_text += "Thank you for having me as tutor.\n\nKind Regards,\nDr Hannes Buchholzer"
        
        text        = "Email:\n\n" + email_text + "\n\nDo you want to send"
        text       += " this email with invoice as attachement to {0}?".format(emaildat[2])
        
        if question:
            ans = QtWidgets.QMessageBox.question( self.parent_widget, "send invoice?", text , 
                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        
        # no question, assume we should send
        if (not question) or ans == QtWidgets.QMessageBox.Yes :
            # email subject
            msg['Subject'] = "invoice for maths tuition"
            msg['From']    = "Hannes.Buchholzer@zohomail.eu"
            msg['To']      = emaildat[2]
            msg.attach(MIMEText(email_text, "plain"))
            
            fp         = open(invoice_file, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=invoice_file)
            msg.attach(attachment)
            
            # Send the message via our email account
            ans = True
            email_password = self.get_email_password()
            s = smtplib.SMTP_SSL('smtp.zoho.eu', 465)
            try:
                s.login("Hannes.Buchholzer@zohomail.eu", email_password)
                s.send_message(msg)
                s.quit()
            except:
                ans = False
                print("Failed to send Email.")
                QtWidgets.QMessageBox.information(self.parent_widget, "Sending Email failed",
                                "There was an error sending the email!\nMaybe password is wrong?")
            return ans
        
        else :
            return False

    
    ########################################################
    ## this python function sends emails using my gmail account
    ## you can use either plain or html text in the body
    ## the attachemnt should be a pdf file. it works!
    # send email with attachment invoice_file
    # return true if invoice should be marked as sent
    # newest version
    def _send_reminder_email(self, student_id, invoice_file, reminder, question=False):
        #assert
        student_idx = self.model.findStudentKey( student_id )
        stdMod      = self.model.student
        
        emaildat    = []
        emaildat.append(stdMod.data3(student_idx,"invoice_to"))
        emaildat.append(re.sub("&","and",stdMod.data3(student_idx,"first_name")))
        emaildat.append(stdMod.data3(student_idx,"invoice_email"))
        
        msg = MIMEMultipart()
        
        ctype, encoding   = mimetypes.guess_type(invoice_file)
        maintype, subtype = ctype.split("/", 1)
        
        email_text  = "Dear {0}\n\nThis is a reminder for the invoice you received recently ".format(emaildat[0])
        email_text += "for tutoring sessions for {0}. This invoice is attached to this email. ".format(emaildat[1])
        email_text += "On the invoice you will find all necessary payment instructions.\n"
        email_text += "Thank you for having me as tutor.\n\nKind Regards,\nDr Hannes Buchholzer"
        
        text        = "Email:\n\n" + email_text + "\n\nDo you want to send"
        text       += " this email with invoice as attachement to {0}?".format(emaildat[2])
        
        if question:
            ans = QtWidgets.QMessageBox.question( self.parent_widget, "send invoice?", text , 
                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)


        # no question, assume we should send
        if (not question) or ans == QtWidgets.QMessageBox.Yes :
            # email subject
            msg['Subject'] = "invoice for maths tuition"
            msg['From']    = "Hannes.Buchholzer@zohomail.eu"
            msg['To']      = emaildat[2]
            msg.attach(MIMEText(email_text,"plain"))
            
            fp         = open(invoice_file, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=invoice_file)
            msg.attach(attachment)
            
            # Send the message via our email account
            ans = True
            email_password = self.get_email_password()
            s = smtplib.SMTP_SSL('smtp.zoho.eu', 465)
            try:
                s.login("Hannes.Buchholzer@zohomail.eu", email_password)
                s.send_message(msg)
                s.quit()
            except:
                ans = False
                print("Failed to send Email.")
                QtWidgets.QMessageBox.information(self.parent_widget, "Sending Email failed",
                                "There was an error sending the email!\nMaybe password is wrong?")

            return ans
        
        else :
            return False
    

    ## send invoice for a row invoice_index
    def send_invoice(self, invoice_index):
        invMod              = self.model.invoice
        self.student_id     = invMod.data3(invoice_index,"last_name", False)
        self.student_idx    = self.student_id-1
        self.invoice_id     = invMod.data3(invoice_index,"invoice_id")
    
        total_seesions      = invMod.data3(invoice_index,"total_sessions")
        active_seesions     = invMod.data3(invoice_index,"active_sessions")
        
        if active_seesions < total_seesions :
            ans = QtWidgets.QMessageBox.question( self.parent_widget, "Record not complete", 
                                              "Invoice record not complete!\nDo you still want to send the invoice?",
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
            if ans == QtWidgets.QMessageBox.No:
                return
    
        tuition_ids         = self._extract_tuition_ids2(invoice_index)
        
        #create invoice
        invoice_file = self.create_invoice(tuition_ids, settings.invoice_dir )
        
            
        if self._send_email(self.student_id, invoice_file):
            invMod.setData3(invoice_index,"invoice_send_yn", "yes")
        else :
            invMod.setData3(invoice_index,"invoice_send_yn", "no")
            
            
        ans = QtWidgets.QMessageBox.question( self.parent_widget, "Change Student Counter", 
                                         "Do you want to mark the active_invoice_id as empty?", 
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
                 
        if ans == QtWidgets.QMessageBox.Yes:
            #update student counter
            self.update_student_counter(self.student_id, "active_invoice_id", "")
        
        #update invoice counter in student counters
        ans = QtWidgets.QMessageBox.question( self.parent_widget, "Change Student Counter", 
                                         "Do you want to increase invoice_counter in student_counters table?", 
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        if ans == QtWidgets.QMessageBox.Yes:
            #increase student_invoice counter
            self._inc_stdinv_counter()
    
        #update global invoice counter in invoice counters
        ans = QtWidgets.QMessageBox.question( self.parent_widget, "Change Student Counter", 
                                         "Do you want to increase invoice_counter in invoice_counters table?", 
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        if ans == QtWidgets.QMessageBox.Yes:
            #increase student_invoice counter
            self._inc_invoice_counter()
    
    
    ## send invoice for a row 
    def send_invoice_reminder(self, invoice_id, invoice_index, student_id, reminder):
        invMod              = self.model.invoice
        self.student_id     = invMod.data3(invoice_index,"last_name", False)
        self.student_idx    = self.student_id-1
        self.invoice_id     = invMod.data3(invoice_index,"invoice_id")
    
        total_seesions      = invMod.data3(invoice_index,"total_sessions")
        active_seesions     = invMod.data3(invoice_index,"active_sessions")
        
        tuition_ids         = self._extract_tuition_ids2(invoice_index)
        #print("tuition ids: ", tuition_ids)
        
        #create invoice
        invoice_file = self.create_invoice(tuition_ids, settings.invoice_dir )
        
        return self._send_reminder_email(self.student_id, invoice_file, reminder, True )


    ## check if the tuition record id is already in an invoice
    ## this is used in add_tuition_dialog to perform checks
    ## here we can't eliminate uses of QSqlRecord
    def check_invoice(self, student_idx, tuition_record):
        student_id          = student_idx+1
        cind                = self.model.findStdcountKey(student_id)
        invoice_id          = self.model.stdcount.data3(cind,"active_invoice_id")
        
        self.model.dump_record(tuition_record, "Tuition counter record ")
        # we need a new invoice record
        if invoice_id == "":
            return True
        
        # there is already an active invoice record for lesson
        else:
            # we need to update this invoice record
            # first we need to find this record
            iind           = self.model.findInvoiceKey(invoice_id)
            invmod         = self.model.invoice
            
            # we need to add the tuition number to tuition_id_numbers
            id_numbers     = str(invmod.data3(iind,"tuition_id_numbers"))
            print("tuition id numbers: ", id_numbers)
            tnum           = int(re.match("\w+_0*([1-9][0-9]*)", 
                                tuition_record.value("tuition_id")).group(1))
            print("tuition id new number: ", tnum)
            tuition_nums   = self._extract_tuition_nums(id_numbers)
            if( tnum in tuition_nums):
                ans = QtWidgets.QMessageBox.question(self.parent_widget, "Add tuition id anyway?", "This tuition number is already in a invoice record!\n"
                    "Do you still want to add in to the invoice record?", 
                    QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                
                if( ans == QtWidgets.QMessageBox.No ):
                    return False
            
            elif( not tnum == (max(tuition_nums)+1)):
                ans = QtWidgets.QMessageBox.question(self.parent_widget, "Add tuition id anyway?", "This tuition number is not the next bigger number!\n"
                    "Do you still want to add in to the invoice record?", 
                    QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                
                if( ans == QtWidgets.QMessageBox.No ):
                    return False
                
        return True

    
    ## main function, does it almost all
    ## this function is called when a new tuition record is added
    ## and payment type is bank transfer
    ## it produces a new invoice row or adds info to a present row
    ## This is the new version, that does not use records
    def process_invoice(self, student_idx, tut_idx):
        self.student_idx    = student_idx
        self.student_id     = student_idx+1
        
        stdcMod             = self.model.stdcount
        invMod              = self.model.invoice
        tutMod              = self.model.tuition
        
        stdc_idx            = self.model.findStdcountKey( self.student_id )
        self.invoice_id     = stdcMod.data3(stdc_idx,"active_invoice_id")
        self.tuition_index  = tut_idx
        
        # we need a new invoice record
        if self.invoice_id == "":
            self.invoice_id = self._new_invoice_id()
            new_record      = self._produce_invoice_record(tut_idx)
            ok              = invMod.insertRecord(-1, new_record)
            
            if not ok:
                QtWidgets.QMessageBox.warning("New Invoice record could not be inserted in table", QtWidgets.QMessageBox.Ok)
            else :
                self.model.statusBar.showMessage("Invoice record successfully inserted in table", 3000)
                #update student counter
                self._inc_invoice_counter()
                self._set_invoice_id(self.invoice_id)
                inv_idx  =  invMod.rowCount()-1
        
        # there is already a invoice record for this student
        else:
            # we need to update this invoice record
            # first we need to find the index of this invoice record
            inv_idx        = self.model.findInvoiceKey(self.invoice_id)
            #print("Key: ",self.invoice_id, "Index: ", iind)
            
            # we need to add the tuition number to tuition_id_numbers
            id_numbers     = str(invMod.data3(inv_idx, "tuition_id_numbers"))
            
            tnum           = int(re.match("\w+_0*([1-9][0-9]*)", 
                                tutMod.data3(tut_idx, "tuition_id")).group(1))
            
            id_numbers    += "#" + str(tnum)
            invMod.setData3(inv_idx, "tuition_id_numbers", id_numbers)
            
            # first we increase active_sessions_for_invoice
            count          = int(invMod.data3(inv_idx, "active_sessions"))
            count         += 1
            invMod.setData3(inv_idx, "active_sessions", count)
            
            
            # we need to increase the payment of the invoice by total_cost from the tuition record
            payment        = float(invMod.data3(inv_idx, "invoice_amount"))
            payment       += float(tutMod.data3(tut_idx, "total_cost"))
            invMod.setData3(inv_idx, "invoice_amount", payment)
            
            
            # we need to produce an invoice
            if (invMod.data3(inv_idx, "total_sessions") <= count):
                # get the tuition_ids from the invoice_records
                tuition_ids         = self._extract_tuition_ids2(inv_idx)
                
                #create invoice
                invoice_file = self.create_invoice(tuition_ids, settings.invoice_dir )
                
                #update student counter
                self.update_student_counter(self.student_id, "active_invoice_id", "")
                self._inc_stdinv_counter()
                
                # do you want to send invoice
                if self._send_email(self.student_id, invoice_file):
                    invMod.setData3(inv_idx, "invoice_send_yn", "yes")
                    invMod.setData3(inv_idx, "invoice_send_date", QtCore.QDate.currentDate())
                else :
                    invMod.setData3(inv_idx, "invoice_send_yn", "no")
            
        return 0
    


######################################################################################




    # This function can spot inconsistencies between
    # the invoice records and the tuition records
    def check_paid_invoice_carry_over(self):
        problem_strings = ["payment not registered", "payment date differs from invoice",
                           "invoice id wrong", "payment method wrong", "invoice total wrong"]
        print("\n\nChecking if paid invoices have been registered in tuition records")
        last = self.model.invoice.rowCount()
        paya = 0  # tuition payment in tuition record
        paym = 0  # payment method
        total_amount = 0
        dates = []
        faulty_invoices = []
        invMod = self.model.invoice
        tutMod = self.model.tuition

        # loop over all invoice indices
        for invidx in range(0, last):
            idate = invMod.data3(invidx, "invoice_paid_date")
            inv_id = invMod.data3(invidx, "invoice_id")
            # skip records that are not marked as paid
            if (invMod.data3(invidx, "invoice_paid_yn") == "no"):  continue
            tuition_ids = self._extract_tuition_ids2(invidx)

            problems = []
            tindices = []
            dates = []
            total_amount = 0  # total amount from the tuitions on the invoice
            for tutid in tuition_ids:
                tidx = self.model.findTuitionKey(tutid)
                tindices.append(tidx)
                tdate = tutMod.data3(tidx, "tuition_date")
                dates.append(tdate)
                paya = tutMod.data3(tidx, "total_cost")
                paym = tutMod.data3(tidx, "payment_method")
                preceived = tutMod.data3(tidx, "payment_received")
                pdate = tutMod.data3(tidx, "payment_date")
                tinv_id = tutMod.data3(tidx, "invoice_number")
                total_amount += paya

                # mark incosistencies
                if (preceived == "no"):
                    if not 0 in problems: problems.append(0)
                if (pdate != idate):
                    if not 1 in problems: problems.append(1)
                if (inv_id != tinv_id):
                    if not 2 in problems: problems.append(2)
                if (paym != "bank transfer"):
                    if not 3 in problems: problems.append(3)

            payi = invMod.data3(invidx, "invoice_amount")
            if total_amount != payi:
                problems.append(4)

            if problems:
                faulty_invoice = [invidx, inv_id, tindices, tuition_ids, dates, problems]
                faulty_invoices.append(faulty_invoice)

        num_easy_faults = 0
        details = ""
        for entry in faulty_invoices:
            #print("\ninvoice number: ", entry[1])
            #print("tuition indices: ", entry[3])
            #print("tuition dates: ", entry[4])
            #print("faults: ", entry[5])
            if max(entry[5]) < 3: num_easy_faults += 1
            details += "invoice id: {}\n".format(entry[1])
            details += "corresponding tuition ids: {}\n".format(entry[3])
            details += "problems: "
            for n in entry[5]:
                details += problem_strings[n]
                if n < 3: details += " -> fixable "
                else: details += " -> hard "
                if n != entry[5][-1]: details += ", "
            details += "\n\n"

        ####  inform user with QMessageBox
        num_faults = len(faulty_invoices)

        msgBox = QtWidgets.QMessageBox()
        if num_faults == 0:
            text = "We have found no inconsitencies."
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        else:
            text = "We have found {0} inconsitencies.".format(num_faults)
            if num_easy_faults == 0:
                text += " But none of them are fixable."
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            else:
                text += " Of these {0} are fixable. Do you want to fix these?".format(num_easy_faults)
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        msgBox.setDetailedText(details)
        msgBox.setText(text)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
        ret = msgBox.exec()

        if ret == QtWidgets.QMessageBox.Ok and num_easy_faults > 0:
            self.fix_invoice_carry_over_faults(faulty_invoices)


    # in this function we try to fix fixable faults that
    # have been identified in the function 'check_paid_invoice_carry_over'
    # the variable faulty_invoices was defined in that function
    def fix_invoice_carry_over_faults(self, faulty_invoices):
        invMod = self.model.invoice
        tutMod = self.model.tuition

        for entry in faulty_invoices:
            # entry[5] is a integer list of the problems of that invoice
            # 0: in some tuition records corresponding to the invoice
            #    are not marked as paid even though the invoice is
            if 0 in entry[5]:
                for tidx in entry[2]:
                    tutMod.setData3(tidx, "payment_received", "yes")

            # 1: in some tuition records corresponding to the invMod
            #    the payment date differs from the invoice payment date
            if 1 in entry[5]:
                iidx = entry[0]
                idate = invMod.data3(iidx,"invoice_paid_date")
                for tidx in entry[2]:
                    tutMod.setData3(tidx, "payment_date", idate)

            # 2: in some tuition records corresponding to the invoice
            #    have a invoice id that differs from invoice's id
            if 2 in entry[5]:
                inv_id = entry[1]
                for tidx in entry[2]:
                    tutMod.setData3(tidx, "invoice_number", inv_id)

