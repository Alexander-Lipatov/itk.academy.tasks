from django.db import models


class Task(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
    ]
    
    task_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='pending')
    worker_id = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.task_name} - {self.status}"