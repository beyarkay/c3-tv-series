from datetime import datetime, timedelta
import yaml
import os
import requests
from bs4 import BeautifulSoup


def main():

    shows = {
        "The Good Doctor": "https://www.rottentomatoes.com/tv/the_good_doctor",
        "The Last of Us": "https://www.rottentomatoes.com/tv/the_last_of_us",
        "The White Lotus": "https://www.rottentomatoes.com/tv/the_white_lotus",
        "Yellowjackets": "https://www.rottentomatoes.com/tv/yellowjackets",
        "House of the Dragon": "https://www.rottentomatoes.com/tv/house_of_the_dragon",
        "Fleabag": "https://www.rottentomatoes.com/tv/fleabag",
        "Stranger Things": "https://www.rottentomatoes.com/tv/stranger_things",
        "Sherlock": "https://www.rottentomatoes.com/tv/sherlock",
        "The Boys": "https://www.rottentomatoes.com/tv/the_boys_2019",
        "Invincible": "https://www.rottentomatoes.com/tv/invincible",
        "Arcane": "https://www.rottentomatoes.com/tv/arcane_league_of_legends",
        "Utopia": "https://www.rottentomatoes.com/tv/utopia_2013",
        "Electric Dreams": "https://www.rottentomatoes.com/tv/philip_k_dick_s_electric_dreams",
        "Foundation": "https://www.rottentomatoes.com/tv/foundation",
        "Money Heist": "https://www.rottentomatoes.com/tv/money_heist",
        "Doctor Who": "https://www.rottentomatoes.com/tv/doctor_who",
        "The Expanse": "https://www.rottentomatoes.com/tv/the_expanse",
        "The Good Place": "https://www.rottentomatoes.com/tv/good_place",
        "Peaky Blinders": "https://www.rottentomatoes.com/tv/peaky_blinders",
        "Schitts Creek": "https://www.rottentomatoes.com/tv/schitts_creek",
        "Silicon Valley": "https://www.rottentomatoes.com/tv/silicon_valley",
        "Black Mirror": "https://www.rottentomatoes.com/tv/black_mirror",
        "Westworld": "https://www.rottentomatoes.com/tv/westworld",
        "Love, Death, + Robots": "https://www.rottentomatoes.com/tv/love_death_robots",
        "Rick and Morty": "https://www.rottentomatoes.com/tv/rick_and_morty",
    }

    for show, url in shows.items():
        print(f"Processing show {show}")
        events = []
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        season_selector = "season-list-item"
        seasons = [
            l
            for l in soup.select("div.panel-body>a")
            if l.get("data-qa") == "season-link"
        ]
        season_urls = [
            f'https://www.rottentomatoes.com{season.get("href")}' for season in seasons
        ]
        for season_url in season_urls:
            print(f"  Processing season {season_url.split('/')[-1]}")
            if len(show.split(" ")) == 1:
                short_name = show
            else:
                short_name = "".join(
                    w[0] for w in show.replace("The", "the").split(" ")
                )
            short_season = season_urls[0].split("/")[-1]
            season_events = get_season_data(
                season_url,
                f"{short_name} {short_season}",
            )
            # print(f"  Found {len(season_events)} events")
            events.extend(season_events)

        print(f"Writing {len(events)} events to {show}")
        events_to_disk(events, show.replace(" ", "-").lower())

    print(f"Python script finished")


def events_to_disk(events, calendar_name):
    # Create a directory to contain our calendars
    # print("Creating directory `calendars/`")
    os.makedirs("calendars", exist_ok=True)

    # Write the events list as yaml files into the calendars directory
    # print(f"Writing events to `calendars/{calendar_name}.yaml`")
    with open(f"calendars/{calendar_name}.yaml", "w") as file:
        yaml.dump({"events": events}, file)


def get_season_data(url, short_title):
    events = []
    res = requests.get(url)
    if res.ok:
        # Try-except the whole thing so the calendars don't fail just because
        # a website is down
        try:
            soup = BeautifulSoup(res.text, "html.parser")
            episode_selector = "#desktopEpisodeList .episodeItem-body"
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
                        "title": f"{short_title}: {title}",
                        "description": f"{desc}",
                        "start": str(air_date)[:-9],
                        "end": str(air_date)[:-9],
                    }
                )

        except Exception as e:
            print(f"Failed to get TV Series events: {e}")
    else:
        print(
            f"Warning, result for {url} returned status code != 2XX: {res.status_code}"
        )
    return events


if __name__ == "__main__":
    main()
