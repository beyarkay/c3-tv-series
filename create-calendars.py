from datetime import datetime, timedelta
import yaml
import os
import requests
from bs4 import BeautifulSoup


def main():
    shows = {
        "Arcane": "https://www.rottentomatoes.com/tv/arcane_league_of_legends",
        "Black Mirror": "https://www.rottentomatoes.com/tv/black_mirror",
        "Doctor Who": "https://www.rottentomatoes.com/tv/doctor_who",
        "Electric Dreams": "https://www.rottentomatoes.com/tv/philip_k_dick_s_electric_dreams",
        "Fleabag": "https://www.rottentomatoes.com/tv/fleabag",
        "Foundation": "https://www.rottentomatoes.com/tv/foundation",
        "House of the Dragon": "https://www.rottentomatoes.com/tv/house_of_the_dragon",
        "Inside Job": "https://www.rottentomatoes.com/tv/inside_job_2021",
        "Invincible": "https://www.rottentomatoes.com/tv/invincible",
        "Love Death and Robots": "https://www.rottentomatoes.com/tv/love_death_robots",
        "Money Heist": "https://www.rottentomatoes.com/tv/money_heist",
        "Peaky Blinders": "https://www.rottentomatoes.com/tv/peaky_blinders",
        "Rick and Morty": "https://www.rottentomatoes.com/tv/rick_and_morty",
        "Schitts Creek": "https://www.rottentomatoes.com/tv/schitts_creek",
        "Severance": "https://www.rottentomatoes.com/tv/severance",
        "Sex Education": "https://www.rottentomatoes.com/tv/sex_education",
        "Sherlock": "https://www.rottentomatoes.com/tv/sherlock",
        "Silicon Valley": "https://www.rottentomatoes.com/tv/silicon_valley",
        "Stranger Things": "https://www.rottentomatoes.com/tv/stranger_things",
        "The Boys": "https://www.rottentomatoes.com/tv/the_boys_2019",
        "The Expanse": "https://www.rottentomatoes.com/tv/the_expanse",
        "The Good Doctor": "https://www.rottentomatoes.com/tv/the_good_doctor",
        "The Good Place": "https://www.rottentomatoes.com/tv/good_place",
        "The Last of Us": "https://www.rottentomatoes.com/tv/the_last_of_us",
        "The White Lotus": "https://www.rottentomatoes.com/tv/the_white_lotus",
        "Utopia": "https://www.rottentomatoes.com/tv/utopia_2013",
        "Westworld": "https://www.rottentomatoes.com/tv/westworld",
        "Yellowjackets": "https://www.rottentomatoes.com/tv/yellowjackets",
    }

    for show, url in shows.items():
        events = []
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        seasons = [
            link for link in soup.select("a") if link.get("data-qa") == "season-link"
        ]
        season_urls = sorted(
            [
                f'https://www.rottentomatoes.com{season.get("href")}'
                for season in seasons
            ]
        )
        print(f"Processing {len(season_urls)} seasons of [{show}]({url})")
        for season_url in season_urls:
            print(f"  Processing season {season_url.split('/')[-1]} ({season_url})")
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
            print(f"  -> {len(season_events)} events")
            events.extend(season_events)

        print(f"-> Writing {len(events)} events to {show}")
        events_to_disk(events, show.replace(" ", "-").lower())

    print("Python script finished")


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
            episode_selector = "li.episodes-list-item>div.episode-wrap"
            episodes = soup.select(episode_selector)
            for episode in episodes:
                # print("    Processing episode")
                air_dates = [
                    ad
                    for ad in episode.select("p")
                    if ad.get("data-qa") == "episode-air-date"
                ]
                air_date = air_dates[0].text.replace("Air date:", "").strip()
                air_date = datetime.strptime(air_date, "%b %d, %Y")

                titles = [
                    t
                    for t in episode.select("a")
                    if t.get("data-qa") == "episode-title"
                ]
                title = titles[0].text.strip()
                episode_url = url + "/" + titles[0].get("href").split("/")[-1]

                descs = [
                    d
                    for d in episode.select("p")
                    if d.get("data-qa") == "episode-synopsis"
                ]
                desc = descs[0].text.strip()
                events.append(
                    {
                        "title": f"{short_title}: {title}",
                        "description": f"{desc}\n---\n{episode_url}",
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
