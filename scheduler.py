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
    my_session = Session()
    active_routes = []
    for instance in my_session.query(Route):
        if instance.active:
            active_routes.append(instance)
    
    jobs_added_to_queue = 0
    jobs_reviewed = 0
    now = datetime.utcnow()
    horizon = now + timedelta(minutes=600)
    for route in active_routes:
        jobs_reviewed += 1
        # TODO if we have already passed the run time, then run time is the next run time
        # TODO Check if job already exists in job scheduler queue
        # TODO Check if day of week is correct
        run_date = datetime(2019, 12, 17, route.run_time.hour, route.run_time.minute, route.run_time.second)
        if now < run_date and run_date < horizon:
            run_date2 = datetime.now() + timedelta(seconds=2)
            scheduler.add_job(alarm, 'date', run_date=run_date, args=[route])
            jobs_added_to_queue += 1
            # print(f'Added {route.id} Run date {run_date} Horizon {horizon}')
        else:
            # print(f'Not added {route.id} Run date {run_date} Horizon {horizon}')
            pass
    return jobs_reviewed, jobs_added_to_queue


def alarm(route):
    if True:
        print(commute_check.run_route(route))


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.start()
    print('Press Ctrl+{0} to exit\n'.format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            # scheduler.print_jobs()
            jobs_reviewed, jobs_added_to_queue = scan_for_jobs()
            now = datetime.utcnow()
            print(f'Added {jobs_added_to_queue} jobs to the queue, reviewed {jobs_reviewed} total. ({now})')
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()    