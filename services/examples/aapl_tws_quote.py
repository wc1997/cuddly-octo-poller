#!/usr/bin/env python3

import os
import time
import threading

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper

class IBApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.connected_event = threading.Event()

    def nextValidId(self, orderId):
        print(f"Connected. nextValidId={orderId}")
        self.connected_event.set()

    def error(self, reqId, errorCode, errorString):
        print(f"Error {errorCode}: {errorString}")

    def marketDataType(self, reqId, marketDataType):
        # 1=live, 2=frozen, 3=delayed, 4=delayed-frozen
        print(f"MarketDataType. reqId={reqId}, type={marketDataType}")

    def tickPrice(self, reqId, tickType, price, attrib):
        print(f"Tick Price. Ticker Id: {reqId}, tickType: {tickType}, Price: {price}")


def main():
    app = IBApp()
    host = os.getenv("IBKR_HOST", "127.0.0.1")
    port = int(os.getenv("IBKR_PORT", "4002"))
    client_id = int(os.getenv("IBKR_CLIENT_ID", "999"))
    exchange = os.getenv("IBKR_EXCHANGE", "BATS")
    primary_exchange = os.getenv("IBKR_PRIMARY_EXCHANGE", "NASDAQ")

    def run_loop():
        app.run()

    # Start the socket in a separate thread
    api_thread = threading.Thread(target=run_loop, daemon=True)
    api_thread.start()

    # Connect to TWS or IB Gateway
    print(f"Connecting to {host}:{port} with clientId={client_id}...")
    app.connect(host, port, clientId=client_id)

    if not app.connected_event.wait(timeout=15):
        print("Connection handshake timed out.")
        app.disconnect()
        return

    # Request delayed market data (about 15 minutes delayed).
    app.reqMarketDataType(3)

    # Define the contract for AAPL stock
    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = exchange
    if exchange.upper() == "SMART":
        contract.primaryExchange = primary_exchange
    contract.currency = "USD"

    print(
        f"Requesting market data for {contract.symbol} on exchange={contract.exchange}"
        + (f", primaryExchange={contract.primaryExchange}" if exchange.upper() == "SMART" else "")
    )

    # Request market data
    app.reqMktData(1, contract, "", False, False, [])
    # app.reqHistoricalData(1, contract, "", "1 M", "1 day", "MIDPOINT", 1, 1, False, [])

    # Sleep to allow data to be received
    time.sleep(5)

    # Disconnect from TWS
    app.disconnect()

if __name__ == "__main__":
    main()
