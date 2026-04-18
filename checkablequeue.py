from queue import Queue

class CheckableQueue(Queue):
    # we need this additional method to our queue object to check the link found by the crawler has been already crawled previously or not. This method will then just check through 'crawledLinks' to see if link is there, if not, crawl the link
    def __contains__(self, item):
        with self.mutex:
            return item in self.queue

    # commenting this out because the primitive queue object already has a qsize() method defined. Might as well use that since it's no different than this __len__ method.
    # def __len__(self):
    #     return len(self.queue)