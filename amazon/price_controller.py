'''
Questo file serve a:
- Aprire il file info.json
- Eliminare le righe in eccesso
- Controllare tutti i prezzi del prodotto
- Mandare una notifica se il prezzo di qualche prodotto combacia
'''
# librerie
import json
import os
import getpass
import sys
from email_sender import *

# entrare nella directory dove si trova il file
current_path = os.path.dirname(__file__)
os.chdir(current_path)


class PriceController():
    def __init__(self, name, price_treshold, receiver_email = 'ilpalbio@gmail.com'):
        self.name = name
        self.price_treshold = price_treshold
        self.receiver_email = receiver_email
        self.sender_passwd = None

    def controll_price(self):
        with open(self.name, 'r') as f:
            data = json.load(f)
            
            for product in data:
                pr_price = float(product['price'])
                pr_name = str(product['name'])
                pr_asin = str(product['asin'])
                pr_link = product['link']

                if pr_price <= self.price_treshold + 10:
                    # controllo se la passwd è già stata inserita
                    if self.sender_passwd == None:
                        self.sender_passwd = getpass.getpass(prompt = "Sender's Password: ")

                    else:
                        pass

                    # controllo se la mail del destinatario è stata inserita
                    if sys.argv[1] != None:
                        self.receiver_email = sys.argv[1]

                    else:
                        pass

                    emailsender = EmailSender(
                        sender_email = '0WhoIsCandice0@gmail.com',
                        receiver_email = self.receiver_email,
                        sender_passwd = self.sender_passwd
                    )

                    emailsender.send_email(pr_asin, pr_name, pr_price, pr_link)

                else:
                    pass

    def delete_extralines(self):
        # apertura del file in lettura
        with open(self.name, 'r') as f:
            lines = f.readlines()

        # apertura del file in scrittura
        with open(self.name, 'w') as f:
            for number, line in enumerate(lines):
                if line.strip("\n") == '[' or line.strip("\n") == ']':
                    f.write(line)

                elif number % 2 == 0:
                    f.write(line)

                else:
                    pass

price_controller = PriceController('info.json', price_treshold = 150)
price_controller.delete_extralines()
price_controller.controll_price()