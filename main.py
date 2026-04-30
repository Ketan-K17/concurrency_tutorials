import threading
from crawler import *
from checkablequeue import *
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv

THREAD_COUNT = 20
linksToCrawl = CheckableQueue()

# def createCrawlers(): # our thread factory
#     for i in range(THREAD_COUNT):
#         t = threading.Thread(target=consume_link, daemon=True)
#         t.start()

def appendToCSV(result):
    print("Appending result to CSV File: {}".format(result))
    with open('results.csv', 'a') as csvfile:
        resultwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        resultwriter.writerow(result)

def consume_link(url):
    try:
        Crawler.crawl(threading.current_thread(), url, linksToCrawl)
    except:
        print("Exception thrown with link: {}".format(url))
    finally:
        linksToCrawl.task_done()
    
def main():
    url = input("Website > ")
    Crawler(url)
    linksToCrawl.put(url)
    with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        futures = []
        while True:
            try:
                link = linksToCrawl.get(timeout=1)
                if link is not None:
                    future = executor.submit(consume_link, link)
                    futures.append(future)
            except:
                if linksToCrawl.empty():
                    break

        for future in as_completed(futures):
            try:
                if future.result() != None:
                    appendToCSV(future.result())
            except:
                print(future.exception())

    print("Total Links Crawled: {}".format(len(Crawler.crawledLinks)))
    print("Total Errors: {}".format(len(Crawler.errorLinks)))

if __name__ == '__main__':
    main()