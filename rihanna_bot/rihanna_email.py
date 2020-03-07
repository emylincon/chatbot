import smtplib
import config
import re

regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

contact = {'tim': 'lamt3@lsbu.ac.uk',
           'me': 'ugwuanye@lsbu.ac.uk',
           'emeka': 'emylincon@gmail.com',
           'rishi': 'ghoshs4@lsbu.ac.uk',
           'kasra': 'kasra.kassai@lsbu.ac.uk',
           'godwin': 'idojeg@lsbu.ac.uk',
           'brahim': 'elboudab@lsbu.ac.uk',
           'tasos': 'tdagiuklas@lsbu.ac.uk',
           'iqbal': 'm.iqbal@lsbu.ac.uk',
           'lucia': 'lucia.otoyo@lsbu.ac.uk',
           'maria': 'lemacm@lsbu.ac.uk',
           'jess': 'darleyjess@gmail.com',
           'ovo': 'ourumedji@yahoo.co.uk',
           }


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
        reply = f"Email sent to {_send_email}"
        return {'display': reply, 'say': reply}
    except Exception as e:
        reply = f"Could not send email \n {e}"
        return {'display': reply, 'say': reply}
