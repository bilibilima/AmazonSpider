# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class AmazonPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if not adapter.get('price'):
            raise DropItem(f'Missing price in {item}')

        elif not adapter.get('name'):
            raise DropItem(f'Missing name in {item}')

        elif not adapter.get('info') and len(adapter.get('info')) != 0:
            raise DropItem(f'Missing info in {item}')

        else:
            return item