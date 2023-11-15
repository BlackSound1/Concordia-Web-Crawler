import scrapy
from pathlib import Path


class MySpider(scrapy.Spider):
    name = 'concordia'
    start_urls = ['https://www.concordia.ca']

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings=settings)
        settings.set('ROBOTSTXT_OBEY', 'True', priority='spider')

    def parse(self, response, **kwargs):
        self.log(f"SEX: {response.url}")
        page = response.url.split('//')[-1]
        filename = f'html-files/{page}.html'
        Path('html-files').mkdir(exist_ok=True, parents=True)
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file: {filename}")
