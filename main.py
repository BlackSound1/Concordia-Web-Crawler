from scrapy.crawler import CrawlerProcess, CrawlerRunner
from P4.spiders.ConcordiaSpider import MainSpider
from P4.spiders.LinkSpider import LinkSpider
from twisted.internet import reactor


def main():
    process = CrawlerProcess()

    # process.crawl(MainSpider)
    # process.start()

    with open('text_files/concordia_links.txt', 'rt') as f:
        links = [l.strip('\n') for l in f.readlines()]

    # print(links)
    process.crawl(LinkSpider, start_urls=links)
    process.start()


if __name__ == '__main__':
    main()
