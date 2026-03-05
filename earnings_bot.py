import requests
import schedule
import time
from datetime import date

API_KEY = "d6kj5t1r01qg51f44qdgd6kj5t1r01qg51f44qe0"
WEBHOOK = "https://discord.com/api/webhooks/1479019811513172040/0Tip7R6LOIqE2hmOxcgBEjvn91YllDaidLPJcnXWfmHrvH-C6fmtKeayl1GznMqNMyKy"


def send_discord(message):
    try:
        requests.post(WEBHOOK, json={"content": message})
        print("Sent to Discord")
    except:
        print("Discord webhook failed")


# DAILY EARNINGS
def today_earnings():

    today = date.today()

    url = f"https://finnhub.io/api/v1/calendar/earnings?from={today}&to={today}&token={API_KEY}"

    try:
        data = requests.get(url).json()
    except:
        return

    message = "📊 **Today's Earnings**\n\n"

    earnings = data.get("earningsCalendar", [])

    for company in earnings[:15]:

        symbol = company.get("symbol", "Unknown")
        hour = company.get("hour", "TBA")

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

    try:
        data = requests.get(url).json()
    except:
        return

    message = "📅 **Weekly Earnings Watchlist**\n\n"

    earnings = data.get("earningsCalendar", [])

    for company in earnings[:25]:

        symbol = company.get("symbol", "Unknown")
        message += f"{symbol}\n"

    send_discord(message)


# PREMARKET GAPPERS
def premarket_gappers():

    url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={API_KEY}"

    try:
        stocks = requests.get(url).json()
    except:
        return

    message = "🚨 **Premarket Movers**\n\n"

    count = 0

    for stock in stocks[:200]:

        if count >= 10:
            break

        symbol = stock.get("symbol")

        try:
            quote = requests.get(
                f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
            ).json()
        except:
            continue

        pc = quote.get("pc")
        c = quote.get("c")

        if pc and pc != 0 and c:

            change = ((c - pc) / pc) * 100

            if abs(change) > 5:

                message += f"{symbol} — {round(change,2)}%\n"
                count += 1

    if count > 0:
        send_discord(message)


# AFTER HOURS MOVERS
def after_hours():

    url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={API_KEY}"

    try:
        stocks = requests.get(url).json()
    except:
        return

    message = "📈 **After Hours Movers**\n\n"

    count = 0

    for stock in stocks[:200]:

        if count >= 10:
            break

        symbol = stock.get("symbol")

        try:
            quote = requests.get(
                f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
            ).json()
        except:
            continue

        pc = quote.get("pc")
        c = quote.get("c")

        if pc and pc != 0 and c:

            change = ((c - pc) / pc) * 100

            if abs(change) > 5:

                message += f"{symbol} — {round(change,2)}%\n"
                count += 1

    if count > 0:
        send_discord(message)


# SCHEDULE TASKS
schedule.every().day.at("08:00").do(today_earnings)
schedule.every().sunday.at("20:00").do(weekly_earnings)
schedule.every().day.at("09:00").do(premarket_gappers)
schedule.every().day.at("16:10").do(after_hours)


print("Trading bot running...")

send_discord("✅ Trading bot is now online")


# TEST RUN (runs immediately when bot starts)
today_earnings()
premarket_gappers()
after_hours()


while True:

    try:
        schedule.run_pending()
    except:
        print("Scheduler error")

    time.sleep(60)