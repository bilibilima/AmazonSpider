''' Programma principale'''

# librerie
import os
import json
import shutil

class AmazonSpider:
    def __init__(self):
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        self.file_name = 'pcontroller_setting.json'

        # entrata nella cartella amazon
        os.chdir(self.current_path + '/amazon/')

    def controll_product(self, product, treshold, email_receiver):
        # controllo dell'esistenza della cartella .data
        if not os.path.exists('.data'):
            print('La cartella .data non esiste')
            print()
            os.mkdir('.data')
            os.chdir('.data')
            
            pcontroller_info = {'price_treshold' : treshold, 'receiver_email' : email_receiver, 'product' : product}
            # scrittura delle informazioni sopra ad un file .json
            with open(self.file_name, 'w') as f:
                json_dump = json.dump(pcontroller_info, f)
            
            # uscita dalla cartella .data
            os.chdir('..')

            # avvio dello spider per controllare i prezzi attuali
            os.system('scrapy crawl Amazon -O .data/info.json')

            # esecuzione del controllo prezzi
            os.system('python3 file_dir/price_controller.py')

            # creazione del file per l esecuzione giornaliera dello spider
            self._create_pyfile()
            
        else:
            # rimozione della cartella
            shutil.rmtree('.data')
            self.controll_product(product, treshold, email_receiver)
    # alla fine del metodo controll_product() la cartella è amazon

    # metodo per creare un file .py da eseguire ogni volta che il computer si accende
    def _create_pyfile(self):
        # scipt da mettere in un file py
        script = '''\
        
        # librerie
        import os
        import scrapy

        # entare nella cartella amazon
        os.chdir(os.path.abspath(__file__) + '..')

        # esecuzione dello spider
        os.system('scrapy crawl Amazon -O .data/info.json')

        # esecuzione del controllo prezzi
        os.system('python3 file_dir/price_controller.py')    
        '''

        with open('file_dir/amazon_startup.py', 'w') as f:
            f.write(script)

    # alla fine di questo metodo la cartella è amazon

    # metodo per modificare un valore
    def change_value(self, new_value, key):
        if not os.path.exists('.data') and not os.path.isfile('.data/' + self.file_name):
            print('Bisogna prima scegliere un prodotto da controllare')

        else:
            os.chdir('.data')
            # modifica del valore
            with open(self.file_name, 'r') as f:
                json_obj = json.load(f)

            json_obj[key] = new_value
            with open(self.file_name, 'w') as f:
                json.dump(json_obj, f)

            os.chdir('..')
    # alla fine del metodo change_value() la cartella è amazon

# funzione per pulire il terminale
def clear_screen():
    if os.name == 'nt':# il sistema operativo usato è Windows
        os.system('cls')

    elif os.name == 'posix': # il sistema operativo usato è macos/linux
        os.system('clear')


# funzione per verificare l'input
def controll_input(message, input_type):
    while True:
        try:
            answ = input_type(input(message))

        except ValueError:
            print('Valore non consentito')
            print()
            continue
        break
    return answ

def main():
    clear_screen()
    amazon_spider = AmazonSpider()

    start_message = """\
        --------------------------------------------------
                    BENVENUTO IN AMAZON SPIDER
        --------------------------------------------------
        In questo applicativo potrai scegliere un prodotto
        che verrà controllato su amazon
        
        Scegli il numero di queste opzioni:
        """

    options_message = """\
        1) CONTROLLARE UN NUOVO PRODOTTO
        2) CAMBIARE LA SOGLIA MASSIMA DEL PREZZO
        3) CAMBIARE LA EMAIL DEL DESTINATARIO
        4) USCIRE

        """
    
    print(start_message)
    print(options_message)
    
    # controllo se l'opzione esiste
    while True:
        choise = str(input('N. OPZIONE: '))
        
        if choise in ['1','2','3','4']:
            break
        else:
            clear_screen()
            print('OPZIONE NON TROVATA')
            print()
            print(options_message)
    # controllo di un nuovo prodotto
    if choise == '1':
        # richiesta delle informazioni necessarie
        product = str(input('Nome prodotto che si vuole controllare: '))
        message = 'Soglia del prezzo massima: '
        treshold = controll_input(message, float)

        email_receiver = str(input('Email del destinatario: '))

        amazon_spider.controll_product(product, treshold, email_receiver)
        print()
        print('Operazione avvenuta con successo')
        print()
        input("Premere INVIO per continuare")
        main()
    # modifica della soglia massima
    elif choise == '2':
        message = 'Inserire una nuova soglia di denaro massima: '
        new_treshold = controll_input(message, float)

        amazon_spider.change_value(new_treshold, 'price_treshold')
        print()
        print('Operazione avvenuta con successo')
        print()
        input('Premere INVIO per continuare')
        main()
    # modifica del destinatario
    elif choise == '3' :
        new_receiver = str(input('Inserire la nuova email del destinatario: '))
        amazon_spider.change_value(new_receiver, 'receiver_email')
        print()
        print('Operazione aavvenuta con successo')
        print()
        input('Premere INVIO per continuare')
        main()
    elif choise == '4' : quit()

if __name__ == "__main__":
    main()
