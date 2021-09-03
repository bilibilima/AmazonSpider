'''
Questo file serve a:
- Spedire una Email nel caso uno o più prezzi di un prodotto scendono al prezzo voluto
'''

# librerie
import smtplib, ssl
import getpass
# librerie per migliorare le email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self, sender_email, receiver_email, sender_passwd):
        self.port = 465
        self.smtp_server = "smtp.gmail.com"
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.sender_passwd = sender_passwd
        self.max_passwd = 0

    def send_email(self, asin, name, price, link):
        # restituisce un context con le impostazioni di sicurezza predefinite
        context = ssl.create_default_context()

        # messaggio
        message = MIMEMultipart("alternative")
        message['Subject'] = "IT'S TIME TO BUY THIS PRODUCT"
        message['From'] = self.sender_email
        message['To'] = self.receiver_email

        html = f"""\
            <html><body><p>
            Now you can BUY {name} WITH {price} $<br>
            
            <br> 
            <a href = {link}> CLICK HERE </a><br>
            <br>

            INFORMATIONS<br>
            - Asin = {asin}<br>
            - Name = {name}<br>
            - Price = {price} $<br>
            - Link = {link}<br>

            </p></body></html>
        """

        part = MIMEText(html, 'html')
        message.attach(part)

        # connessione al server SMTP
        with smtplib.SMTP_SSL(self.smtp_server, self.port, context = context) as server:

            try:
                server.login(self.sender_email, self.sender_passwd)

            except:
                while True:
                    self.sender_passwd = getpass.getpass(prompt = "Sender's Password: ")
                    try:
                        server.login(self.sender_email, self.sender_passwd)

                    except smtplib.SMTPAuthenticationError:
                        if self.max_passwd >= 3:
                            print('wrong Password for too many times')
                            quit()

                        else:
                            self.max_passwd += 1
                            continue

                    break
            
            server.sendmail(self.sender_email, self.receiver_email, message.as_string())
            print('-' * 50)
            print('Email sent succesfully')
            print('-' * 50)


