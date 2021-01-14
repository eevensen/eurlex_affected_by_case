# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EurlexAffectedByCaseItem(scrapy.Item):
    # define the fields for your item here like:
    affected_acq_recno = scrapy.Field()
    affected_celex_number = scrapy.Field()
    affected_text = scrapy.Field()
    affected_court_celex = scrapy.Field()
