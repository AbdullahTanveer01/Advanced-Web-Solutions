# sensore_app/models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ("patient", "Patient"),
        ("clinician", "Clinician"),
        ("admin", "Admin"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
class PressureFrame(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    matrix = models.JSONField()  # stores 32×32 numbers (1–4095)
    peak_pressure = models.IntegerField()
    contact_area = models.FloatField()
    alert_flag = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} @ {self.timestamp}"
class ThreadComment(models.Model):
    frame = models.ForeignKey(PressureFrame, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    profile = models.ManyToManyField(Profile)
    