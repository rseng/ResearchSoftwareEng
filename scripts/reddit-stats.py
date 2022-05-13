# Count members of ResearchSoftwareEng reddit
# Copyright @vsoch, 2022

import os
import sys
import requests
import random
import yaml
import datetime

here = os.path.dirname(os.path.abspath(__file__))


def read_file(filepath):
    """
    read in the jobs data.
    """
    with open(filepath, "r") as fd:
        data = yaml.load(fd.read(), Loader=yaml.SafeLoader)
    return data


def get_user_agent() -> str:
    """
    Return a randomly chosen user agent for requests
    Returns:
        user agent string to include with User-Agent.
    """
    agents = [
        (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/57.0.2987.110 "
            "Safari/537.36"
        ),  # chrome
        (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/61.0.3163.79 "
            "Safari/537.36"
        ),  # chrome
        (
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) "
            "Gecko/20100101 "
            "Firefox/55.0"
        ),  # firefox
        (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/61.0.3163.91 "
            "Safari/537.36"
        ),  # chrome
        (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/62.0.3202.89 "
            "Safari/537.36"
        ),  # chrome
        (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/63.0.3239.108 "
            "Safari/537.36"
        ),  # chrome
    ]
    return random.choice(agents)


def main():

    user_agent = get_user_agent()
    headers = {"User-Agent": user_agent}

    # Read the community name from file
    name_file = os.path.join(os.path.dirname(here), "COMMUNITY_NAME")
    with open(name_file, 'r') as fd:
        name = fd.read().strip()

    print("Community name is %s" % name)

    # First update the current data file
    response = requests.get(
        "https://www.reddit.com/r/%s/about.json" % name, headers=headers
    )
    if response.status_code != 200:
        sys.exit("Issue retrieving stats endpoint: %s" % response.reason)

    data = response.json()

    # Save latest raw data to file
    stats_file = os.path.join(os.path.dirname(here), "_data", "stats.yaml")
    with open(stats_file, "w") as outfile:
        yaml.dump(data, outfile)
    counts_file = os.path.join(os.path.dirname(here), "_data", "counts.yaml")

    # Index based on today's date
    now = datetime.date.today()

    # Update counts!
    counts = read_file(counts_file)
    counts["subscribers"][str(now)] = data['data']["subscribers"]
    with open(counts_file, "w") as outfile:
        yaml.dump(counts, outfile)


if __name__ == "__main__":
    main()
