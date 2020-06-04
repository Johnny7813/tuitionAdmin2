from reportlab.platypus import Table, TableStyle, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import pink, black, red, blue, green


class InvoiceDocument:
    """This class represents a pdf invoice.
    All units are in mm
    pdffilePath is the output pdf file
    invoiceData = [invoiceHeader, lesson1List, ..., lessonNList]
    invoiceHeader = [invoice_date, invoice_to, invoice_for, invoice_ref, n, amount]
    lesson1List = [date, tuition_ref, hours, rate, amount, reason1, money1, ...,
                    reasonN, moneyN, "discount", money]
    """

    def __init__(self, pdffilePath, invoiceData):
        self.pageHeight = A4[1]/mm  # in mm, all units in mm
        self.pageWidth = A4[0]/mm
        self.lMargin = 20.0
        self.rMargin = 20.0
        self.tMargin = 30.0
        self.bMargin = 30.0
        #print("page size of A4 in mm: ", self.pageWidth, self.pageHeight)

        self.canvas = Canvas(pdffilePath, pagesize=A4)
        self.canvas.setTitle("Invoice for Maths tuition")
        self.title = "Invoice for Maths tuition"

        self.fontPathBase = "./fonts/%s.ttf"
        #print("Font: ", self.fontPathBase % "DejaVuSerif")
        pdfmetrics.registerFont(TTFont('DejaVu', self.fontPathBase % "DejaVuSerif"))
        pdfmetrics.registerFont(TTFont('DejaVu-Bold', self.fontPathBase % "DejaVuSerif-Bold"))
        pdfmetrics.registerFont(TTFont('DejaVu-Italics', self.fontPathBase % "DejaVuSerif-Italic"))

        self.tutorData = ["Hannes Buchholzer", "3 April Close, Horsham, RH12 2LL",
                          "07516-100218", "buchholzer.hannes@gmail.com"]
        self.invoiceHeader = invoiceData.pop(0)
        self.invoiceData   = invoiceData

        self.compileInvoice()

    # translate coordinates x,y in mm from top left
    # into pixels from bottom right
    def coord(self, x, y, fromRight=False, fromBottom=False):
        cx = (self.pageWidth - x)*mm if fromRight else x*mm
        cy = y * mm if fromBottom else (self.pageHeight - y) * mm
        return (cx, cy)

    # translate a mm value into pixels. Works also for a list of mm values
    def trans(self, x):
        if isinstance(x,list):
            cx = list(range(len(x)))
            for i in range(len(x)):
                cx[i] = float(x[i]) * mm
        else:
            cx = float(x)*mm

        return cx

    # convert Money to String
    # x should be a money amount as integer and float
    # the output is a string with £ sign
    def cM2S(self, x):
        x = float(x)
        if x < 0.0:
            pre = "-"
            x   = -x
        else:
            pre = ""

        s = pre + "£{0:4.2f}".format(x)
        #print("convertMoney2String: ", x, " ", s)
        return s

    # convert date to String
    # x should be a list of 3 integers
    # day, month, year
    def cD2S(self, x):
        if x[2] < 100: x[2] += 2000
        s = "{0:>02n}/{1:>02n}/{2:4n}".format(*x)
        #print("convertDate2String: ", x, " ", s)
        return s

    # draw it centered y mm from top
    def draw_heading(self, y):
        # canvas.saveState()
        self.canvas.setFont('DejaVu', 20)
        (cx, cy) = self.coord(self.pageWidth / 2.0, y)
        self.canvas.drawCentredString(cx, cy, self.title)
        # canvas.restoreState()

    # draw the tutor's details; here x, y is the bottom left
    # corner of the first line in mm
    def draw_tutor(self, x, y):
        # canvas.saveState()
        cx, cy = self.coord(x,y)
        self.canvas.setFont('DejaVu-Bold', 13)
        self.canvas.drawString(cx, cy, self.tutorData[0])
        self.canvas.setFont('DejaVu', 10)
        cy -= 15
        self.canvas.drawString(cx, cy, "address:")
        self.canvas.drawString(cx + 19 * mm, cy, self.tutorData[1])
        cy -= 13
        self.canvas.drawString(cx, cy, "phone:")
        self.canvas.drawString(cx + 19 * mm, cy, self.tutorData[2])
        cy -= 13
        self.canvas.drawString(cx, cy, "email:")
        self.canvas.drawString(cx + 19 * mm, cy, self.tutorData[3])
        # canvas.restoreState()

    # draw the date; again x, y  are in mm
    # y is the distance from the top
    # x is the distance from the right
    def draw_invoice_date(self, x, y):
        # canvas.saveState()
        cx, cy = self.coord(x, y, fromRight=True)
        self.canvas.setFont('DejaVu-Bold', 10)
        self.canvas.drawRightString(cx, cy, "invoice date:")
        self.canvas.setFont('DejaVu', 10)
        cy -= 12 # go 12 pixels lower
        self.canvas.drawRightString(cx, cy, self.invoiceHeader[0])
        # canvas.restoreState()

    # draw the date; y  is in mm
    # y is the distance from the top
    def draw_invoice_data(self, y):
        middlex = 80
        # canvas.saveState()
        cx , cy = self.coord(self.lMargin, y)
        self.canvas.setFont('DejaVu-Bold', 11)
        self.canvas.drawString(cx, cy, "invoice to:")
        cx, cy = self.coord(middlex, y)
        self.canvas.drawString(cx, cy, "invoice for:")
        cx, cy = self.coord(self.pageWidth - 20, y)
        self.canvas.drawRightString(cx, cy, "invoice reference nr:")

        self.canvas.setFont('DejaVu', 10)
        cy -= 12 # go 12 pixels lower
        cx = self.lMargin * mm
        self.canvas.drawString(cx, cy, self.invoiceHeader[1])
        cx = middlex * mm
        self.canvas.drawString(cx, cy, self.invoiceHeader[2])
        cx = (self.pageWidth - 20) * mm
        self.canvas.drawRightString(cx, cy, self.invoiceHeader[3])
        # canvas.restoreState()

    # draw table
    # y is the distance in mm from top
    def draw_table(self, y):
        vspace = 4
        y += 8
        self.headStyle = TableStyle([
            ('FONT', (0, 0), (-1, 0), 'DejaVu-Bold', 10), ('GRID', (0, 0), (-1, 0), 2, black)])
        self.bodyStyle = TableStyle([('FONT', (0, 0), (-1, -1), 'DejaVu', 10),
                    ('BOX', (0, 0), (-1, -1), 2, black),('LINEBEFORE', (1, 0), (1, -1), 2, black),
                    ('LINEBEFORE', (2, 0), (2, -1), 2, black),('LINEBEFORE', (3, 0), (3, -1), 2, black),
                    ('LINEBEFORE', (4, 0), (4, -1), 2, black),('LINEBEFORE', (5, 0), (5, -1), 2, black),
                    ('ALIGN', (3, 0), (5, -1), 'RIGHT')])
        self.footStyle = TableStyle([
            ('FONT', (0, 0), (-1, 0), 'DejaVu-Bold', 10), ('BOX', (0, 0), (-1, -1), 2, black),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'), ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('LINEBEFORE', (1, 0), (1, -1), 2, black)])

        dataBody = []
        num = 0
        for lesson in self.invoiceData:
            #print("Line: ", lesson)
            num += 1
            line = lesson[0:2]
            line.append("teaching")
            line.append("{0:3.2f}".format(lesson[2]))
            line.append(self.cM2S(lesson[3]))
            line.append(self.cM2S(lesson[4]))
            dataBody.append(line)

            lRest = lesson[5:]
            while lRest:
                num += 1
                extra_reason = lRest.pop(0)
                extra_cost   = self.cM2S(lRest.pop(0))
                line2 = [None, None, extra_reason, None, None, extra_cost]
                dataBody.append(line2)

            self.bodyStyle.add('LINEABOVE', (0, num), (-1, num), 2, black)

        dataHead = [["date", "tuition reference", "description", "hours", "rate", "amount"]]
        dataFoot = [["total",self.cM2S(self.invoiceHeader[-1])]]

        colWiMMB  = [25, 48, 42, 16, 18, 20]
        colWiMMF  = [sum(colWiMMB[0:-1]),colWiMMB[-1]]
        colWidthB = self.trans(colWiMMB)
        colWidthF = self.trans(colWiMMF)
        #print(colWiMMB, colWiMMF)

        self.tableHead = Table(dataHead, colWidths=colWidthB, style=self.headStyle)
        self.tableBody = Table(dataBody, colWidths=colWidthB, style=self.bodyStyle, repeatRows=0)
        self.tableFoot = Table(dataFoot, colWidths=colWidthF, style=self.footStyle)

        sw, sh = self.tableHead.wrapOn(self.canvas, *self.trans([180, 10]))
        tw, th = self.tableBody.wrapOn(self.canvas, *self.trans([180, 120]))
        uw, uh = self.tableFoot.wrapOn(self.canvas, *self.trans([180, 10]))

        xx, yy = self.coord(self.lMargin, y)
        ay = yy - sh
        by = ay - th - vspace
        cy = by - uh - vspace
        theight = (sh + th + uh + 2*vspace) / mm
        self.tableHead.drawOn(self.canvas, xx, ay)
        self.tableBody.drawOn(self.canvas, xx, by)
        self.tableFoot.drawOn(self.canvas, xx, cy)

        return theight


    # draw the date; y  is in mm
    # y is the distance from the top
    def draw_invoice_foot(self, y):
        # canvas.saveState()
        cx, cy = self.coord(self.lMargin, y+6)
        self.canvas.setFont('DejaVu', 10)
        # theight is becoming the total height of
        # the footer
        theight = 10

        self.canvas.drawString(cx, cy,
            "Please pay by bank transfer to following account within 7 calendar days of invoice date:")
        cy -= 13
        theight += 13
        self.canvas.drawString(cx, cy,
            "Account Title: Hannes Buchholzer, Sort Code: 20-42-58, Account Number: 23821595.")
        cy -= 13
        theight += 13
        self.canvas.setFont('DejaVu-Italics', 10)
        self.canvas.drawString(cx, cy,
            "Please set the reference as the invoice reference number :")
        cy -= 20
        theight += 20
        self.canvas.setFont('DejaVu', 12)
        cx  = self.trans(self.pageWidth/2.0)
        self.canvas.drawCentredString(cx, cy, self.invoiceHeader[3])
        cy -= 20
        theight += 20
        self.canvas.setFont('DejaVu', 10)
        self.canvas.drawCentredString(cx, cy, "Thank you for choosing me as your Tutor!")
        theight = theight / mm   # convert into mm
        return theight


    def compileInvoice(self):
        self.draw_heading(30)
        self.draw_tutor(20, 50)
        self.draw_invoice_date(20, 50)
        self.draw_invoice_data(90)
        height1 = self.draw_table(110)

        yfoot = 120 + height1 + 20
        if yfoot <= 250.0:
            height2 = self.draw_invoice_foot(yfoot)
        else:
            self.canvas.showPage()
            height2 = self.draw_invoice_foot(35)
        self.canvas.save()

        #print("Height of the table: ", height1)
        #print("Height of the footer: ", height2)





if __name__ == "__main__":
    invoiceData = [['31/05/2020', 'Timothy Russell', 'Fraser Russell', 'invb-0819', 2, 180.0],
        ['03/07/2019', 'FRussell_037', 1.5, 32.0, 48.0, 'travel', 3.0, 'discount', -6.0],
        ['10/07/2019', 'FRussell_038', 1.5, 32.0, 48.0, 'travel', 3.0, 'discount', -6.0],
        ['17/07/2019', 'FRussell_039', 1.5, 32.0, 48.0, 'travel', 3.0, 'discount', -6.0],
        ['24/07/2019', 'FRussell_040', 1.5, 32.0, 48.0, 'travel', 3.0, 'discount', -6.0],
        #['31/07/2019', 'FRussell_041', 1.5, 32.0, 48.0, 'travel', 3.0, 'discount', -6.0],
        #['06/08/2019', 'FRussell_042', 1.5, 32.0, 48.0, 'travel', 3.0, 'discount', -6.0]
        ]

    inv = InvoiceDocument("reportlab_invoice02.pdf", invoiceData)
    #inv.compileInvoice()


