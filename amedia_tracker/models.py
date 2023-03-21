from django.db import models


class Title(models.Model):
    url = models.CharField(max_length=511)
    name = models.CharField(max_length=255)
    total_episodes = models.CharField(max_length=255)
    last_available_episode = models.IntegerField()
    last_watched_episode = models.IntegerField(null=True)

    class Meta:
        ordering = ["name"]


class Episode(models.Model):
    number = models.IntegerField()
    url = models.CharField(max_length=511)
    title = models.ForeignKey(
        to="Title",
        on_delete=models.CASCADE,
        related_name="episode",
    )
