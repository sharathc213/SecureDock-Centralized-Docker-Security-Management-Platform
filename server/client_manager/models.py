from django.db import models

class Client(models.Model):
    ip_address = models.CharField(max_length=100)
    token = models.CharField(max_length=255)  # Define a token field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.token}"
