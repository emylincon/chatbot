import smtplib
import config
import re

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def check(email):

    if re.search(regex, email):
        return 'valid'

    else:
        return 'invalid'


def send_email(subject, msg, _send_email):

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.ehlo()
        server.login(config.email_address, config.password)
        _message = 'Subject: {}\n\n{}\n\n SENT BY RIHANNA \n\n'.format(subject, msg)
        server.sendmail(config.email_address, _send_email, _message)
        server.quit()
        return f"Email sent to {_send_email}"
    except Exception as e:
        return f"Could not send email \n {e}"