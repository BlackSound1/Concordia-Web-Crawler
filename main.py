from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor, defer

from P4.spiders.ConcordiaSpider import MainSpider
from P4.spiders.LinkSpider import LinkSpider


@defer.inlineCallbacks
def crawl(*processes: CrawlerProcess):
    """
    A callback generator function to define how the CrawlerProcesses are called.

    :param processes: 1 or more CrawlerProcesses. Must have a concordia process and link process,
                      but allows for extensibility.
    :return: The results of each spider crawl
    """

    # Crawl with the concordia spider
    yield processes[0].crawl(MainSpider)

    # Get all the links to traverse the links spider with
    with open('text_files/concordia_links.txt', 'rt') as f:
        links = [l.strip('\n') for l in f.readlines()]

    # Crawl with the links spider, given the links to crawl
    yield processes[1].crawl(LinkSpider, start_urls=links)

    # End the process once finished
    reactor.stop()


def main():
    # Create 2 processes, 1 for each spider
    concordia_process = CrawlerProcess()
    links_process = CrawlerProcess()

    # Call the crawl callback function
    crawl(concordia_process, links_process)

    # Actually run the twisted reactor
    reactor.run()


if __name__ == '__main__':
    main()
