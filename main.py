from scrapy.crawler import CrawlerProcess
from P4.spiders.ConcordiaSpider import MainSpider
from P4.spiders.LinkSpider import LinkSpider
from twisted.internet import reactor, defer


@defer.inlineCallbacks
def crawl(*processes: CrawlerProcess):
    yield processes[0].crawl(MainSpider)

    with open('text_files/concordia_links.txt', 'rt') as f:
        links = [l.strip('\n') for l in f.readlines()]

    yield processes[1].crawl(LinkSpider, start_urls=links)

    reactor.stop()


def main():
    concordia_process = CrawlerProcess()
    links_process = CrawlerProcess()

    crawl(concordia_process, links_process)

    reactor.run()


if __name__ == '__main__':
    main()
