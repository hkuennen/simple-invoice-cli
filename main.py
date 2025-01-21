from operator import attrgetter

# import emailing
from lib.invoice import Invoice

if __name__ == "__main__":
    invoice = Invoice()
    invoice.create()
    invoice_number, this_month, this_year = attrgetter(
        "invoice_number", "this_month", "this_year"
    )(invoice)
    # emailing.email_func(invoice_number, this_month, this_year)
