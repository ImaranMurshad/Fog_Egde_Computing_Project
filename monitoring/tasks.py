from celery import shared_task

from .models import Alert, FogHealth


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def save_alert_task(self, data):
    Alert.objects.create(**dict(data))


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def save_fog_health_task(self, data):
    FogHealth.objects.create(**dict(data))