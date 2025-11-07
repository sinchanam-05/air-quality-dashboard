from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import timedelta
import logging

from .services.ingestion import run_ingestion_job
from .database import get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

def ingestion_job_wrapper():
    logger.info("Scheduler : Executing ingestion job wrapper...")

    try:
        with get_db() as db:
            run_ingestion_job(db)
    except Exception as e:
        logger.error(f"Scheduler: Fatal error during ingestion job: {e}", exc_info=True)


def start_ingestion_scheduler():
    trigger = IntervalTrigger(hours=3)
    
    # Add the job to the scheduler
    scheduler.add_job(
        ingestion_job_wrapper,
        trigger=trigger,
        id='periodic_ingestion',
        name='Periodic Air/Allergen Data Ingestion',
        replace_existing=True,
        # Start the job immediately upon scheduler start
        next_run_time=timedelta(seconds=5) 
    )
    
    # Start the scheduler background service
    if not scheduler.running:
        scheduler.start()
        logger.info("Scheduler: Periodic ingestion scheduler started.")
        logger.info(f"Scheduler: Job 'periodic_ingestion' configured to run every 3 hours.")
    else:
        logger.info("Scheduler: Already running.")

def stop_ingestion_scheduler():
    """
    Shuts down the scheduler gracefully.
    """
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler: Periodic ingestion scheduler shut down.")