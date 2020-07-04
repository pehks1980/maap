import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from cred_maap import *

def send_my_mail(sender_email, receiver_email, user):
    # Send email here
    message = MIMEMultipart("alternative")
    message["Subject"] = "MAAP e-mail notify test"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    user_name = user.get('first_name')
    user_id = user.get('id')
    host_url = HOST_URL
    text = """\
    Hi, THIS IS MAAP TEST e-mail notification!
    How are you? Костя Костя """
    html = f"""\
    <html>
      <body>
        <p>Hi,{user_name}<br> THIS IS MAAP TEST e-mail notification! <br>
           Костя Костя<br>
           <a href="{host_url}">MAAP LESSON</a> 
           <br>
           <a href="{host_url}/uncheck/{receiver_email}/{user_id}/">stop receiving notifications for MAAP LESSON</a> 
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    port = 465  # For SSL
    #password = input("Type your password and press enter: ")

    mygmail_acct = GMAIL_ACCT
    mygmail_password = GMAIL_PASSWD
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(mygmail_acct, mygmail_password)
        server.sendmail(sender_email,receiver_email,message.as_string())

def mail_notify(email_addr, user ):
    print (f'sending mail to {user}, addr {email_addr}')
    sender_email = SENDER_MAIL
    send_my_mail(sender_email,email_addr,user)
