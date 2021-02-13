import scrapy
import pandas as pd
from scrapy import Selector
import requests
from ..items import EurlexAffectedByCaseItem


class AffectedByCaseSpider(scrapy.Spider):
    name = 'affected_by_case'
    handle_httpstatus_list = [404, 500]
    allowed_domains = []

    def start_requests(self):
        csv_file = "https://www.efta.int/sites/default/files/feeds/eea-lex/9_91c_EEA_Lex_3_0_export.csv"
        df = pd.read_csv(csv_file, usecols=["acq_recno", "celex_number",
                                            "case_status"])  # extract three fields/columns from csv file
        df = df.drop(df[df.celex_number.isnull()].index)  # drop row if field/column 'celex_number' is null
        df = df.drop(
            df[df.celex_number.str[0] != '3'].index)  # drop row if field/column 'celex_number' doesn't start with '3'
        df = df.drop(df[df.case_status == 0].index)  # drop row if field/column 'case_status' is '0'
        df = df.drop(df[df.case_status == 1].index)  # drop row if field/column 'case_status' is '1'
        df = df.drop(df[df.case_status == 6].index)  # drop row if field/column 'case_status' is '6'
        df = df.drop(df[df.case_status == 8].index)  # drop row if field/column 'case_status' is '8'

        base_url = "https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:"  # base url to be concatenated with the celex number.

        for row in df.iterrows():  # iterate over rows and parse generated urls based on celex numbers
            acq_recno = row[1][0]  # extract field acq_recno from csv row
            celex_number = row[1][1]  # extract field celex number from csv row
            url = str(base_url) + str(
                celex_number)  # concatenate base url with celex number. For example 'https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32000L0060'
            yield scrapy.Request(url, dont_filter=True, callback=self.parse,
                                 meta={'celex_number': celex_number,
                                       'acq_recno': acq_recno,
                                       })

    def parse(self, response):
        meta = response.request.meta

        if response.status != 404:
            return self.parse_body(response.body, response.url, response.request.meta)
        else:
            print ("\n" * 2)
            print ('URL: %s' % response.url)
            print ('SPIDER RETURNS 404 - TRYING ALTERNATIVE REQUEST METHOD...')
            print ("\n" * 2)

            meta['notify'] = 1
            x = requests.get(response.url)
            print ('STATUS: %s' % x.status_code)
            return self.parse_body(x.content, response.url, meta)

    def parse_body(self, body, url, meta):
        sel = Selector(text=body)

        notfound = 'The requested document does not exist.'

        if 'notify' in meta and b'The requested document does not exist.' in body:
            print ("\n" * 2)
            print (notfound)
            print (url)
            print ("\n" * 2)
            return

        pplinked_affected_by_lis = sel.xpath(
            "//div[@id='PPLinked_Contents']/div/dl/dt[contains(.,'Affected by case')]/following-sibling::dd[1]/ul/li")  # xpath to extract li elements under "Affected by case"

        # print ("\n")
        # print ('Affected Case: %s' % pplinked_affected_by_lis)
        # print ("\n")
        if len(pplinked_affected_by_lis) == 0:
            # print ('URL: %s' % url)
            # print ('Affected by case not found on document')
            return

        for li in pplinked_affected_by_lis:
            affected_text = li.xpath(
                ".//text()").get()

            affected_court_celex = li.xpath(
                ".//a/text()").get()

            if 'notify' in meta:
                print ("\n" * 2)
                print ('!!!FOUND!!!')

            item = EurlexAffectedByCaseItem()
            item['affected_acq_recno'] = meta['acq_recno']
            item['affected_celex_number'] = meta['celex_number']
            item['affected_text'] = affected_text.strip()
            item['affected_court_celex'] = affected_court_celex

            yield item
