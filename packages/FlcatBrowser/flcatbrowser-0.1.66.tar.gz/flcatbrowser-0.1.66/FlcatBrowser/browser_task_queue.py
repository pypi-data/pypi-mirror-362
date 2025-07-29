import random
import threading
import time
from typing import Type
from .browser import BaseBrowser
from .utils.task_queue import TaskQueue, Worker

class BrowserWorker(Worker):
    def __init__(self, task_queue: "TaskQueue", browser: BaseBrowser, *args, **kwargs):
        super().__init__(task_queue, *args, **kwargs)
        self.browser = browser

class BrowserTaskQueue(TaskQueue):
    def __init__(self, browser_class: Type[BaseBrowser], proxy_ip = '', num_workers: int = 2, max_size: int = 0, create_interval_time: int = None):
        self.proxy_ip = proxy_ip
        self.browser_class =browser_class
        super().__init__(num_workers, max_size, create_interval_time)

    def create_worker(self, index):
        worker = BrowserWorker(
            self, 
            self.browser_class(str(index+1), self.proxy_ip), 
            name=f"Worker-{index+1}"
        )
        worker.start()
        self.workers.append(worker)