# Questo è il file che verrà eseguito ogni volta che si accende il computer per controllare le offerte di un determinato prodotto
# entrare nella  cartella dello spider
cd amazon

# eseguire lo spider
scrapy crawl Amazon -O info.json

# eseguire il programma per controllare i prezzi dei prodotti
python3 price_controller.py
