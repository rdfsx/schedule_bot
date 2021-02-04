import random

from loader import scheduler, dp
from schedule_requests.api_group import APIMethodsGroup


def schedule_jobs():
    group = APIMethodsGroup()
    minute = random.randint(1, 58)
    hour = random.randint(3, 5)
    scheduler.add_job(group.compare_all_groups(), "cron", day_of_week='mon-sun', hour=hour, minute=minute, args=(dp,))
