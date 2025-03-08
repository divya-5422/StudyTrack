from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    hours = models.PositiveIntegerField(null=True, blank=True)  # Allow blank for initial input
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Prevent modification of hours after it's set
        if self.pk:  # If the task already exists
            original = Task.objects.get(pk=self.pk)
            if original.hours is not None:  # If hours were already set, don't allow changes
                self.hours = original.hours
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title