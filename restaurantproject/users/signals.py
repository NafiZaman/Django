from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import NewUser, Customer
from user_profile.models import Profile#, Friend

@receiver(post_save, sender=Customer)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        group, created = Group.objects.get_or_create(name='customer')
        instance.groups.add(group.id)
        
        try:
            new_user = NewUser.objects.get(email = instance.email)
            profile = Profile.objects.create(user = new_user)
            profile.username = new_user.email.split('@')[0]
            # Friend.objects.create(email_1 = new_user, email_2 = new_user, status = 'confirmed')
        except Exception as e:
            print('error:', e)

# @receiver(post_save, sender=Profile)
# def update_profile(sender, instance, created, **kwargs):
#     if created == False:
#         # instance.save()
#         print(instance)
#         print('profile updated')

# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from .models import Profile
# from users.models import Customer, NewUser


# @receiver(post_save, sender=NewUser)
# def create_profile(sender, instance, created, **kwargs):
#     if created and sender.groups.all()[0].name == 'customer':
#         Profile.objects.create(user=instance)
#         print('profile was created')

# @receiver(post_save, sender=NewUser)
# def update_profile(sender, instance, created, **kwargs):
#     if created == False and sender.groups.all()[0].name == 'customer':
#         instance.profile.save()
#         print('profile updated')