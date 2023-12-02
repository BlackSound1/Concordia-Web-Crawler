from pathlib import Path

from scrapy.crawler import CrawlerProcess

from P4.spiders.MainSpider import MainSpider


def main():

    clear_folder()

    # Create and run a CrawlerProcess based on the spider
    process = CrawlerProcess()
    process.crawl(MainSpider, max_files=10)
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
