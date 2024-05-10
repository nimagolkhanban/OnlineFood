from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from vendor.models import Vendor
from .models import User, UserProfile


# receiver signal for profile
@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, *args, **kwargs):
    print("a userprofile has been saved")


