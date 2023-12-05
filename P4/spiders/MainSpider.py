import logging
from pathlib import Path
from urllib.parse import urljoin
from re import sub

import scrapy
from scrapy.exceptions import CloseSpider
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords


# Get first 150 stopwords
stopwords = list(stopwords.words('english'))[:150]


def _clean(string: str) -> str:
    """
    Given a string, clean it according to some rules.

    :param string: The string to clean
    :return: The cleaned string
    """

    # Remove punctuation and special characters
    string = sub(r"[()<>{}\[\]!$=@&*-/|+.,:;`'?\"]+", ' ', string)

    # Remove certain unicode control characters, as found in experiment
    string = sub(r'\xa0|\x03|\x02|\x07|\x05|\xfc|\u007F', ' ', string)

    # Remove multiple spaces
    string = sub(r'\s{2,}', ' ', string)

    # Tokenize string
    tokenized = word_tokenize(string)

    # Remove stopwords
    no_stopwords = [t for t in tokenized if t not in stopwords]

    # Remove numbers
    no_nums = [t for t in no_stopwords if not t.isnumeric()]

    # Lowercase
    lowercase = [t.lower() for t in no_nums]

    # Remove tokens that are of length 1
    no_len_1 = [t for t in lowercase if len(t) != 1]

    # Remove duplicates
    no_dupes = {t for t in no_len_1}

    # Join into single string
    to_return = ' '.join(t for t in no_dupes)

    # Remove surrounding spaces
    to_return = to_return.strip()

    # Ensure 1 space at the end
    to_return = f"{to_return} "

    return to_return


def _fill_page_text(*list_of_lists: list) -> str:
    """
    Turn the given list of lists of page elements into a single string representing the page's content.

    :param list_of_lists: The list of lists of page elements
    :return: The single string representing the page's text
    """

    page_text = ""

    for ls in list_of_lists:
        for item in ls:
            item = _clean(item)
            page_text += f" {item}"

    return page_text


class MainSpider(scrapy.Spider):
    name = 'test'

    allowed_domains = ['www.concordia.ca']
    start_urls = ['https://www.concordia.ca']

    max_files = None
    num_files = 0

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

        # Set the ROBOTSTXT_OBEY setting. This may not be necessary, as the setting is set in settings.py,
        # but this adds a specific line to the Scrapy logs
        settings.set('ROBOTSTXT_OBEY', 'True', priority='spider')

    def parse(self, response, **kwargs):
        """
        Parse the links on a page, and save HTML files of those pages if the maximum number of files
        to download hasn't been reached.

        :param response: The response from the internet
        :param kwargs: Any kwargs
        """

        # First, check to see if we've reached the file download limit. If so, stop the crawler
        if self.num_files >= self.max_files:
            self.log(f"Reached maximum files to save: {self.max_files}", level=logging.INFO)
            raise CloseSpider(f"Reached maximum files to save: {self.max_files}")

        # If we receive a 404, don't bother with parsing this link
        if response.status == 404:
            return

        # Parse the response body
        contents = BeautifulSoup(response.body, features="html.parser", from_encoding='utf-8')

        # Only bother with English pages
        if contents.html['lang'] != "fr":
            # Get the actual page name, removing 'https://', replacing '/' characters for '-' characters.
            # This helps with file saving
            page = response.url.split('//')[-1].replace('/', '-')

            # Replace invalid characters with a '-'
            page = sub(r'[\\/:*?\"<>|]', '-', page)

            # Set the filename to save
            filename = f"text_files/{page}.txt"

            # Set a list of valid HTML to tags to parse. This narrows the scope of the text
            valid_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

            # Get all paragraph text
            paragraphs = [p.text for p in contents.body.find_all('p')]

            # Get all headings by type
            headings_lists = [contents.body.find_all(h) for h in valid_tags[1:]]

            # Flatten the headings list, keeping only the text of each heading
            headings = [item.text for sublist in headings_lists for item in sublist]

            # Get all divs with the 'body' class
            div_bodies = [d.text for d in contents.body.find_all('div', {'class': 'body'})]

            # Get all list items
            list_items = [li.text for li in contents.body.find_all('li')]

            page_text = _fill_page_text(paragraphs, headings, div_bodies, list_items)

            # Ensure the required directory exists and write the HTML for the page into the file
            Path('text_files').mkdir(exist_ok=True, parents=True)
            with open(filename, 'wt', encoding='utf-8') as f:
                f.writelines(page_text)
            self.log(f"Saved file: {filename}")
            self.num_files += 1

            # Get all links on this page
            links = [l['href'] for l in contents.body.find_all('a', href=True)]
            # links = response.css('a::attr(href)').getall()
            self.log(f"On {page}, found {len(links)} links in total", level=logging.INFO)

            # TLDs must be in this list
            allowed_TLDs = ['.html', '.htm', '.ca']

            # From these links, get all links that follow certain rules
            valid_links = [urljoin(response.url, link) for link in links if

                           # If this link starts with '/' then it is an endpoint of Concordia. Keep
                           link.startswith('/')

                           # If the link is only the '/' character, then the link is just the homepage again. Reject
                           and link != '/'

                           # If the link starts with a selector, then it's a section of a page not a new page. Reject
                           and not link.startswith('#')

                           # If the link contains a '?' character, then it's an endpoint query. Too specific.
                           # Want new pages, not just query results from a single page. Reject
                           and '?' not in link

                           # Don't consider links that contain certain words
                           and "francais" not in link
                           and "ucactualites" not in link
                           and 'diplome' not in link
                           and 'traduc' not in link
                           and 'litterature' not in link

                           # If this link has an allowed TLD, Keep
                           and Path(link).suffix in allowed_TLDs]
            self.log(f"From all links found on {page}, found {len(valid_links)} valid links", level=logging.INFO)

            # Recursively follow all valid links using this method
            yield from response.follow_all(valid_links, callback=self.parse)
