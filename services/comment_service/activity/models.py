import uuid
from django.db import models


class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor_id = models.UUIDField()
    action = models.CharField(max_length=100)  # comment_created, user_mentioned, comment_updated
    object_type = models.CharField(max_length=50)
    object_id = models.UUIDField()
    comment_id = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Activity({self.action}) by {self.actor_id} on {self.object_type}:{self.object_id}"
