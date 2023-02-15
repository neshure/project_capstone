from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.core.exceptions import ObjectDoesNotExist


#check if a user profile exists, if not, create one
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  try:
    if created:
      Profile.objects.create(user=instance)
  except ObjectDoesNotExist:
    Profile.objects.create(user=instance)


#saves the user profile when a user is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
  instance.profile.save()