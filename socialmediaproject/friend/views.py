from django.contrib import messages
from django.shortcuts import render
from django.urls.base import reverse
from django.http.response import HttpResponseRedirect, JsonResponse#, JsonResponse
from upload.models import UserUpload
#from django.template.defaultfilters import slugify
# from django.contrib.auth.decorators import login_required
\

from user_profile.models import Profile
from users.decorators import ajax_login_required, user_login_required #,ajax_check_friend_status
from .models import Friend
# from users.models import NewUser

@ajax_login_required
def unfriend(request):
    try:
        if request.method=='POST' and request.is_ajax():
            # print(request.POST)
            friend_id = int(request.POST.get('friend_id'))
            Friend.objects.get(id=friend_id).delete()

    except Exception as e:
        print("error in unfriend", e)
        return JsonResponse({'server_error':True})
    
    return JsonResponse({'success':True})

@user_login_required
def accept_friend_request(request):
    context = {}

    try:
        if request.method == 'POST':
            # print(request.POST)

            req_id = int(request.POST.get('req_id'))
            req = Friend.objects.get(id=req_id)
            req.confirmed = True
            req.save()

    except Exception as e:
        print('error in accept friend request', e)
        messages.error(request, "Server error")
        return HttpResponseRedirect(reverse('users:home'))
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@user_login_required
def send_friend_request(request):
    context = {}

    try:
        if request.method == 'POST':
            profile_id = int(request.POST.get('profile_id'))
            receiver = Profile.objects.get(id=profile_id).user
            sender = request.user

            if Friend.objects.filter(sender=sender, receiver=receiver).exists() or Friend.objects.filter(sender=receiver, receiver=sender).exists():
                raise Exception
            else:
                Friend.objects.create(sender=sender, receiver=receiver)

    except Exception as e:
        print("error in send_friend_request", e)
        messages.error(request, "Server error")
        return HttpResponseRedirect(reverse('users:home'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@user_login_required
def friends(request):
    context = {'friends':[], 'frnd_reqs':[]}

    try:

        for friend in Friend.objects.filter(receiver=request.user, confirmed=True) | Friend.objects.filter(sender=request.user, confirmed=True):
            frnd = None
            if friend.sender == request.user:
                frnd = friend.receiver
            elif friend.receiver == request.user:
                frnd = friend.sender

            context['friends'].append({
                'id': friend.id,
                'profile_id': Profile.objects.get(user=frnd).id,
                'name': frnd.full_name,
                'profile_pic': UserUpload.objects.get(id=Profile.objects.get(user=frnd).profile_pic.id).image.url,
            })

        for frnd_req in Friend.objects.filter(receiver=request.user, confirmed=False):
            context['frnd_reqs'].append({
                'id': frnd_req.id,
                'sender' : frnd_req.sender.full_name,
                'sender_pic': UserUpload.objects.get(id=Profile.objects.get(user=frnd_req.sender).profile_pic.id).image.url,
                'sender_profile_id': Profile.objects.get(user=frnd_req.sender).id,
            })

        # print(friends_list)
        # print(context)

    except Exception as e:
        print("error om my_friends", e)
        messages.error(request, 'Server error')
        return HttpResponseRedirect(reverse("users:home"))

    return render(request, 'friend/friends.html', context)

