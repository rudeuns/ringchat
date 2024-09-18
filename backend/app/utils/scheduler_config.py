from apscheduler.schedulers.background import BackgroundScheduler

from app.utils.vector_operations import batch_insert_vector

scheduler = BackgroundScheduler()


def start_scheduler():
    scheduler.add_job(batch_insert_vector, "interval", minutes=1)
    scheduler.start()


def stop_scheduler():
    scheduler.shutdown()
