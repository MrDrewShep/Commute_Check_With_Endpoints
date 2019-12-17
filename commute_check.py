
import requests
import pprint
import datetime
import time
import csv
import os
import send_sms
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
AMAZON_API_KEY = os.getenv('AMAZON_API_KEY')


#TODO Make the program capable of handling when "duration_in_traffic" is unavailable and only "duration" is available


def unpack_route_from_db(route):
    """Opens the route details from the PostgreSQL db."""

    #TODO change out these hardcoded values for values from the db
    # start_location = "151 W Ohio St, Indianapolis, IN 46204, USA".replace(' ', '+').replace(',', '')
    # end_location = "5325 Metoyer Ct, Plainfield, IN 46168, USA".replace(' ', '+').replace(',', '')
    # delay_tolerance = "3"
    # waypoints = "via:39.769999%2C-86.161605%7Cvia:39.7671321%2C-86.161717%7Cvia:39.7566020%2C-86.162132%7Cvia:39.6702869%2C-86.365237%7Cvia:39.6699482%2C-86.370688%7Cvia:39.6749122%2C-86.370980%7Cvia:39.6746236%2C-86.389323%7Cvia:39.6745572%2C-86.390419%7Cvia:39.6744236%2C-86.398685%7Cvia:39.6743044%2C-86.418279%7Cvia:39.6833243%2C-86.418404%7Cvia:39.6834125%2C-86.420359%7Cvia:39.6839588%2C-86.420538%7Cvia:39.6846948%2C-86.428165%7Cvia:39.6870287%2C-86.430225%7Cvia:39.6882133%2C-86.430473%7Cvia:39.6881996%2C-86.431335"
    # phone = "3175142678"

    # start_location = "332 N ave 59 los angeles, ca 90042"
    # end_location = "los angeles international airport"
    # waypoints = "via:34.160454%2C-118.467785"
    
    my_route = {
        "start_location": route.start_location,
        "end_location": route.end_location,
        "delay_tolerance": int(route.delay_tolerance),
        "waypoints": route.waypoints,
        "phone": route.phone
    }
    return my_route


def setup_api_requests_data(my_route):
    my_route["api_requests"] = []

    preferred = {
        "request_type": "preferred",
        "api_url": build_api_url(my_route, "preferred"),
        "api_response": None
    }

    best_available = {
        "request_type": "best_available",
        "api_url": build_api_url(my_route, "best_available"),
        "api_response": None
    }

    my_route["api_requests"].append(preferred)
    my_route["api_requests"].append(best_available)

    return my_route


def build_api_url(my_route, route_request_type):
    """Builds the respective URLs, per user, to send to Google and compare responses.""" 

    url_base_characteristics = [
    {
        "parameter": "",
        "argument": "https://maps.googleapis.com/maps/api/directions/json?"
    },
    {
        "parameter": "origin",
        "argument": my_route["start_location"]
    },
    {
        "parameter": "destination",
        "argument": my_route["end_location"]
    },
    {
        "parameter": "key",
        "argument": GOOGLE_MAPS_API_KEY
    },
    {
        "parameter": "alternatives",    # Only works without intermediate waypoints
        "argument": "false"
    },
    {
        "parameter": "mode",
        "argument": "driving"
    },
    {
        "parameter": "departure_time",
        "argument": "now"
    },
    {
        "parameter": "waypoints",
        "argument": my_route["waypoints"] if route_request_type == "preferred" else ""
    }
]

    url = ""
    for item in url_base_characteristics:
        if item["parameter"] == "":
            url += item["argument"]
        else:
            url += f'&{item["parameter"]}={item["argument"]}'
    
    return url


def make_api_calls(my_route):
    for request in my_route["api_requests"]:
        response = requests.get(request["api_url"])
        request["api_response"] = response.json()

    return my_route


def parse_api_responses(my_route):
    """Take each Google API JSON response and parse the response for data."""

    print(my_route["phone"])
    for request in my_route["api_requests"]:
        total_distance = 0
        sum_duration = 0
        sum_duration_w_traffic = 0
        print(f'Route: {request["request_type"]}, {request["api_response"]["routes"][0]["summary"]}')
        i = 1
        legnum = 1
        rte_index = 0

        for leg in request["api_response"]["routes"][rte_index]["legs"]:
            # pprint.pprint(leg)
            # quit()
            sum_duration_w_traffic += int(leg["duration_in_traffic"]["value"])  #duration_in_traffic to duration
            for step in leg["steps"]:
                i += 1
                total_distance += int(step["distance"]["value"])
                sum_duration += int(step["duration"]["value"])
            legnum += 1

        # Convert cumluative seconds into string of x hrs y min
        duration = convert_secs_to_hr_min_string(sum_duration)
        duration_w_traffic = convert_secs_to_hr_min_string(sum_duration_w_traffic)
        request["duration"] = sum_duration
        request["duration_str"] = duration
        request["duration_w_traffic"] = sum_duration_w_traffic
        request["duration_w_traffic_str"] = duration_w_traffic
        print(f"Total: {round(total_distance/1607, 1)} mi, {duration}, {duration_w_traffic} with traffic")
    
    return my_route


def convert_secs_to_hr_min_string(seconds):
    """Google converses in seconds, for departure time and duration of routes. This converts it to a readable format of hours/minutes."""

    duration_string = ""

    duration_hrs = int((seconds/60) // 60)
    duration_minutes = int((seconds/60) % 60)

    if duration_hrs > 0:
        duration_string += f'{duration_hrs}'
        if duration_hrs == 1:
            duration_string += " hr "
        else:
            duration_string += " hrs "
    duration_string += f'{duration_minutes} min'

    return duration_string


def evaluate_optimal_route(my_route):
    phone = "+1" + my_route["phone"]
    tolerance_seconds = 60 * my_route["delay_tolerance"]

    for request_type in my_route["api_requests"]:
        if request_type["request_type"] == "preferred":
            preferred_duration_w_traffic = request_type["duration_w_traffic"]
        elif request_type["request_type"] == "best_available":
            best_avail_duration_w_traffic = request_type["duration_w_traffic"]

    delta = preferred_duration_w_traffic - best_avail_duration_w_traffic

    if delta > tolerance_seconds:
        suggest_alt_route(preferred_duration_w_traffic, best_avail_duration_w_traffic, delta, phone)
    else:
        suggest_preferred_route(preferred_duration_w_traffic, best_avail_duration_w_traffic, delta, phone, tolerance_seconds)

    return my_route


def suggest_alt_route(preferred_duration_w_traffic, best_avail_duration_w_traffic, delta, phone):
    """Sends an SMS suggesting the user take an alternate route."""

    preferred = convert_secs_to_hr_min_string(preferred_duration_w_traffic)
    best = convert_secs_to_hr_min_string(best_avail_duration_w_traffic)
    delta = convert_secs_to_hr_min_string(delta)

    text_body = f'Save {delta}, your usual route is {preferred} and a {best} alternative exists.'
    print(text_body)
    send_sms.send_sms(phone, text_body)


def suggest_preferred_route(preferred_duration_w_traffic, best_avail_duration_w_traffic, delta, phone, tolerance_seconds):
    """Sends an SMS suggesting the user take their usual route. Note: This is for testing purposes. Eventually the suggestion of a user's "usual" route would be indicated by a non-notificaiton."""

    preferred = convert_secs_to_hr_min_string(preferred_duration_w_traffic)
    best = convert_secs_to_hr_min_string(best_avail_duration_w_traffic)
    delta = convert_secs_to_hr_min_string(delta)
    tolerance = convert_secs_to_hr_min_string(tolerance_seconds)

    text_body = f'Stick to your usual route, at {preferred}. The best route available is {best}. Your threshold for an alternative is {tolerance}.'
    print(text_body)
    send_sms.send_sms(phone, text_body)


def run_route(route):
    my_route = unpack_route_from_db(route)
    my_route = setup_api_requests_data(my_route)
    my_route = make_api_calls(my_route)
    my_route = parse_api_responses(my_route)
    my_route = evaluate_optimal_route(my_route)

# run_route(route)