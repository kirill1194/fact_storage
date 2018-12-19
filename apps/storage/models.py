from uuid import uuid4
from apps.handlers.messages import push_to_carrier
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db.utils import IntegrityError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

class Fact(models.Model):
    uuid = models.UUIDField(default=uuid4)
    hash = models.CharField(max_length=256, null=True, blank=True)
    actor = ArrayField(models.IntegerField())
    type = models.CharField(max_length=256)
    result = JSONField(default=dict)
    source = models.CharField(max_length=1024)
    handler = models.CharField(max_length=256)
    meta = JSONField(default=dict)
    description = models.CharField(max_length=1024, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

@receiver(post_save, sender=Fact)
def send_new_fact_to_carrier(instance: Fact, created, *args, **kwargs):
    if not created:
        return

    payload = {
        'id': {'fact': {'uuid': str(instance.uuid)}},
        'action': 'create',
        'title': '',
        'type': 'fact',
        'timestamp': now().isoformat(),
        'source': 'factstorage',
        'version': 1
    }

    push_to_carrier(topic="fs", payload=payload)