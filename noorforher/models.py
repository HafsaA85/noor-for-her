from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class AnxietyTrigger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="triggers")
    title = models.CharField(max_length=200)
    situation = models.TextField(help_text="What happened? Where were you?")  # Trigger
    thoughts = models.TextField(
        blank=True,
        help_text="What thoughts came to your mind?",
    )  # Thought
    feelings = models.TextField(
        blank=True,
        help_text="How did you feel in your body?",
    )  # Emotion
    intensity = models.IntegerField(help_text="Rate anxiety 1–10")
    behaviour = models.TextField(
        blank=True,
        help_text="What did you do or avoid?",
    )  # Behaviour
    outcome = models.TextField(
        blank=True,
        help_text="What was the result or consequence?",
    )  # Outcome
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.title} ({self.date})"
