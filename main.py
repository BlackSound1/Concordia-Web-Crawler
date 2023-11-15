from scrapy.crawler import CrawlerProcess
from P4.spiders.ConcordiaSpider import MainSpider


def main():
    process = CrawlerProcess()

    process.crawl(MainSpider)
    process.start()


if __name__ == '__main__':
    main()
