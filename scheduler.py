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
    for route in active_routes:
        run_date = datetime.now() + timedelta(seconds=4)
        scheduler.add_job(alarm, 'date', run_date=run_date, args=[route])
        jobs_added_to_queue += 1
    return jobs_added_to_queue


def alarm(route):
    if True:
        commute_check.run_route(route)
        print(f'Route id {route.id} from {route.start_location} to {route.end_location} at {route.run_time}')


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            jobs_added_to_queue = scan_for_jobs()
            now = datetime.utcnow()
            print(f'Added {jobs_added_to_queue} jobs to the queue. ({now})')
            time.sleep(30)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()    