# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import re
import os
import subprocess
from settings import *
from Hmodel   import *

import smtplib
import mimetypes
import sys
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from reportlab_invoice import *


email_password = ""

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
        prefix     = self.model.invcount.data3(0,"invoice_number_prefix")
        counter    = self.model.invcount.data3(0,"invoice_counter")
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

    
    
    ## produce a string with the Latex code for an invoice
    ## arg 1  : (invoiceData,tuitionData)
    ## return : string with tex code
    def _create_invoice_string(self,invdat):
        invoice_data = invdat[0]
        tuition_data = invdat[1]
        
        nr             = tuition_data[0][0]
        total_amount   = tuition_data[0][1]
        invoice_tex_id = re.sub("\_", "\\_", invoice_data[2] )
        pt             = 5  # precision variable for numberic values
        
        fixed  = [
              "\\documentclass[11pt,english,DIV 14]{scrlttr2}\n\\linespread{1}\n"
           +  "\\usepackage[T1]{fontenc}\n\\usepackage[utf8]{inputenc}\n"
           +  "\\usepackage{longtable}\\usepackage{babel}\n\\pagestyle{empty}\n"
           +  "\\setparsizes{0pt}{0pt}{0pt}\n\n\\begin{document}\n\n" ,
              "\\hspace{6pt}{\\Large\\bfseries Hannes Buchholzer} \\hfill {\\Huge\\bfseries Invoice}\\\\\n"
           +  "\\begin{tabular}{llrr}\n3 April Close & Phone: 07516 100 218 \\\\\nHorsham & Email: "
           +  "&  \\hspace{4cm} \\\\\nRH12 2LL & buchholzer.hannes@gmail.com\\\\\n\\end{tabular}\n\n\\vspace{2cm}\n\n" ,
              "\\begin{tabular}{p{5.1cm}p{5.1cm}r}\n & & {\\bfseries Invoice date:}\\\\\n & & " 
           +  "{{ {0} }}\\\\\n".format(invoice_data[3])
           +  "{\\bfseries Invoice to:} & {\\bfseries Invoice for:} & {\\bfseries \\hfill Invoice reference number:}\\\\\n"
           +  " {0} & {1}  & {2}\\\\\n".format(invoice_data[0], invoice_data[1], invoice_tex_id)
           +  "\\end{tabular}\n\n\\vspace{2cm}\n\n" ,
              "\\renewcommand{\\arraystretch}{1.5}\n\\begin{longtable}{|p{2cm}p{3.0cm}p{6.2cm}|p{0.9cm}p{0.7cm}r|}\n"
           +  "\\hline\n{\\bfseries date}&{\\bfseries reference nr}&{\\bfseries description}&{\\bfseries hours}&{\\bfseries rate}&{\\bfseries amount}\\endhead\n"
           +  "\\hline" ,
              "\\hline\n\\end{longtable}\n\n" ,
              "\\vfill\n{\\large Please pay by bank transfer to following account within 7 calendar days of invoice "
           +  "date:\\\\\nAccount Holder: Hannes Buchholzer, Sort Code: 20-42-58, Account Number: 23821595. "
           +  "\\emph{Please set the reference as\n the invoice reference number}}:\\newline"
           +  "\n\\begin{{center}}{{\\Large {0} }}\\end{{center}}\n".format(invoice_tex_id)
           +  "\\vspace{1cm}\n\n\\begin{center}\n\\Large Thank you for choosing me as your Tutor!\n\\end{center}\n\\end{document}\n" ]

        rstring  = fixed[0]
        rstring += fixed[1]
        rstring += fixed[2]
        rstring += fixed[3]
        
        ## calculate a page break if necessary
        bfak = 1.5 
        tutrec = tuition_data[1]
        if tutrec[7] == 1: bfak += 1
        if tutrec[9] == 1: bfak += 1
        if nr*bfak >= 13.9:    first = int(13.9/bfak)
        else :                 first = -1
        
        num = [0, 0, 0, 0, 0] # initialise list we need later
        
        for i in range(1, nr+1): 
            tutrec = tuition_data[i]
            #print("tutrec", tutrec)
            p      = 5
            
            #set precision for numbers correctly
            for j in (3,6,8,10):
                if tutrec[j] >= 100:
                    pt = p = 6
                    break
            # prepare data
            form_str  = "£{{:0{:d}.2f}}".format(p)
            #print("form_str", form_str)
            num[0]    = form_str.format(tutrec[3])
            num[1]    = form_str.format(tutrec[6])
            tutrec[1] = re.sub("\_", "\\_", tutrec[1])
            
            if i == first:  rstring += "\\hline\n\\newpage\n"
            
            rstring += "\\hline\n"
            rstring += "{0} & {1} & {{\\bfseries tuition for {2} subtotal}}".format(tutrec[0], tutrec[1], tutrec[2])
            rstring += " & & & {0} \\\\\n".format(num[0])
            rstring += " & & teaching  & {0} & £{1:0.2f} & {2} \\\\\n".format(tutrec[4], tutrec[5], num[1])
            if tutrec[8] > 0.001:
                num[2] = form_str.format(tutrec[8])
                rstring += " & & {0}  &  &  & {1} \\\\\n".format(tutrec[7], num[2])
            if tutrec[10] > 0.001:
                num[3] = form_str.format(tutrec[10])
                rstring += " & & {0}  &  &  & {1} \\\\\n".format(tutrec[9], num[3])
            if tutrec[12] > 0.001:
                num[4] = form_str.format(tutrec[12])
                rstring += " & & {0}  &  &  & {1} \\\\\n".format(tutrec[11], num[4])
            if tutrec[13] > 0.001:
                rstring += " & & discount  &  &  & £ {0:0.2f} \\\\\n".format((-1)*tutrec[13])
        
        form_str  = "£{{:0{:d}.2f}}".format(pt)
        num[0]    = form_str.format(total_amount)
        rstring  += "\\hline\n"
        rstring  += "\\hline\\hline  & & {{\\bfseries total}}  &  &  & {0} \\\\\n".format(num[0])
        
        rstring  += fixed[4]
        rstring  += fixed[5]
        
        #print("#########################\nrstring:\n", rstring)
        
        return rstring

    
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


    # This function is called by the "Create Receipt" buttons
    # It uses the preset data in studentData and Fixme
    ## arg 1: tuition_ids
    ## arg 2: output dir
    ## arg 3: optional start okular
    def create_invoice2(self, tuition_ids, output_dir, start_okular=True):
        # print(tuition_ids)
        invoice_data = self._make_invoice_data(tuition_ids)
        print("invoice_data:", invoice_data)
        invoice_tex = self._create_invoice_string(invoice_data)

        fname = output_dir + "/tuition-invoice-{0}.tex".format(invoice_data[0][2])
        fname2 = re.sub("tex", "pdf", fname)

        fhandle = open(fname, 'w')
        fhandle.write(invoice_tex)
        fhandle.close()

        os.chdir(output_dir)

        exitcode = subprocess.check_call("/usr/bin/pdflatex '{0}'".format(fname), shell=True,
                                         stdout=subprocess.DEVNULL)
        # print("create_invoice, pdflatex exitcode:", exitcode )

        assert exitcode == 0, "pdflatex failed!"
        if exitcode == 0 and start_okular:
            okular = subprocess.Popen(["/usr/bin/okular", fname2])
            # print("create_invoice, okular exitcode:", okular )

        return fname2



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
            msg['From']    = "buchholzer.hannes@gmail.com"
            msg['To']      = emaildat[2]
            msg.attach(MIMEText(email_text))
            
            fp         = open(invoice_file, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=invoice_file)
            msg.attach(attachment)
            
            # Send the message via our own SMTP server.
            ans = True 
            s   = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            try:
                r = s.login("buchholzer.hannes@gmail.com", email_password)
                r = s.send_message(msg)
                s.quit()
            except:
                ans = False
                print("login response : ", r)
                print("send_message response: ", r)
                
            
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
            msg['From']    = "buchholzer.hannes@gmail.com"
            msg['To']      = emaildat[2]
            msg.attach(MIMEText(email_text))
            
            fp         = open(invoice_file, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=invoice_file)
            msg.attach(attachment)
            
            # Send the message via our own SMTP server.
            ans = True 
            s   = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            try:
                r = s.login("buchholzer.hannes@gmail.com", "15R7f3m2h5t2f4")
                r = s.send_message(msg)
                s.quit()
            except:
                ans = False
                print("login response : ", r)
                print("send_message response: ", r)
                
            
            return ans
        
        else :
            return False
    
    
    
    
    
    ## send invoice for a row invoice_index
    def send_invoice(self, invoice_index):
        invMod              = self.model.invoice
        self.student_id     = invMod.data3(invoice_index,"last_name", False)
        self.student_idx    = self.student_id-1
        self.invoice_id     = invMod.data3(invoice_index,"invoice_id")
    
        #print("student_id", self.student_id, "invoice_id", self.invoice_id)
        #cind                = self.model.findStdcountKey( self.student_id )
    
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
    def check_invoice(self, student_idx, tuition_record):
        student_id          = student_idx+1
        cind                = self.model.findStdcountKey(student_id)
        invoice_id          = self.model.stdcount.data3(cind,"active_invoice_id")
        
        self.model.dump_record(tuition_record, "Tuition counter record ")
        # we need a new invoice record
        if invoice_id == "":
            return True
        
        # there is already a invoice record for this student
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
            # first we need to find this record
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
            
            
            # we need to increase the payment of the invoice by total_cost_ps from the tuition record
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
    
    
    
    
        
    # This function needs to be rewritten    
    # check if the payment amount in tuition records has been
    # correctly registered for paid invoice_send_date
    def check_paid_invoice_carry_over(self):
        print("\n\nChecking if paid invoices have been registered in tuition records")
        last = self.model.invoice.rowCount()-1
        paya = 0  # tuition payment asked
        payr = 0  # tuition payment received
        paym = 0  # difference in payment method
        total_amount  = 0
        pans = True
        easy = False
        hard = False
        ind  = []
        easy_ind         = []
        dates            = []
        easy_dates       = []
        hard_ind         = []
        easy_tuition_ids = []
        hard_tuition_ids = []
        
        
        for i in range(0, last+1):
            rec  = self.model.invoice.record(i)
            
            # skip records that are not marked as paid
            if rec.value("invoice_paid_yn") == "no" :  continue
            #self.model.dump_record(rec)
            tuition_ids = self._extract_tuition_ids(rec)
            #print(tuition_ids)
            
            easy     = False
            hard     = False
            end      = len(tuition_ids)
            ind.clear()
            dates.clear()
            total_amount   = 0  # total amount from the tuitions on the invoice
            for j in range(0,end):
                ti   = self.model.findTuitionKey(tuition_ids[j])
                trec = self.model.tuition.record(ti)
                ind.append(ti)
                idate= rec.value("invoice_paid_date")
                dates.append(idate)
                
                paya = trec.value("total_cost")
                payr = trec.value("payment_amount_received")
                paym = trec.value("payment_method")
                pans = trec.value("payment_received_yn")
                pdat = trec.value("payment_received_date")
                iref = rec.value("invoice_id")
                total_amount += paya   

                
                if (paya!=payr) or (paym!="bank transfer") or (pans=="no") or (pdat!=idate):
                    easy = True
                    print("\tPay difference: ", paya-payr,", payment method:", paym, ", payment received: ", pans)
                    
                    if (paym!="bank transfer")  or (iref != trec.value("invoice_number")):
                        hard = True
                    
            payi  = rec.value("invoice_amount")
            
            if not total_amount == payi:
                easy = True
                hard = True
                
            if easy:
                if not hard:
                    easy_ind.extend(ind)
                    easy_tuition_ids.extend(tuition_ids)
                    easy_dates.extend(dates)
                    
                else :
                    hard_ind.extend(ind)
                    hard_tuition_ids.extend(tuition_ids)
                    
        
        print("easy inconsistencies: \n", easy_tuition_ids)
        #print("easy inconsistencies: \n", easy_ind)
        #print("easy dates: \n", easy_dates)
        print("hard inconsistencies: \n", hard_tuition_ids, "\n\n")
        #print("hard inconsistencies: \n", hard_ind)
            
        
        ####  inform user with QMessageBox
        intot  = len(easy_ind) + len(hard_ind)
        ine    = len(easy_ind)
            
        details  = "Easy fixable inconsitencies:\n======================\n"
        details += "List of tuition_ids of these inconsistencies: "
        details += str(easy_tuition_ids) + "\n\n\n"
        details += "Hard non-fixable inconsitencies:\n===========================\n"
        details += "List of tuition_ids of these inconsistencies: "
        details += str(hard_tuition_ids) + "\n"
            
        msgBox = QtWidgets.QMessageBox()
        if ine == 0:
            if intot == 0:
                text = "We have found no inconsitencies."
            else:    
                text = "We have found {0} inconsitencies. But none of them are fixable".format(intot)
                msgBox.setDetailedText(details)
            msgBox.setText(text)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msgBox.exec()
        else:
            text = "We have found {0} inconsitencies. Of these {1} are fixable. Do you want to fix these?".format(intot, ine)
            msgBox.setText(text)
            msgBox.setDetailedText(details)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = msgBox.exec()
                
            if ret==QtWidgets.QMessageBox.Ok :
                    self.fix_paid_invoice_carry_over(easy_ind, easy_dates)
    
    




# check if the payment amount in tuition records has been
    # correctly registered for paid invoice_send_date
    def check_paid_invoice_carry_over2(self):
        print("\n\nChecking if paid invoices have been registered in tuition records")
        last             = self.model.invoice.rowCount()-1 #last invoice index
        paya             = 0  # tuition payment asked
        payr             = 0  # tuition payment received
        paym             = 0  # difference in payment method
        total_amount     = 0
        pans             = True
        easy             = False
        hard             = False
        ind              = []
        easy_ind         = []
        dates            = []
        easy_dates       = []
        hard_ind         = []
        easy_tuition_ids = []
        hard_tuition_ids = []
        invMod           = self.model.invoice
        tutMod           = self.model.tuition
        
        for i in range(0, last+1):
            
            # skip records that are not marked as paid
            if invMod.data3(i,"invoice_paid_yn") == "no" :  continue
            tuition_ids = self._extract_tuition_ids2(i)
            #print(tuition_ids)
            
            easy     = False
            hard     = False
            end      = len(tuition_ids)
            ind.clear()
            dates.clear()
            total_amount   = 0  # total amount from the tuitions on the invoice
            for tuition_id in tuition_ids:
                tidx   = self.model.findTuitionKey(tuition_id)
                trec   = self.model.tuition.record(tidx)
                ind.append(tidx)
                idate  = invMod.data3(i,"invoice_paid_date")
                dates.append(idate)
                
                
                paya = tutMod.data3(tidx, "total_cost")
                payr = tutMod.data3(tidx, "payment_amount_received")
                paym = tutMod.data3(tidx, "payment_method")
                pans = tutMod.data3(tidx, "payment_received_yn")
                pdat = tutMod.data3(tidx, "payment_received_date")
                iref = invMod.data3(i, "invoice_id")
                total_amount += paya   

                
                if (paya!=payr) or (paym!="bank transfer") or (pans=="no") or (pdat!=idate):
                    easy = True
                    print("\tPay difference: ", paya-payr,", payment method:", paym, ", payment received: ", pans)
                    
                    if (paym!="bank transfer")  or (iref != trec.value("invoice_number")):
                        hard = True
                    
            payi  = invMod.data3(i, "invoice_amount")
            
            if not total_amount == payi:
                easy = True
                hard = True
                
            if easy:
                if not hard:
                    easy_ind.extend(ind)
                    easy_tuition_ids.extend(tuition_ids)
                    easy_dates.extend(dates)
                    
                else :
                    hard_ind.extend(ind)
                    hard_tuition_ids.extend(tuition_ids)
                    
        
        print("easy inconsistencies: \n", easy_tuition_ids)
        #print("easy inconsistencies: \n", easy_ind)
        #print("easy dates: \n", easy_dates)
        print("hard inconsistencies: \n", hard_tuition_ids, "\n\n")
        #print("hard inconsistencies: \n", hard_ind)
            
        
        ####  inform user with QMessageBox
        intot  = len(easy_ind) + len(hard_ind)
        ine    = len(easy_ind)
            
        details  = "Easy fixable inconsitencies:\n======================\n"
        details += "List of tuition_ids of these inconsistencies: "
        details += str(easy_tuition_ids) + "\n\n\n"
        details += "Hard non-fixable inconsitencies:\n===========================\n"
        details += "List of tuition_ids of these inconsistencies: "
        details += str(hard_tuition_ids) + "\n"
            
        msgBox = QtWidgets.QMessageBox()
        if ine == 0:
            if intot == 0:
                text = "We have found no inconsitencies."
            else:    
                text = "We have found {0} inconsitencies. But none of them are fixable".format(intot)
                msgBox.setDetailedText(details)
            msgBox.setText(text)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msgBox.exec()
        else:
            text = "We have found {0} inconsitencies. Of these {1} are fixable. Do you want to fix these?".format(intot, ine)
            msgBox.setText(text)
            msgBox.setDetailedText(details)
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            ret = msgBox.exec()
                
            if ret==QtWidgets.QMessageBox.Ok :
                    self.fix_paid_invoice_carry_over(easy_ind, easy_dates)
    






    

    # fix easy inconsitencies
    def fix_paid_invoice_carry_over(self, indices, dates):
        print("fixing easy inconsitencies...")
        #indices = dat[0]
            
        end   = len(indices)
        for i in range(0,end):
            ind = indices[i]
            dat = dates[i]
            rec = self.model.tuition.record(ind)
            rec.setValue("payment_method","bank transfer")
            rec.setValue("payment_received_yn","yes")
            rec.setValue("payment_received_date",dat)
            v   = rec.value("total_cost_ps")
            rec.setValue("payment_amount_received",v)
            self.model.tuition.setRecord(ind,rec)
                
        print("Done.")
        
        
    

    
