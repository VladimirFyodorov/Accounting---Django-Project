# https://docs.python.org/3/library/email.examples.html#email-examples
import smtplib, ssl
from email.message import EmailMessage
from math import floor

sender = 'acc.app.bot@gmail.com'
password = 'tfslvstxlyxvbssi'


def formatNumber(amount):
    amount_str = str(round(amount))
    n = floor(len(amount_str)/3)
    diff = len(amount_str) - n*3
    amount_formated = amount_str[0: diff]
    for i in range(n):
        amount_formated += ' '
        amount_formated += amount_str[diff + i*3: diff + (i + 1)*3]
    
    return(amount_formated)



def send_payment_email(receiver_email, receiver, payer, amount, test = False):

    msg = EmailMessage()

    if test:
        msg['Subject'] = "TEST Payment"
    else:
        msg['Subject'] = "Payment"

    content = """
    Hi, {receiver}!

    {payer} has made a payment of {amount} rub
    """.format(receiver = receiver, payer = payer, amount = formatNumber(amount))

    msg.set_content(content) 

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = ssl.create_default_context()) as server:
        server.login(sender, password)
        server.sendmail(sender, [receiver_email], msg.as_string())



def get_payment_email(receiver_email, receiver, payer, amount, test = False):

    msg = EmailMessage()

    if test:
        msg['Subject'] = "TEST Payment"
    else:
        msg['Subject'] = "Payment"

    content = """
    Hi, {payer}!

    You've made a payment of {amount} rub to {receiver}
    """.format(receiver = receiver, payer = payer, amount = formatNumber(amount))

    msg.set_content(content) 

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = ssl.create_default_context()) as server:
        server.login(sender, password)
        server.sendmail(sender, [receiver_email], msg.as_string())
