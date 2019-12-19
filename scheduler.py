# This automatic job scheduler checks in the db every 15 min. 
# If it finds an active job within a 35 min horizon, it attempts
# to add it to the job scheduler. It disregards any duplicate jobs.

from datetime import datetime, timedelta
import time
import sys
import os
DATABASE_URL = os.getenv('DATABASE_URL')
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import commute_check

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Route(Base):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    phone = Column(String)
    start_location = Column(String)
    start_location_type = Column(String)
    end_location =  Column(String)
    end_location_type = Column(String)
    waypoints = Column(String)
    local_run_time = Column(Time)
    local_timezone_offset = Column(Integer)
    run_time = Column(Time)
    delay_tolerance = Column(Integer)
    run_sunday = Column(Boolean)
    run_monday = Column(Boolean)
    run_tuesday = Column(Boolean)
    run_wednesday = Column(Boolean)
    run_thursday = Column(Boolean)
    run_friday = Column(Boolean)
    run_saturday = Column(Boolean)

    def __repr__(self):
        return f'Route: {self.id} \nFor: {self.phone} \nFrom: {self.start_location} \nTo: {self.end_location}'


def scan_for_jobs():
    print('\nSCANNING FOR JOBS TO ADD TO THE SCHEDULER', f'({datetime.utcnow().replace(microsecond=0)} UTC)')
    routes_reviewed = 0
    routes_added_to_scheduler = 0
    my_session = Session()

    for route in my_session.query(Route):
        routes_reviewed += 1

        # Check if the route already exists in the job queue
        if str(route.id) in [job.id for job in scheduler.get_jobs()]:
            continue

        # Check if route is set to Active
        if not route.active:
            continue

        # Check if route has disabled service for all days of the week
        if not route.run_monday and not route.run_tuesday and not \
            route.run_wednesday and not route.run_thursday and not \
                route.run_friday and not route.run_saturday and not \
                    route.run_sunday:
                    continue

        # Find the next local datetime that route will need to fire
        utc_now = datetime.utcnow()
        local_now = utc_now + timedelta(hours=route.local_timezone_offset)
        run_on_which_weekdays = {
            0: route.run_monday,
            1: route.run_tuesday,
            2: route.run_wednesday,
            3: route.run_thursday,
            4: route.run_friday,
            5: route.run_saturday,
            6: route.run_sunday
        }
        check_this_weekday = local_now.weekday()
        for i in range(7):
            if run_on_which_weekdays[check_this_weekday]:
                next_local_run_datetime = local_now.replace(hour=route.local_run_time.hour, minute=route.local_run_time.minute, second=0, microsecond=0)
                next_local_run_datetime += timedelta(days=i)
                if next_local_run_datetime > local_now:
                    break
            check_this_weekday += 1 if check_this_weekday <=5 else -6

        # Check if the next run time is within the horizon for adding to the job scheduler
        local_horizon = local_now + timedelta(minutes=35)
        next_utc_run_datetime = next_local_run_datetime - timedelta(hours=route.local_timezone_offset)
        if local_now < next_local_run_datetime and next_local_run_datetime < local_horizon:
            # Add job to queue, in UTC datetime
            # next_local_run_datetime2 = datetime.now() + timedelta(seconds=30)  # Line for testing only
            new_job = scheduler.add_job(alarm, 'date', run_date=next_utc_run_datetime, args=[route], id=str(route.id))
            routes_added_to_scheduler += 1
            print(f'Added Route: {route.id} Run date UTC: {next_utc_run_datetime}')

    print('CURRENTLY SCHEDULED JOBS')
    print([f'Route:{job.id} at {job.next_run_time}' for job in scheduler.get_jobs()])
    return routes_reviewed, routes_added_to_scheduler


def alarm(route):
    if True:
        response = commute_check.run_route(route)
        print('\n', response)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.start()
    print('Press Ctrl+{0} to exit\n'.format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            routes_reviewed, routes_added_to_scheduler = scan_for_jobs()
            utc_now = datetime.utcnow()
            print('JOB SCAN COMPLETE', f'({datetime.utcnow().replace(microsecond=0)} UTC)')
            print(f'Added {routes_added_to_scheduler} jobs to the queue, reviewed {routes_reviewed} total.')
            time.sleep(60*15)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()    