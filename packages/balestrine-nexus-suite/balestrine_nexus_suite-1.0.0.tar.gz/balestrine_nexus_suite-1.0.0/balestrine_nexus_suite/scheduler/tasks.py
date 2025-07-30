from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
def job(): print('Job ran')
def start(): scheduler.add_job(job, 'interval', seconds=60); scheduler.start()
