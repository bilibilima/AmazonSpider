'''
Questo file serve a:
- Spedire una Email nel caso uno o più prezzi di un prodotto scendono al prezzo voluto
'''

# librerie
import smtplib, ssl
import getpass

class EmailSender:
    def __init__(self, sender_email, receiver_email, sender_passwd):
        self.port = 587
        self.smtp_server = "smtp.gmail.com"
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.sender_passwd = sender_passwd

    def send_email(self, asin, name, price, link):
        # restituisce un context con le impostazioni di sicurezza predefinite
        context = ssl.create_default_context()

        # messaggio
        message = f"""\
            Subject: IT'S TIME TO BUY THIS PRODUCT


            Now you can buy {name} with {price}:

            Click Here --->  {link} <---

            Here there are the info:
            - Asin = {asin}
            - Name = {name}
            - Price = {price} $
            - Link = {link}
        """

        # connessione al server SMTP
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            # funzione per identificarsi ad un server ESMTP
            server.ehlo() # può essere omesso
            server.starttls(context = context) # funzione per criptare il messaggio
            server.ehlo()
            server.login(self.sender_email, self.sender_passwd)
            server.sendmail(self.sender_email, self.receiver_email, message)


