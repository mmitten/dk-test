import datetime

import scrapy
 
 
class ScrapeTableSpider(scrapy.Spider):
    name = 'scrape-table'
    allowed_domains = ['https://sportsbook.draftkings.com/leagues/baseball/mlb']
 
 
    def start_requests(self):
        urls = [
            'https://sportsbook.draftkings.com/leagues/baseball/mlb',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
 
    def parse(self, response):
        table = response.xpath('//*[@class="sportsbook-table__body"]//tr')
        for row in table:
            yield {
                'book' : 'draftkings',
                'sport': 'baseball',
                'league' : 'mlb',
                'timestamp': datetime.datetime.timestamp(datetime.datetime.now(datetime.UTC)),
                'day':  response.xpath('//*[@class="sportsbook-table-header__title"]//span//span//text()').extract_first(),
                'event' : row.xpath('th//a[@class="event-cell-link"]/@href').extract_first(),
                'team_name' : row.xpath('th//*[@class="event-cell__name-text"]//text()').extract_first(),
                'run_line' : row.xpath('td[1]//*[@class="sportsbook-outcome-cell__line"]//text()').extract_first(),
                'run_line_odds' : row.xpath('td[1]//*[@class="sportsbook-odds american default-color"]//text()').extract_first(),
                'total': row.xpath('td[2]//*[@class="sportsbook-outcome-cell__line"]//text()').extract_first(),
                'total_odds' : row.xpath('td[2]//*[@class="sportsbook-odds american default-color"]//text()').extract_first(),
                'moneyline_odds' : row.xpath('td[3]//*[@class="sportsbook-odds american no-margin default-color"]//text()').extract_first(),
            }

