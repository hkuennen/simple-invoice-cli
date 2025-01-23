import datetime
import io
import locale
import os

from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


class Invoice:
    def __init__(self):
        locale.setlocale(locale.LC_TIME, "de_DE.UTF-8")

        pdfmetrics.registerFont(TTFont("CMU Bright", "cmunbmr.ttf"))
        pdfmetrics.registerFont(TTFont("CMU Bright SemiBold", "cmunbsr.ttf"))

        self.date_today = datetime.date.today()
        self.this_month = self.date_today.strftime("%B")
        self.this_year = self.date_today.strftime("%Y")
        self.invoice_number = input("Welche Rechnungs-Nr. hat die Rechnung?: ")

    def create(self):
        factor = 2.835
        date = self.date_today.strftime("%d. %b. %Y")
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        # Max x position: 210, max y position: 297
        can.setFont("CMU Bright SemiBold", 11)
        can.drawString(
            (21.5 * factor),
            (171 * factor),
            f"{'Rechnungs-Nr.: '}{self.invoice_number}",
        )
        can.setFont("CMU Bright", 11)
        can.drawString((161.5 * factor), (181 * factor), date)
        can.drawString(
            (39 * factor),
            (153.5 * factor),
            f"{'Für die Lagerkapazität für '}{self.this_month}{' '}{self.this_year}",
        )
        can.drawString((39 * factor), (148.6 * factor), "berechnen wir")
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)

        # Create a new PDF
        new_pdf = PdfReader(packet)
        # Read in the template
        template_name = os.getenv("TEMPLATE_NAME")
        template = PdfReader(open(f"_input/{template_name}.pdf", "rb"))
        output = PdfWriter()
        # Put the newly created PDF on top of the existing template
        page = template.pages[0]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)
        # Finally, write the blob to a real pdf file
        output_stream = open(
            f"{'_output/Rechnungs-Nr. '}{self.invoice_number}{'.pdf'}", "wb"
        )
        output.write(output_stream)
        output_stream.close()
