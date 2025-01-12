import datetime
import io
import locale

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

import emailing

locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

pdfmetrics.registerFont(TTFont("CMU Bright", "cmunbmr.ttf"))
pdfmetrics.registerFont(TTFont("CMU Bright SemiBold", "cmunbsr.ttf"))

factor = 2.835
date_today = datetime.date.today()
# dateNextMonth = dateToday + datetime.timedelta(days=30)
this_month = date_today.strftime("%B")
this_year = date_today.strftime("%Y")
invoice_number = input("Welche Rechnungs-Nr. hat die Rechnung?: ")
date = date_today.strftime("%d. %b. %Y")


def pdf_func():
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    # Max x position: 210, max y position: 297
    can.setFont("CMU Bright SemiBold", 11)
    can.drawString(
        (21.5 * factor), (171 * factor), f"{'Rechnungs-Nr.: '}{invoice_number}"
    )
    can.setFont("CMU Bright", 11)
    can.drawString((161.5 * factor), (181 * factor), date)
    can.drawString(
        (39 * factor),
        (153.5 * factor),
        f"{'Für die Lagerkapazität für '}{this_month}{' '}{this_year}",
    )
    can.drawString((39 * factor), (148.6 * factor), "berechnen wir")
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)

    # Create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # Read your existing PDF
    existing_pdf = PdfFileReader(open("Rechnung_WTF.pdf", "rb"))
    output = PdfFileWriter()
    # Lay the newly created PDF on top of the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # Finally, write "output" to a real file
    output_stream = open(f"{'Rechnungs-Nr. '}{invoice_number}{'.pdf'}", "wb")
    output.write(output_stream)
    output_stream.close()


if __name__ == "__main__":
    pdf_func()
    emailing.email_func(invoice_number, this_month, this_year)
