import perspective
import tornado
import logging
from threading import Thread
from app_setup import loop
from table_setup import Table
from deribit_client import *
from threading import Thread
from events import *
from deribit_client import DeribitTradeClient
import sys


def feed_Table(event_queue:Queue):
    while True:
        try:
            event: Event = event_queue.get()

            if event.event_type == 'deribit':
                cleaned_event_info = DeribitTradeClient.clean(event.info)
                Table.update([cleaned_event_info])
        except KeyboardInterrupt:

            sys.exit(0)


event_queue = Queue()
stream_from_deribit_thread = Thread(target=get_deribit_trade, args=(event_queue,))
stream_from_deribit_thread.daemon = True
stream_from_deribit_thread.start()

feed_Table_thread = Thread(target=feed_Table, args=(event_queue,))
feed_Table_thread.daemon = True
feed_Table_thread.start()

loop.start()
