from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_counselor = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    bio = models.TextField(blank=True)

class Appointment(models.Model):
    counselor = models.ForeignKey(UserProfile, related_name='counselor_appointments', on_delete=models.CASCADE)
    client = models.ForeignKey(UserProfile, related_name='client_appointments', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')])


class Payment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=[('paid', 'Paid'), ('pending', 'Pending'), ('failed', 'Failed')])

    def __str__(self):
        return f"{self.appointment} - {self.status} - {self.amount}"


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    message_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.user.username} to {self.receiver.user.username} at {self.timestamp}"
class Feedback(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.appointment} - Rating: {self.rating}"
