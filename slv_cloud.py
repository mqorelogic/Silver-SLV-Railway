SLV Cloud - Day-Only
TICKER: SLV - ENTRY: 08:01 ET - FLATTEN: 15:58 ET
"""

import os, csv, logging
from datetime import datetime
import pytz
from alpaca_trade_api import REST
from alpaca_trade_api.rest import TimeFrame

TICKER = "SLV"
ENTRY_TIME = "08:01"
FLATTEN_TIME = "15:58"
NOTIONAL_DOLLARS = 90
TAKE_PROFIT_PCT = 0.006
STOP_LOSS_PCT = 0.0045

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s",
    handlers=[logging.FileHandler("slv_cloud.log"), logging.StreamHandler()])

def et_now():
    return datetime.now(pytz.timezone("US/Eastern"))

def get_api():
    return REST(os.getenv("APCA_API_KEY_ID"), os.getenv("APCA_API_SECRET"),
                os.getenv("APCA_BASE_URL", "https://paper-api.alpaca.markets"))

def audit(action, detail):
    with open("slv_cloud_audit.csv", "a", newline="") as f:
        csv.writer(f).writerow([et_now().isoformat(), action, TICKER, detail])

def run():
    now = et_now()
    api = get_api()
    if not api.get_clock().is_open:
        logging.info("SLV Cloud - Market closed SKIP")
        return
    try:
        pos = api.get_position(TICKER)
    except:
        pos = None
    cur = now.strftime("%H:%M")
    if cur >= FLATTEN_TIME:
        if pos:
            api.close_position(TICKER)
            logging.info(f"SLV Cloud FLATTEN OK - closed {pos.qty} {TICKER}")
            audit("FLATTEN", f"Closed {pos.qty}")
        else:
            logging.info("SLV Cloud FLATTEN - already flat")
        return
    if pos:
        logging.info(f"SLV Cloud SKIP - already in {TICKER}")
        return
    if cur < ENTRY_TIME:
        logging.info(f"SLV Cloud SKIP - before {ENTRY_TIME}")
        return
    try:
        last = float(api.get_latest_trade(TICKER).price)
    except:
        bars = api.get_bars(TICKER, TimeFrame.Minute, limit=1).df
        last = float(bars["close"].iloc[-1])
    tp = round(last * (1 + TAKE_PROFIT_PCT), 2)
    sl = round(last * (1 - STOP_LOSS_PCT), 2)
    order = api.submit_order(symbol=TICKER, notional=NOTIONAL_DOLLARS, side="buy",
        type="market", time_in_force="day", order_class="bracket",
        take_profit=dict(limit_price=tp), stop_loss=dict(stop_price=sl))
    logging.info(f"SLV Cloud BRACKET OK - {TICKER} entry ~{last} TP {tp} SL {sl} ID {order.id}")
    audit("BRACKET OK", f"Entry {last} TP {tp} SL {sl} Notional ${NOTIONAL_DOLLARS}")

if __name__ == "__main__":
    run()
