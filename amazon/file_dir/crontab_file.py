''' file che verra eseguito ad ogni boot del pc'''

# librerie
from datetime import datetime
import os
import scrapy
import datetime
from date_check import Date_Check

# entare nella cartella amazon
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir('..')

def execute_spider():
    # esecuzione dello spider
    os.system('scrapy crawl Amazon -O .data/info.json')

    # esecuzione del controllo prezzi
    os.system('python3 file_dir/price_controller.py')

date_check = Date_Check(file_name = '.data/date_file.date')

# controllo della possibilità di eseguire lo spider
actual_date = str(datetime.date.today()).strip('\n').split('-')

date_check.check_date(date = actual_date, callback = execute_spider)