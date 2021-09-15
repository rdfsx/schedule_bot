import random

from app.loader import scheduler
from app.services.api_group import APIMethodsGroup


def schedule_jobs():
    group = APIMethodsGroup()
    minute = random.randint(8, 57)
    hour = random.randint(3, 5)
    scheduler.add_job(group.compare_all_groups, "cron", day_of_week='mon-sun', hour=hour, minute=minute)
