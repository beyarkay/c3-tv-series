from datetime import datetime, timedelta
import yaml
import os
import requests
from bs4 import BeautifulSoup


def main():

    # Attempt to collect weather data from a website, scrape it with
    # BeautifulSoup, and add that data as a calendar event

    events = []
    url = "https://www.rottentomatoes.com/tv/the_last_of_us/s01"
    res = requests.get(url)
    if res.ok:
        # Try-except the whole thing so the calendars don't fail just because
        # a website is down
        try:
            soup = BeautifulSoup(res.text, "html.parser")
            episode_selector = ".episodeItem-body"
            for episode in soup.select(episode_selector):
                air_date_selector = ".col-sm-6"
                air_date = (
                    episode.select(air_date_selector)[0]
                    .text.replace("Air date:", "")
                    .strip()
                )
                air_date = datetime.strptime(air_date, "%b %d, %Y")
                title_selector = ".episodelink-title"
                title = episode.select(title_selector)[0].text.strip()
                desc_selector = ".synopsis"
                desc = episode.select(desc_selector)[0].text.strip()
                events.append(
                    {
                        "title": f"tLoU: {title}",
                        "description": f"{desc}",
                        "start": str(air_date),
                        "end": str(air_date),
                    }
                )

        except Exception as e:
            print(f"Failed to get TV Series events: {e}")

    # Create a directory to contain our calendars
    print("Creating directory `calendars/`")
    os.makedirs("calendars", exist_ok=True)

    # Write the events list as yaml files into the calendars directory
    calendar_name = "the-last-of-us"
    print(f"Writing events to `calendars/{calendar_name}.yaml`")
    with open(f"calendars/{calendar_name}.yaml", "w") as file:
        yaml.dump({"events": events}, file)

    print(f"Python script finished")


if __name__ == "__main__":
    main()
