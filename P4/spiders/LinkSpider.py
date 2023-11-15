import logging

import scrapy
from pathlib import Path


class LinkSpider(scrapy.Spider):
    name = 'links'

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings=settings)
        settings.set('ROBOTSTXT_OBEY', 'True', priority='spider')

    def parse(self, response, **kwargs):
        page = response.url.split('//')[-1].replace('/', '-')
        filename = f'html_files/{page}'
        Path('html_files').mkdir(exist_ok=True, parents=True)
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file: {filename}")
