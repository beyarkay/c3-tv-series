from datetime import datetime, timedelta
import yaml
import os
import requests
from bs4 import BeautifulSoup

def main():
    # A static list of events to create
    events = [
        {
            "title": "An example event title",
            "description": "An example description.",
            "start": datetime.now(),
            "end": datetime.now() + timedelta(hours=3),
        },
        {
            "title": "An example all-day event",
            "description": "An example description for the all-day event.",
            "start": str(datetime.now().date()),
            "end": str(datetime.now().date()),
        },
    ]
    
    # Attempt to collect weather data from a website, scrape it with
    # BeautifulSoup, and add that data as a calendar event
    weather_url = "https://www.yr.no/en/details/table/2-3361025/Republic%20of%20South%20Africa/Western%20Cape/Cape%20Winelands%20District%20Municipality/Stellenbosch"
    res = requests.get(weather_url)
    if res.ok:
        # Try-except the whole thing so the calendars don't fail just because
        # a website is down
        try:
            soup = BeautifulSoup(res.text, 'html.parser')
            selector = 'div.hourly-weather-table:nth-child(2) > div:nth-child(1) > div:nth-child(3) > table:nth-child(1) > tbody:nth-child(3) > tr:nth-child(1) > td:nth-child(7) > span:nth-child(1) > span:nth-child(1)'
            txt = soup.select_one(selector)
            events.append({
                "title": f"{txt.text}hPa in Stellenbosch",
                "description": f"Data from {weather_url}",
                "start": str(datetime.now().date()),
                "end": str(datetime.now().date()),
            })
        except Exception as e:
            print(f"Failed to get weather events: {e}")

    # Create a directory to contain our calendars
    print("Creating directory `calendars/`")
    os.makedirs("calendars", exist_ok=True)

    # Write the events list as yaml files into the calendars directory
    print(f"Writing events to `calendars/simple-calendar.yaml`:\n{events}")
    with open('calendars/simple-calendar.yaml', 'w') as file:
        yaml.dump({"events": events}, file)

    print(f"Python script finished")

if __name__ == "__main__":
    main()
