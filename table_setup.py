import perspective
from schemas import *

from deribit_client import DeribitTradeClient
Table = perspective.Table(sch, index='sym')

exchange_info = DeribitTradeClient.get_exchange_info("BTC")
symbols = [el['instrument_name'] for el in exchange_info]
expiries = [el['expiration_timestamp'] for el in exchange_info]
first_update = []
for i,symbol in enumerate(symbols):
    if symbol == "BTC-PERPETUAL" or symbol == "ETH-PERPETUAL":
        expiry = datetime.today()
    else:
        expiry = datetime.fromtimestamp(expiries[i]/1000)
    first_update.append({'sym':symbol,'expiry':expiry})
Table.update(first_update)
# view = Table.view()
MANAGER = perspective.PerspectiveManager()
MANAGER.host_table('data_source_one',Table)