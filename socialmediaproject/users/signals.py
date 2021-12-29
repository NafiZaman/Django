from django.contrib.auth.models import Group
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from upload.models import UserUpload

from .models import *
# from friend.models import Friend
from user_profile.models import Profile
# from upload.models import UserUpload

@receiver(post_save, sender=NewUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser == False:
            instance.full_name = instance.first_name + " " + instance.last_name
            # print(instance.full_name)
            instance.save()
            group, created = Group.objects.get_or_create(name='default_user')
            instance.groups.add(group.id)
        try:
            new_user = NewUser.objects.get(email=instance.email)
            profile = Profile.objects.create(user=new_user)
            UserSetting.objects.create(user=new_user)
            profile.profile_pic = UserUpload.objects.get(image='default_pic.svg')
            profile.save()
        except Exception as e:
            print("Error in signals,", e)

@receiver(post_delete, sender=UserUpload)
def delete_file_from_storage(sender, instance, using, **kwargs):
    # print("This is from signals:", instance.image)
    instance.image.delete(save=False)