from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import *

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, bio="I am one-piece fan")

@receiver(post_save, sender=Order)
def order_confirmation_email(sender, instance, created, **kwargs):
    if created:
        subject = "Order Placed Successfully"
        message = f"Thank you for your order #{instance.id}! We'll process it right away."
        from_email = "rev@gmail.com"
        recipient_list = [instance.user.email]  # Note: this should be a list
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email: {str(e)}")  # For debugging