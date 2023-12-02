from pathlib import Path

from scrapy.crawler import CrawlerProcess
from argparse import ArgumentParser

from P4.spiders.MainSpider import MainSpider


# Create an argument parser to let user decide how many files to process
parser = ArgumentParser(description="Concordia Scraper")
parser.add_argument('--num_files', metavar='n', type=int,
                    help="The number of files to process", default=10, required=False)


def main():

    # Parse the command-line arguments passed to this script, if any
    args = parser.parse_args()

    # Clear the file folder(s)
    clear_folder()

    # Create and run a CrawlerProcess based on the spider
    process = CrawlerProcess()
    process.crawl(MainSpider, max_files=args.num_files)
    process.start()


def clear_folder():
    """
    Delete the contents of html_files when starting the app.
    """

    # for path in Path('html_files/').glob('*'):
    #     if path.is_file():
    #         path.unlink()

    for path in Path('text_files/').glob('*'):
        if path.is_file():
            path.unlink()


if __name__ == '__main__':
    main()
