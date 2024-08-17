from celery import shared_task
from .models import Job

@shared_task
def process_job(job_id):
    job = Job.objects.get(id=job_id)
    job.status = 'in_progress'
    job.save()

    try:
        # Simulate processing
        result = "Job processed successfully!"
        job.status = 'completed'
        job.result = result
    except Exception as e:
        job.status = 'failed'
        job.result = str(e)
    
    job.save()
