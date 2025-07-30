#!/usr/bin/env python

import argparse
import json
import sys

import requests

noaa_url = "https://api.weather.gov"


def parse_args(args):
    parser = argparse.ArgumentParser(
        prog="noaapi",
        description="API Wrapper to get Weather Data",
    )
    parser.add_argument("subject", choices=["alerts", "stations", "zones"])
    parser.add_argument("-t", "--target", type=str, required=True)
    parser.add_argument("-p", "--proxy-server", type=str, required=False, default=noaa_url)

    return parser.parse_args(args)


def endpoint_to_json(endpoint, fileloc, baseurl):
    response = requests.get(f"{baseurl}/{endpoint}")
    if not response.ok:
        print(f"Problem with endpoint: {endpoint}")
    else:
        with open(f"{fileloc}/{endpoint.replace('/', '.')}.json", "w") as W:
            W.write(json.dumps(response.json(), indent="    "))


def main(args):
    args = parse_args(args)
    endpoint_to_json(args.subject, args.target, args.proxy_server)


"""
def paginated_endpoint(endpoint,pagenum=0,pageurl=None):
    if pageurl:
        response = requests.get(pageurl)
    else:
        response = requests.get(f"{baseurl}/{endpoint}")

    if not response.ok:
        print(f"Problem with endpoint: {endpoint}")
        return None
    resp = response.json()
    with open(f"{endpoint.replace('/','.')}_{pagenum}.json",'w') as W:
"""


"""
alerts = requests.get(f"{baseurl}/alerts/active/count"}
#alerts = requests.get(f"{baseurl}/alerts/active/zone/{zone}"}

stations = requests.get(f"{baseurl}/stations"} # Gets paginated list of stations
stations.json()['pagination']['next']

zones = requests.get(f"{baseurl}/zones"} # Gets paginated list of stations
zones = zones.json()['features']
glossary = requests.get(f"{baseurl}/glossary"} # Gets paginated list of stations
zone_id = zones[1]['properties']['id']
"""


def run():
    main(sys.argv[1:])


if __name__ == "__main__":
    run()

# Get observations by station or by zone
# /stations/{stationId}/observations/latest
# /stations/stationId}/observations/{time}
# zones/forecast/{zoneid}/observations
