import logging

import scrapy
from pathlib import Path
from urllib.parse import urljoin


class MainSpider(scrapy.Spider):
    """
    This spider's purpose is to read https://www.concordia.ca, find all the links therein,
    and save those links to a file. Those links will be traversed by a different spider with different rules.
    """

    name = 'concordia'  # Set this spider's name
    start_urls = ['https://www.concordia.ca']  # Set this spider's URLs to crawl from
    max_files = None

    @classmethod
    def update_settings(cls, settings):
        """
        Update the default settings for a Scrapy spider to ensure robots.txt is obeyed.

        Inspired by:
        https://docs.scrapy.org/en/latest/topics/settings.html?highlight=update%20settings#settings-per-spider
        :param settings: The settings to update.
        """

        # Update the settings of the base Scrapy spider with the given settings
        super().update_settings(settings=settings)

        # Set the ROBOTSTXT_OBEY setting
        settings.set('ROBOTSTXT_OBEY', 'True', priority='spider')

    def parse(self, response, **kwargs):
        """
        Parse the required URL, save the site's HTML to a file, find all the links on the page, then save those
        links to a file. Inspired by various examples in: https://docs.scrapy.org/en/latest/intro/tutorial.html.

        :param response: The response after crawling the page
        :param kwargs: Any kwargs
        """

        # Get the actual page name, removing 'https://'
        page = response.url.split('//')[-1]

        # Set the filename to save
        filename = f'html_files/{page}.html'

        # Ensure the required directory exists and write the HTML for the page into the file
        Path('html_files').mkdir(exist_ok=True, parents=True)
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file: {filename}")

        # Get all links on Concordia.ca
        links = response.css("a::attr(href)").extract()

        self.log(f"On {page}, found {len(links)} links in total", level=logging.INFO)

        # From these links, get all links that stay on Concordia.ca, that aren't just '/'
        concordia_links = [urljoin(response.url, link) for link in links if
                           link.startswith('/') and link != '/' and not link.startswith('#')]
        self.log(f"From all links found on {page}, found {len(concordia_links)} Concordia links",
                 level=logging.INFO)

        # If there is a valid max_files number specified, reduce the amount of links to parse to the first
        # max_files of them
        if self.max_files is not None and self.max_files >= 0:
            concordia_links = concordia_links[: self.max_files]

        # Write the final list of urls to file
        self.log(f'Writing Concordia links to P4/concordia_links.txt', level=logging.INFO)
        Path('text_files').mkdir(exist_ok=True, parents=True)
        with open('text_files/concordia_links.txt', 'wt') as f:
            f.write('\n'.join(concordia_links))
