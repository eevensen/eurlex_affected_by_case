import scrapy
import pandas as pd


class AffectedByCaseSpider(scrapy.Spider):
    name = 'affected_by_case'
    allowed_domains = ['eur-lex.europa.eu']

    def start_requests(self):
        csv_file = "./csv/celex-numbers.csv"
        df = pd.read_csv(csv_file, usecols=["acq_recno", "celex_number",
                                                       "case_status"])  # extract three fields/columns from csv file
        df = df.drop(df[df.celex_number.isnull()].index)  # drop row if field/column 'celex_number' is null
        df = df.drop(
            df[df.celex_number.str[0] != '3'].index)  # drop row if field/column 'celex_number' doesn't start with '3'
        df = df.drop(df[df.case_status == 0].index)  # drop row if field/column 'case_status' is '0'
        df = df.drop(df[df.case_status == 1].index)  # drop row if field/column 'case_status' is '1'
        df = df.drop(df[df.case_status == 6].index)  # drop row if field/column 'case_status' is '6'
        df = df.drop(df[df.case_status == 8].index)  # drop row if field/column 'case_status' is '8'

        base_url = "https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:"  # base url to be concatenated with the celex number. For example 'https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32000L0060'

        for row in df.iterrows():  # iterate over rows and parse generated urls based on celex numbers
            acq_recno = row[1][0]  # extract field acq_recno from csv row
            celex_number = row[1][1]  # extract field celex number from csv row
            url = str(base_url) + str(celex_number)  # concatenate base url with celex number. For example 'https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32000L0060'
            yield scrapy.Request(url, dont_filter=True, callback=self.parse,
                                 meta={'celex_number': celex_number,
                                       'acq_recno': acq_recno,
                                       })

    def parse(self, response):
        celex_number = response.request.meta['celex_number']  # celex number, ex. 32000L0060
        acq_recno = response.request.meta['acq_recno']  # unique ID from EFTA 360, ex. 318588

        pplinked_affected_by_lis = response.xpath(
            "//div[@id='PPLinked_Contents']/div/dl/dt[contains(.,'Affected by case')]/following-sibling::dd[1]/ul/li")  # xpath to extract li elements under "Affected by case"

        for li in pplinked_affected_by_lis:
            affected_text = li.xpath(
                ".//text()").get()

            affected_court_celex = li.xpath(
                ".//a/text()").get()

            yield {
                'affected_acq_recno': acq_recno,
                'affected_celex_number': celex_number,
                'affected_text': affected_text.strip(),
                'affected_court_celex': affected_court_celex,
            }
