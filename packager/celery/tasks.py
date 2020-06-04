from celery import shared_task


@shared_task
def my_packager_task(data=None):
    # This is a sample celery task
    pass
