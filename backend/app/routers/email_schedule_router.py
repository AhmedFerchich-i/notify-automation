from datetime import datetime, timedelta
from typing import Optional

from strategies.email_scheduling_stategies import EtaScheduler,CacheScheduler,DeferScheduler,SchedulerStrategy

class ScheduleRouter:
    def __init__(self):
        self.eta_scheduler = EtaScheduler()
        self.cache_scheduler = CacheScheduler()
        self.defer_scheduler = DeferScheduler()

    def schedule(self, email_id: int, scheduled_time: datetime) :
        now = datetime.utcnow()
        diff = scheduled_time - now

        if diff <= timedelta(hours=3):
            # Use ETA countdown task for emails within 3 hours
            strategy: SchedulerStrategy = self.eta_scheduler
        elif diff <= timedelta(hours=6):
            # Use cache-based scheduling for emails between 3 to 6 hours
            strategy = self.cache_scheduler
        else:
            # Defer scheduling for emails more than 6 hours away
            strategy = self.defer_scheduler

        return strategy.schedule(email_id, scheduled_time)
