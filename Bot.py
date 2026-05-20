import requests
import time

BOT_TOKEN = "8883669866:AAEKLfsZSzZPYwqHSxCAcQhS5LmT2TDYh4Q"
CHAT_ID = "486658987"
INTERVAL = 600

ENDPOINTS = [
    "https://api.criptoya.com/api/yadio/usdt/ves",
    "https://api.criptoya.com/api/binance/usdt/ves",
]

last_ask = None

def get_price():
    for url in ENDPOINTS:
        try:
            r = requests.get(url, timeout=10)
            d = r.json()
            ask = float(d.get("ask") or d.get("totalAsk") or d.get("sell") or 0)
            bid = float(d.get("bid") or d.get("totalBid") or d.get("buy") or 0)
            if ask > 0:
                return ask, bid
        except:
            continue
    return None, None

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=10)
    except:
        pass

def fmt(n):
    return f"{n:,.2f}"

print("Bot iniciado. Enviando señales cada 10 minutos...", flush=True)

last_ask = None

while True:
    try:
        ask, bid = get_price()
        if ask:
            if last_ask is None:
                signal = "⚪ *NEUTRAL* — Primer dato"
            elif ask > last_ask:
                diff = ask - last_ask
                pct = (diff/last_ask)*100
                signal = f"🟢 *SUBE* +{fmt(diff)} VES (+{pct:.4f}%)"
            elif ask < last_ask:
                diff = last_ask - ask
                pct = (diff/last_ask)*100
                signal = f"🔴 *BAJA* -{fmt(diff)} VES (-{pct:.4f}%)"
            else:
                signal = "⚪ *ESTABLE* Sin variación"

            spread = ask - bid if bid else 0
            msg = (
                f"📊 *USDT/VES · Binance*\n\n"
                f"{signal}\n\n"
                f"💰 *ASK:* `{fmt(ask)} VES`\n"
                f"💵 *BID:* `{fmt(bid)} VES`\n"
                f"📈 *Spread:* `{fmt(spread)} VES`"
            )
            send_telegram(msg)
            print(f"Señal enviada: {signal}", flush=True)
            last_ask = ask
        else:
            print("Sin datos, reintentando...", flush=True)
    except Exception as e:
        print(f"Error: {e}", flush=True)

    time.sleep(INTERVAL) # v2
