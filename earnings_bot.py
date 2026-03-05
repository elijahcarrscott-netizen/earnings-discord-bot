import requests
import schedule
import time
from datetime import date

API_KEY = "d6kj5t1r01qg51f44qdgd6kj5t1r01qg51f44qe0"
WEBHOOK = "https://discord.com/api/webhooks/1479019811513172040/0Tip7R6LOIqE2hmOxcgBEjvn91YllDaidLPJcnXWfmHrvH-C6fmtKeayl1GznMqNMyKy"


def send_discord(message):
    requests.post(WEBHOOK, json={"content": message})


# DAILY EARNINGS
def today_earnings():

    today = date.today()

    url = f"https://finnhub.io/api/v1/calendar/earnings?from={today}&to={today}&token={API_KEY}"
    data = requests.get(url).json()

    message = "📊 **Today's Earnings**\n\n"

    for company in data["earningsCalendar"][:15]:

        symbol = company.get("symbol","Unknown")
        hour = company.get("hour","TBA")

        if hour == "bmo":
            hour = "Before Market Open"
        elif hour == "amc":
            hour = "After Market Close"

        message += f"**{symbol}** — {hour}\n"

    send_discord(message)


# WEEKLY EARNINGS
def weekly_earnings():

    today = date.today()

    url = f"https://finnhub.io/api/v1/calendar/earnings?from={today}&to={today}&token={API_KEY}"
    data = requests.get(url).json()

    message = "📅 **Weekly Earnings Watchlist**\n\n"

    for company in data["earningsCalendar"][:25]:

        symbol = company.get("symbol","Unknown")
        message += f"{symbol}\n"

    send_discord(message)


# PREMARKET GAPPERS
def premarket_gappers():

    url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={API_KEY}"
    stocks = requests.get(url).json()

    message = "🚨 **Premarket Movers**\n\n"

    count = 0

    for stock in stocks:

        if count >= 10:
            break

        symbol = stock.get("symbol")

        quote = requests.get(f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}").json()

        if quote["pc"] != 0:

            change = ((quote["c"] - quote["pc"]) / quote["pc"]) * 100

            if abs(change) > 5:

                message += f"{symbol} — {round(change,2)}%\n"
                count += 1

    send_discord(message)


# AFTER HOURS MOVERS
def after_hours():

    url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={API_KEY}"
    stocks = requests.get(url).json()

    message = "📈 **After Hours Movers**\n\n"

    count = 0

    for stock in stocks:

        if count >= 10:
            break

        symbol = stock.get("symbol")

        quote = requests.get(f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}").json()

        if quote["pc"] != 0:

            change = ((quote["c"] - quote["pc"]) / quote["pc"]) * 100

            if abs(change) > 5:

                message += f"{symbol} — {round(change,2)}%\n"
                count += 1

    send_discord(message)


# SCHEDULE
schedule.every().day.at("08:00").do(today_earnings)
schedule.every().sunday.at("20:00").do(weekly_earnings)
schedule.every().day.at("09:00").do(premarket_gappers)
schedule.every().day.at("16:10").do(after_hours)

print("Trading bot running...")

while True:
    schedule.run_pending()
    time.sleep(60)