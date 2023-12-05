from argparse import ArgumentParser
from pathlib import Path

from scrapy.crawler import CrawlerProcess

from P4.spiders.MainSpider import MainSpider

# Create an argument parser to let user decide how many files to download
parser = ArgumentParser(description="Concordia Scraper")
parser.add_argument('--num-files', '-n', type=int,
                    help="The number of files to process", default=100, required=False)


def main():
    # Parse the command-line arguments passed to this script, if any
    args = parser.parse_args()

    # Clear the file folder(s)
    _clear_folder()

    print("\n--- Web Crawling ---\n")

    # Create and run a CrawlerProcess based on the spider. Inspired by: https://stackoverflow.com/a/31374345
    # Using Scrapy version 2.8.0 https://github.com/scrapy/scrapy
    process = CrawlerProcess()
    process.crawl(MainSpider, max_files=args.num_files)
    process.start()


def _clear_folder():
    """
    Delete the contents of necessary folders when starting the app.
    """

    for path in Path('text_files/').glob('*'):
        if path.is_file():
            path.unlink()

    for path in Path('clusters/').glob('*'):
        if path.is_file():
            path.unlink()


if __name__ == '__main__':
    main()
