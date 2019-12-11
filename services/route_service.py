from models.route_model import Route
from datetime import time

def parse_waypoints(google_response):
    # TODO
    return "waypoints go here"

def create_route(my_account, form_data):
    route_data = {}

    route_data["phone"] = my_account.phone
    route_data["active"] = True
    #TODO assign start/end locations to google response objects
    route_data["start_location"] = form_data["start_location"]
    route_data["start_location_type"] = form_data["start_location_type"]
    route_data["end_location"] = form_data["end_location"]
    route_data["end_location_type"] = form_data["end_location_type"]
    route_data["waypoints"] = parse_waypoints(form_data["google_response"])
    run_hour = int(form_data["local_run_time"][:2])
    run_minute = int(form_data["local_run_time"][3:])
    run_timezone_offset = int(form_data["local_timezone_offset"])
    route_data["local_run_time"] = time(run_hour, run_minute)
    route_data["local_timezone_offset"] = run_timezone_offset
    route_data["run_time"] = time(run_hour - run_timezone_offset, run_minute)
    route_data["delay_tolerance"] = form_data["delay_tolerance"]
    route_data["run_sunday"] = True if form_data.get("Sunday") else False
    route_data["run_monday"] = True if form_data.get("Monday") else False
    route_data["run_tuesday"] = True if form_data.get("Tuesday") else False
    route_data["run_wednesday"] = True if form_data.get("Wednesday") else False
    route_data["run_thursday"] = True if form_data.get("Thursday") else False
    route_data["run_friday"] = True if form_data.get("Friday") else False
    route_data["run_saturday"] = True if form_data.get("Saturday") else False

    new_route = Route(route_data)
    new_route.save()
    return "successssssss"
    