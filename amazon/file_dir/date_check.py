# file che crea un file dove saranno presenti tutti gli orari di esecuzione di questo file
# librerie
import datetime
import os

class Date_Check:
    def __init__(self, file_name):
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.file_name = file_name
        # cartella attuale Desktop/Programming/Python/bot/amazon
        os.chdir(self.file_path)
        os.chdir('..')

    def __write_date(self):
        day = datetime.date.today()

        # scrittura della data nel file
        with open(self.file_name, 'a') as f:
            f.write(str(day) + '\n')

    def check_date(self, date, callback = None):
        # estrazione del' ultima data
        with open(self.file_name, 'r') as f:
            # controllo se il il file è vuoto
            try:
                last_date = f.readlines()[-1].strip('\n').split('-')
            
                file_year = int(last_date[0])
                file_month = int(last_date[1])
                file_day = int(last_date[2])

                if file_year < int(date[0]) or file_month < int(date[1]) or file_day < int(date[2]):
                    self.__write_date()
                    callback()

            except IndexError:
                self.__write_date()
                self.check_date(date)


