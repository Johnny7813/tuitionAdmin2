from reportlab.platypus import Table, TableStyle, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import pink, black, red, blue, green
from PyQt5.QtCore import QDate


class ReceiptDocument:
    """This class represents a pdf receipt.
    All units are in mm
    pdffilePath is the output pdf file
    receiptData  = [ Options, lesson_dates,tuition_id_prefix, lesson_num, number_of_lessons,
        student_name, tuition_address, post code, duration_of_lesson, tuition_fee ]
    """

    def __init__(self, pdffilePath, receiptData):
        self.pageHeight = A4[1]/mm  # in mm, all units in mm
        self.pageWidth = A4[0]/mm
        self.lMargin = 20.0
        self.rMargin = 20.0
        self.tMargin = 30.0
        self.bMargin = 30.0
        #print("page size of A4 in mm: ", self.pageWidth, self.pageHeight)

        self.canvas = Canvas(pdffilePath, pagesize=A4)
        self.canvas.setTitle("receipt for maths tuition")
        self.title = "receipt for maths tuition"
        self.textSize = 16  # in pixels
        self.headingSize = 22  # in pixels
        self.iSpace = 20  # in pixels
        self.rightColumn = self.pageWidth / 2.0

        self.fontPathBase = "./fonts/%s.ttf"
        #print("Font: ", self.fontPathBase % "DejaVuSerif")
        pdfmetrics.registerFont(TTFont('DejaVu', self.fontPathBase % "DejaVuSerif"))
        pdfmetrics.registerFont(TTFont('DejaVu-Bold', self.fontPathBase % "DejaVuSerif-Bold"))
        pdfmetrics.registerFont(TTFont('DejaVu-Italics', self.fontPathBase % "DejaVuSerif-Italic"))

        self.tutor = "Hannes Buchholzer"
        self.options = receiptData[0]
        self.tuition_dates = receiptData[1]
        self.tuition_id_prefix = receiptData[2]
        self.lesson_num = receiptData[3]
        self.n_lessons = receiptData[4]
        self.student_name = receiptData[5]
        # format address data, put postcode to address
        pre_address = receiptData[6]
        if pre_address.endswith("?"):
            pre_address = pre_address[:-1] + ","
            self.tuition_address = [pre_address, receiptData[7]]
        else:
            address = pre_address + ", " + receiptData[7]
            self.tuition_address = address.split("?")
        self.lesson_duration = receiptData[8]
        self.tuition_fee = receiptData[9]
        self.year = QDate.currentDate().toString("yyyy")

    # make a tuition_id out of a prefix (string)
    # and a number
    def make_tuition_id(self, num):
        tuition_id = self.tuition_id_prefix + "{0:03d}".format(int(num)+self.lesson_num)
        return tuition_id

    # make a date string
    def make_date(self, ind):
        if ind < len(self.tuition_dates):
            return self.tuition_dates[ind].toString("dd/MM/yyyy")
        else:
            word1 = "___ / ___ / "
            word2 = self.year if self.options["year"] else "______"
            return word1+word2

    # return lesson duration dependent on option
    def make_duration(self):
        if self.options["minutes"]:
            word = "{0} minutes".format(int(self.lesson_duration))
        else:
            word = "_____  minutes"
        return word

    # return the payemnt amount, which is the tuition fee
    def make_payment(self):
        if self.options["payment"]:
            word = "£ {:4.2f}".format(float(self.tuition_fee))
        else:
            word = "£ _____"
        return word

    # translate coordinates x,y in mm from top left
    # into pixels from bottom right
    def coord(self, x, y, fromRight=False, fromBottom=False):
        cx = (self.pageWidth - x) * mm if fromRight else x * mm
        cy = y * mm if fromBottom else (self.pageHeight - y) * mm
        return (cx, cy)

    # draw it centered y mm from top
    def draw_heading(self, y):
        self.canvas.setFont('DejaVu', self.headingSize)
        (cx, cy) = self.coord(self.pageWidth / 2.0, y)
        self.canvas.drawCentredString(cx, cy, self.title)


    # draw it centered y mm from top
    def draw_section(self, y, ind):
        self.canvas.setFont('DejaVu', self.textSize)
        # left column
        (xl, yy) = self.coord(self.lMargin, y)
        (xr, yy) = self.coord(self.rightColumn, y)

        self.canvas.drawString(xl, yy, "unique tuition id:")
        self.canvas.drawString(xr, yy, self.make_tuition_id(ind))
        yy -= self.iSpace
        self.canvas.drawString(xl, yy, "name of tutor:")
        self.canvas.drawString(xr, yy, self.tutor)
        yy -= self.iSpace
        self.canvas.drawString(xl, yy, "name of student:")
        self.canvas.drawString(xr, yy, self.student_name)
        yy -= self.iSpace
        self.canvas.drawString(xl, yy, "address of tuition:")
        for line in self.tuition_address:
            self.canvas.drawString(xr, yy, line)
            yy -= self.iSpace
        self.canvas.drawString(xl, yy, "date of tuition:")
        self.canvas.drawString(xr, yy, self.make_date(ind))
        yy -= self.iSpace
        self.canvas.drawString(xl, yy, "duration of a lesson:")
        self.canvas.drawString(xr, yy, self.make_duration())
        yy -= self.iSpace
        self.canvas.drawString(xl, yy, "tuition fee amount:")
        self.canvas.drawString(xr, yy, self.make_payment())
        yy -= self.iSpace
        if self.options["transfer"]:
            self.canvas.drawString(xl, yy, "payment:")
            self.canvas.drawString(xr, yy, "by bank transfer")
        else:
            self.canvas.drawString(xl, yy, "payment amount received:")
            self.canvas.drawString(xr, yy, "£ ______")
        yy -= self.iSpace
        self.canvas.drawString(xl, yy, "signature of client:")
        self.canvas.drawString(xr, yy, "__"*12)
        yy -= self.iSpace
        self.canvas.drawString(xl, yy, "signature of tutor:")
        self.canvas.drawString(xr, yy, "__"*12)


    def compileReceipt(self):
        for i in range(int(self.n_lessons/2)):
            self.draw_heading(30)
            self.draw_section(55, 2*i)
            self.draw_heading(173.5)
            self.draw_section(198.5, 2*i+1)
            self.canvas.showPage()
        self.canvas.save()


if __name__ == "__main__":
    # a simple test example
    Options = {"year": True, "minutes": False, "payment": True, "transfer": True}
    date1 = QDate(2018, 5, 6)
    date2 = QDate(2018, 5, 13)
    receiptData = [Options, [date1, date2], "ASuresh_", 34, 4,"Avinash Suresh",
                   "3 April Close, Horsham?","RH12 2LL", 90, 40]

    rec = ReceiptDocument("reportlab_receipt01.pdf", receiptData)
    rec.compileReceipt()

