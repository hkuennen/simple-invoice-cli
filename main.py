from operator import attrgetter

from lib.email import Email
from lib.invoice import Invoice

if __name__ == "__main__":
    invoice = Invoice()
    invoice.create()
    invoice_number, this_month, this_year = attrgetter(
        "invoice_number", "this_month", "this_year"
    )(invoice)
    email = Email(invoice_number, this_month, this_year)
    email.add_attachment()
    email.send()
