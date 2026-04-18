import threading
from crawler import *
from checkablequeue import *

THREAD_COUNT = 20
linksToCrawl = CheckableQueue()

def createCrawlers(): # our thread factory
    for i in range(THREAD_COUNT):
        t = threading.Thread(target=consume_link, daemon=True)
        t.start()

def consume_link():
    while True:
        url = linksToCrawl.get()
        try:
            if url is None:
                break
            Crawler.crawl(threading.current_thread(), url, linksToCrawl)
        except:
            print("Exception")
        finally:
            linksToCrawl.task_done()
    
def main():
    url = input("Website > ")
    Crawler(url)
    linksToCrawl.put(url)
    createCrawlers()
    linksToCrawl.join() # waiting for there to be NO un-explored links in the queue => tasks have finished, we can proceed
    print("Total Links Crawled: {}".format(len(Crawler.crawledLinks)))
    print("Total Errors: {}".format(len(Crawler.errorLinks)))

if __name__ == '__main__':
    main()