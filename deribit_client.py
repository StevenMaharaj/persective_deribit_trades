import websockets
import asyncio
import json
from queue import Queue
import requests
from events import Event


class DeribitTradeClient:
    def __init__(self, instrument_names, event_queue: Queue):
        self.instrument_names = instrument_names
        self.event_queue = event_queue

    @staticmethod
    def get_exchange_info(asset: str):
        assert asset == "BTC" or asset == "ETH", "asset must equal BTC or ETH"
        url = f"https://www.deribit.com/api/v2/public/get_instruments?currency={asset}&expired=false&kind=future"
        response = requests.get(url)
        response_dict = response.json()
        return response_dict['result']

    @staticmethod
    def clean(response: str):
        res = {}
        temp = json.loads(response)
        # print(temp)
        # print(len(temp['params']['data']))
        res['ts'] = temp['params']['data'][0]['timestamp']
        res['isBuy'] = True if temp['params']['data'][0]['direction'] == 'buy' else False
        res["sym"] = temp['params']['data'][0]["instrument_name"]
        res["price"] = temp['params']['data'][0]["price"]
        res['qty'] = temp['params']['data'][0]['amount']

        return res

    async def handle_messages(self, msg):
        async with websockets.connect('wss://www.deribit.com/ws/api/v2') as websocket:
            await websocket.send(msg)
            response = await websocket.recv()
            while websocket.open:
                response = await websocket.recv()
                # do something with the notifications...
                self.event_queue.put_nowait(Event('deribit', response))
            print('connection closed')

    def start_stream(self):
        msg = \
            {"jsonrpc": "2.0",
             "method": "public/subscribe",
             "id": 42,
             "params": {
                 "channels": [f"trades.{instrument_name}.raw" for instrument_name in self.instrument_names]}
             }

        loop = asyncio.new_event_loop()
        task = loop.create_task(self.handle_messages(json.dumps(msg)))
        loop.run_until_complete(task)

def get_deribit_trade(event_queue: Queue):
    exchange_info = DeribitTradeClient.get_exchange_info("BTC")
    symbols = [el['instrument_name'] for el in exchange_info]
    # symbols.remove("BTC-PERPETUAL")
    trade_stream_deribit = DeribitTradeClient(symbols, event_queue)
    trade_stream_deribit.start_stream()