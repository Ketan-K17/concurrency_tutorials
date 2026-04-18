import threading

class ThreadSafeSet:
    """A thread-safe set wrapper using locks."""
    def __init__(self):
        self._set = set()
        self._lock = threading.Lock()

    def add(self, item):
        with self._lock:
            self._set.add(item)

    def __contains__(self, item):
        with self._lock:
            return item in self._set

    def __len__(self):
        with self._lock:
            return len(self._set)

    def add_if_not_present(self, item):
        """Atomically check if item is present and add it if not.
        Returns True if the item was added, False if it was already present."""
        with self._lock:
            if item not in self._set:
                self._set.add(item)
                return True
            return False
