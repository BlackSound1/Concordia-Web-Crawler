import logging

import scrapy
from pathlib import Path


class LinkSpider(scrapy.Spider):
    """
    This spider's purpose to is crawl all the links provided in the file and save their HTML to separate files.
    """

    name = 'links'  # Set this spider's name

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
        Parse the page for each URL. Get the HTML associated with that page and save it to a file.

        **Note:** For a more readable file structure, '/' is replaced by '-' in each filename for the URLs.

        :param response: The response after crawling the page
        :param kwargs: Any kawrgs
        """

        # Get the page name for this page, removing 'https://' and replacing all '/' with '-', to save to file easier
        page = response.url.split('//')[-1].replace('/', '-')

        # Set the saved filename for this URL accordingly
        filename = f'html_files/{page}'

        # Write the HTML content for this page to an appropriate file
        Path('html_files').mkdir(exist_ok=True, parents=True)
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file: {filename}")
