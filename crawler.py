from urllib.request import Request, urlopen
from urllib.parse import urlparse, urljoin
from urllib.error import URLError
import ssl
from bs4 import BeautifulSoup
from queue import Queue
from threadsafeset import ThreadSafeSet

class Crawler:
    base_url = ''
    myssl = ssl.create_default_context()
    myssl.check_hostname=False
    myssl.verify_mode=ssl.CERT_NONE
    errorLinks = ThreadSafeSet()
    crawledLinks = ThreadSafeSet()

    def __init__(self, base_url):
        Crawler.base_url = base_url

    @staticmethod
    def crawl(thread_name, url, linksToCrawl):
        try:
            link = urljoin(Crawler.base_url, url)

            if urlparse(link).netloc == urlparse(Crawler.base_url).netloc:
                # Atomic check-and-add: prevents duplicate crawls
                if Crawler.crawledLinks.add_if_not_present(link):
                    request = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                    response = urlopen(request, context=Crawler.myssl)
                    print("Url {} Crawled with Status: {} : {} Crawled In Total".format(response.geturl(), response.getcode(), len(Crawler.crawledLinks)))
                    soup = BeautifulSoup(response.read(), "html.parser")
                    Crawler.enqueueLinks(soup.find_all('a'), linksToCrawl)
        except URLError as e:
            print("URL {} threw this error when trying to parse: {}".format(link, e.reason))
            Crawler.errorLinks.add_if_not_present(link)

    @staticmethod
    def enqueueLinks(links, linksToCrawl: Queue):
        for link in links:
            if (urljoin(Crawler.base_url, link.get('href')) not in Crawler.crawledLinks):
                if (urljoin(Crawler.base_url, link.get('href')) not in linksToCrawl):
                    linksToCrawl.put(link.get('href'))