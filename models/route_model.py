from datetime import datetime
from . import db

from marshmallow import Schema, fields

class Route(db.Model):
    __tablename__ = "routes"
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), db.ForeignKey("accounts.phone"))
    start_location = db.Column(db.String(100), nullable=False)
    start_location_type = db.Column(db.String(20), nullable=False)
    end_location = db.Column(db.String(100), nullable=False)
    end_location_type = db.Column(db.String(20), nullable=False)
    run_time = db.Column(db.Time, nullable=False)
    local_run_time = db.Column(db.Time, nullable=False)
    local_timezone_offset = db.Column(db.Integer, nullable=False)
    delay_tolerance = db.Column(db.Integer, nullable=False)
    run_sunday = db.Column(db.Boolean, nullable=False)
    run_monday = db.Column(db.Boolean, nullable=False)
    run_tuesday = db.Column(db.Boolean, nullable=False)
    run_wednesday = db.Column(db.Boolean, nullable=False)
    run_thursday = db.Column(db.Boolean, nullable=False)
    run_friday = db.Column(db.Boolean, nullable=False)
    run_saturday = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)

    route_data = {
        "phone": phone,
        "start_location": start_location,
        "start_location_type": start_location_type,
        "end_location": end_location,
        "end_location_type": end_location_type,
        "run_time": run_time,
        "local_run_time": local_run_time,
        "local_timezone_offset": local_timezone_offset,
        "delay_tolerance": delay_tolerance,
        "run_sunday": run_sunday,
        "run_monday": run_monday,
        "run_tuesday": run_tuesday,
        "run_wednesday": run_wednesday,
        "run_thursday": run_thursday,
        "run_friday": run_friday,
        "run_saturday": run_saturday
    }

    def __init__(self, route_data):
        self.phone = route_data["phone"]
        self.start_location = route_data["start_location"]
        self.start_location_type = route_data["start_location_type"]
        self.end_location = route_data["end_location"]
        self.end_location_type = route_data["end_location_type"]
        self.run_time = route_data["run_time"]
        self.local_run_time = route_data["local_run_time"]
        self.local_timezone_offset = route_data["local_timezone_offset"]
        self.delay_tolerance = route_data["delay_tolerance"]
        self.run_sunday = route_data["run_sunday"]
        self.run_monday = route_data["run_monday"]
        self.run_tuesday = route_data["run_tuesday"]
        self.run_wednesday = route_data["run_wednesday"]
        self.run_thursday = route_data["run_thursday"]
        self.run_friday = route_data["run_friday"]
        self.run_saturday = route_data["run_saturday"]
        now = datetime.utcnow()
        self.created_at = now
        self.last_modified = now

    # TODO def save/update

    # TODO def delete

    @staticmethod
    def get_route(route_id):
        return Route.query.filter_by(id=route_id).first()

    @staticmethod
    def get_all_routes(phone):
        return Route.query.filter_by(phone=phone)
    
    # TODO do we need get_route_owner

class RouteSchema(Schema):
    id = fields.Int(dump_only=True)
    phone = fields.Int(dump_only=True)
    start_location = fields.Str(dump_only=True)
    start_location_type = fields.Str(dump_only=True)
    end_location = fields.Str(dump_only=True)
    end_location_type = fields.Str(dump_only=True)
    run_time = fields.Time(dump_only=True)
    local_run_time = fields.Time(dump_only=True)
    local_timezone_offset = fields.Int(dump_only=True)
    delay_tolerance = fields.Int(dump_only=True)
    run_sunday = fields.Bool(dump_only=True)
    run_monday = fields.Bool(dump_only=True)
    run_tuesday = fields.Bool(dump_only=True)
    run_wednesday = fields.Bool(dump_only=True)
    run_thursday = fields.Bool(dump_only=True)
    run_friday = fields.Bool(dump_only=True)
    run_saturday = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    last_modified = fields.DateTime(dump_only=True)