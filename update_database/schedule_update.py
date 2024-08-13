from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from update_database import update_database


def start():
    """
    Start jobs to update the database.
    In production:
        updateDatabase: 30 mins
        updateLocations: 2 mins

    In development: (the first time)
        updateDatabase: 1 mins
        updateLocations: 5 mins

    In development: after you already have some data in the database
        updateDatabase: 30 mins or disabled
        updateLocations: 10 mins or disabled
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_database.updateDatabase, 'interval', minutes=30)
    scheduler.add_job(update_database.updateLocations, 'interval', minutes=10)

    scheduler.start()

#   Scripts to populate some databases
#   find_all_projects: find all the project with xp in the 42cursus
#   scheduler.add_job(update_database.find_all_projects, 'interval', minutes=2)
