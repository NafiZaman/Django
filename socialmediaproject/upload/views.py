from django.shortcuts import render
from django.urls.base import reverse
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, JsonResponse
from users.decorators import ajax_login_required, user_login_required

from .models import UserUpload
from user_profile.models import Profile

@ajax_login_required
def set_profile_pic(request):
    try:
        profile = Profile.objects.get(user = request.user)

        if request.method == 'POST' and request.is_ajax():
            if 'upload' in request.POST:
                # print(request.POST)
                upload_id = int(request.POST.get('upload'))
                upload = UserUpload.objects.get(id=upload_id)
                
                if upload.user == request.user:
                    # print(request.POST)
                    new_profile_pic = UserUpload.objects.get(id=upload_id)
                    profile.profile_pic = new_profile_pic
                    profile.save()

    except Exception as e:
        print("error in set_profile_pic")
        messages.error(request, "Server error")
        return JsonResponse({'server_error':True})
    
    return JsonResponse({'success':True})

@ajax_login_required
def remove_upload(request):
    try:
        profile = Profile.objects.get(user = request.user)

        if request.method == 'POST' and request.is_ajax():
            if 'upload' in request.POST:
                # print(request.POST)
                upload_id = int(request.POST.get('upload'))
                upload = UserUpload.objects.get(id=upload_id)

                if upload.image != 'default_pic.svg' and upload.user == request.user:
                    upload.delete()
                
                    if profile.profile_pic_id == upload_id:
                        profile.profile_pic = UserUpload.objects.get(image='default_pic.svg')
                        profile.save()
                        
    except Exception as e:
        print("error in remove_upload", e)
        messages.error(request, "Server error")
        return JsonResponse({'server_error':True})
    
    return JsonResponse({'success':True})

@user_login_required
def my_uploads(request):
    context = {}

    try:
        profile = Profile.objects.get(user = request.user)

        context['uploads'] = []
        for upload in UserUpload.objects.filter(user=request.user):
            context['uploads'].append({
                'id':upload.id,
                'is_profile_pic': True if upload.id == profile.profile_pic_id else False,
                'image_path': upload.image.url,
                'date_added': upload.date_added,
            })

    except Exception as e:
        print("error in images", e)
        messages.error(request, "Server error")
        return HttpResponseRedirect(reverse('users:home'))

    return render(request, 'upload/my_uploads.html', context)
