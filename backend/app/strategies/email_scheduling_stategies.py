from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any
from celery_config.celery_worker import celery_app
class SchedulerStrategy(ABC):
    @abstractmethod
    def schedule(self, email_id: int, scheduled_time: datetime) -> Any:
        """Schedule an email for sending at the given time."""
        pass

from tasks.send_email_bulk import send_bulk_emails_task
class EtaScheduler(SchedulerStrategy):
    def schedule(self, email_id: int, scheduled_time: datetime):
        print(f"[ETA] Scheduling email {email_id} at {scheduled_time}")
        # Celery ETA logic will go here

class CacheScheduler(SchedulerStrategy):
    def schedule(self, email_id: int, scheduled_time: datetime):
        print(f"[CACHE] Adding email {email_id} to Redis for {scheduled_time}")
        # Redis sorted set logic will go here

class DeferScheduler(SchedulerStrategy):
    def schedule(self, email_id: int, scheduled_time: datetime):
        print(f"[DEFER] Deferring email {email_id} until closer to {scheduled_time}")
        # Database deferral logic will go here