# Simple invoice script

## Philosophy
The idea for this app came to me while helping my dad with his company's billing process.\
I was manually creating recurring invoices in Excel, exporting them as PDFs, and sending them to customers on a monthly basis. Most of the steps were identical, with the only differences being the invoice number and the invoice date. I realized there had to be a better way to streamline this process by automating the PDF generation and email-sending tasks. So, I decided to put my software skills into practice and let the machine handle the work.


## Description

This script allows you to effortlessly create and email invoices as PDF files directly from your terminal.

### Prerequisites
- A PDF file containing your (corporate) invoice template.  
- Your email credentials, saved in a `.env` file in the root directory.

### How it Works
1. Run the `main.py` file in your terminal.  
2. The terminal will prompt you to enter an invoice number. This number will be added to a buffer together with the provided PDF invoice template.  

   _Note:_ The template is not included in the repository and must be added to the `_input` folder.  

3. The script automatically fetches the current date and adds it to the invoice buffer. Additionally, the billing period for the current month is printed on the invoice.  
4. A new invoice PDF is then generated from the buffer and saved in the `_output` folder.  

The positions of these strings (e.g., invoice number, date, billing period) can be adjusted to fit your invoice template’s layout.  

Finally, the program uses an automated function to send the generated invoice as an email attachment to a specified recipient. The recipient's email address, along with other credentials, must be stored in a `.env` file.  

### Customization Options
- You can modify the email body and the name of the attachment to suit your needs.  
