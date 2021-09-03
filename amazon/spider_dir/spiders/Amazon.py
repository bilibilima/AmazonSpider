import scrapy
from scrapy.spiders import Spider
from urllib.parse import urlencode
from amazon.items import AmazonItem
from itemloaders import ItemLoader
import json
import os


# parola chiave da cercare
with open('.data/pcontroller_setting.json', 'r') as f:
    json_obj = json.load(f)

query = json_obj['product']


class AmazonSpider(Spider):
    name = 'Amazon'
    API = '094ccd1e613a15cdb5a3c82ce9a4afc9'
    
    # metodo per mandare le richieste al sito
    def start_requests(self):
        url = 'https://www.amazon.com/s?' + urlencode({'k': query})
        yield scrapy.Request(url = url, callback = self.parse_keyword_response)
    
    '''
    il metodo parse_keyword_response serve a:
    - estrarre tutti i prodotti tramite ASIN(ID identificativo di ogni prodotto di amazon.com)
    - mandare una richiesta alle pagine di ogni prodotto
    - ripetere queste azioni per ogni pagina
    '''
    def parse_keyword_response(self, response):
        products = response.xpath('//*[@data-asin]') # lista di tutti i ASIN dei prodotti

        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = f"https://www.amazon.com/dp/{asin}"
            yield scrapy.Request(
                url = product_url, callback = self.parse_product_page, meta = {'asin': asin}, 
            ) # meta = {} serve per passare degli elementi da una funzione ad un'altra

    # metodo per estrarre tutte le informazioni necessarie dalla pagina del prodotto 
    def parse_product_page(self, response):
        item = AmazonItem()
        l = ItemLoader(item = item, selector = response)
        
        asin = response.meta['asin']
        name_pr = response.xpath("//span[@id='productTitle']//text()").extract_first()
        price_pr = response.xpath("//span[@id='priceblock_ourprice']/text()").extract_first()
        title_info = response.xpath("//td[@class='a-span3']//span[@class='a-size-base a-text-bold']/text()").extract()
        text_info = response.xpath("//td[@class='a-span9']//span[@class='a-size-base']/text()").extract()
        

        # aggiunta delle informazioni al dict items
        l.add_xpath('name', "//span[@id='productTitle']//text()")
        l.add_xpath('price', "//span[@id='priceblock_ourprice']/text()")

        item['asin'] = asin
        item['info'] = {}
        item['link'] = response.url

        for i in range(len(text_info)):
                item['info'][title_info[i]] = text_info[i]

        return item, l.load_item()

    # metodo per spedire la richiesta a Scraper API
    def get_url():
        payload = {'api_key': API, 'url': url, 'country_code' : 'us'}
        proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
        return proxy_url
