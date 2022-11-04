import base64
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# removed 4.11.22
# from maap_cred.cred_maap import *
from maap.local_settings import MAIL_ACCT, MAIL_PASSWD, MAIL_ACC_TOKEN, CLIENT_ID, SENDER_MAIL, HOST_URL


def generate_oauth2_string(username, access_token, as_base64=False):
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
    if as_base64:
        auth_string = base64.b64encode(auth_string.encode('ascii')).decode('ascii')
    return auth_string


def send_my_mail(sender_email, receiver_email, user):
    # Send email here
    message = MIMEMultipart("alternative")
    message["Subject"] = "MAAP Оповещение E-mail notify"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    user_name = user.get('first_name')
    user_id = user.get('id')
    host_url = HOST_URL
    rem_period = user.get('rem_period')
    text = """\
    Hi, THIS IS MAAP e-mail notification!
    How are you? We need to start again! Костя """

    # print(f"Shut the door{'s' if num_doors > 1 else ''}.")
    dct_choice = [
        {'val': 1, 'msg': 'каждый день'},
        {'val': 3, 'msg': 'раз в 3 дня'},
        {'val': 7, 'msg': 'раз в неделю'},
    ]
    rem_period_char = list(filter(lambda x: x['val'] == rem_period, dct_choice))

    html = f"""\
    <html>
      <body>
        <p>Hi,{str(user_name).capitalize()}<br> Пора начинать занятие! <br>
           
           <a href="{host_url}">MAAP LESSON</a> 
           <br>текущий режим оповещений - {rem_period_char[0]['msg']} <br>
            чтобы отключить рассылку нажмите на ссылку: <a href="{host_url}/uncheck/{receiver_email}/{user_id}/">Остановить</a> <br>
            c уважением MAAP Костя
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
    # password = input("Type your password and press enter: ")

    my_mail_acct = MAIL_ACCT
    my_mail_password = MAIL_PASSWD

    auth_string = generate_oauth2_string(my_mail_acct, MAIL_ACC_TOKEN, as_base64=True)
    context = ssl.create_default_context()
    #
    with smtplib.SMTP_SSL("smtp.yandex.ru", port, context=context) as server:
        # server = smtplib.SMTP('smtp.yandex.ru:587')
        server.helo(CLIENT_ID)
        server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
        server.sendmail(sender_email, receiver_email, message.as_string())

    # Create a secure SSL context
    # context = ssl.create_default_context()
    #
    # with smtplib.SMTP_SSL("smtp.yandex.ru", port, context=context) as server:
    #     #server.ehlo(CLIENT_ID)
    #     #server.starttls()
    #     server.login(my_mail_acct, my_mail_password)
    #     server.docmd('AUTH', 'XOAUTH2 ' + auth_string)
    #     server.sendmail(sender_email, receiver_email, message.as_string())


def mail_notify(email_addr, user):
    print(f'sending mail to {user}, addr {email_addr}')
    sender_email = SENDER_MAIL
    send_my_mail(sender_email, email_addr, user)
