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
from email_sender import *
from cryptography.fernet import Fernet

class PriceController():
    def __init__(self, sender_passwd):
        self.name = 'info.json'
        self.price_treshold = None
        self.receiver_email = None
        self.sender_passwd = sender_passwd

        # entrare nella cartella .data
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        os.chdir('../.data')

    def controll_price(self):
        self.extract_emaildata()
        with open(self.name, 'r') as f:
            data = json.load(f)
            
            for product in data:
                try:
                    pr_price = float(product['price'])

                except ValueError:
                    pr_price = int(product['price'])

                pr_name = str(product['name'])
                pr_asin = str(product['asin'])
                pr_link = product['link']

                if pr_price <= self.price_treshold:
                    emailsender = EmailSender(
                        sender_email = '0WhoIsCandice0@gmail.com',
                        receiver_email = self.receiver_email,
                        sender_passwd = self.sender_passwd
                    )

                    emailsender.send_email(pr_asin, pr_name, pr_price, pr_link)

    def delete_extralines(self):
        # apertura del file in lettura
        with open(self.name, 'r') as f:
            data = json.load(f)

            for i in range(len(data)):
                if i >= len(data) - 1:
                    pass

                else:
                    if data[i]['asin'] == data[i + 1]['asin']:
                        del data[i]

        # apertura del file in scrittura
        with open(self.name, 'w') as f:
          data = json.dump(data, f)

    def extract_emaildata(self):
        # entrare nella cartella .data
        with open('pcontroller_setting.json', 'r') as f:
            data = json.load(f)

        self.price_treshold = data['price_treshold']
        self.receiver_email = data['receiver_email']
            

sender_passwd = getpass.getpass(prompt = "Sender's Password: ")

price_controller = PriceController(sender_passwd = sender_passwd)
# price_controller.delete_extralines()
price_controller.controll_price()
