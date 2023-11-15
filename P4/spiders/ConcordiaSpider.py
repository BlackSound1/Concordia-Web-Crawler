import logging

import scrapy
from pathlib import Path


class MainSpider(scrapy.Spider):
    name = 'concordia'
    start_urls = ['https://www.concordia.ca']

    @classmethod
    def update_settings(cls, settings):
        super().update_settings(settings=settings)
        settings.set('ROBOTSTXT_OBEY', 'True', priority='spider')

    def parse(self, response, **kwargs):
        page = response.url.split('//')[-1]
        filename = f'html_files/{page}.html'
        Path('html_files').mkdir(exist_ok=True, parents=True)
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file: {filename}")

        # Get all links on Concordia.ca
        links = response.css("a::attr(href)").extract()

        self.log(f"On {page}, found {len(links)} links in total", level=logging.INFO)

        # From these links, get all links that stay on Concordia.ca that aren't just '/'
        concordia_links = [link for link in links if link.startswith('/') and link != '/']

        self.log(f"From all links found on {page}, found {len(concordia_links)} Concordia links",
                 level=logging.INFO)

        self.log(f'Writing Concordia links to P4/concordia_links.txt', level=logging.INFO)

        # Write them to file
        Path('text_files').mkdir(exist_ok=True, parents=True)
        with open('text_files/concordia_links.txt', 'wt') as f:
            f.write('\n'.join(concordia_links))
