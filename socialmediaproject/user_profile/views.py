from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls.base import reverse
# from django.contrib.auth.decorators import login_required
from users.decorators import user_login_required
from django.http.response import HttpResponseRedirect

# from users.models import NewUser
from friend.models import Friend
from upload.models import UserUpload
from user_profile.models import Profile
from post.models import Post, PostComment, PostLike, PostCommentLike
from users.models import UserSetting
from .forms import ProfileForm

def get_posts(current_user, the_user):
    context = {'posts':[]}

    for post in Post.objects.filter(op=the_user).order_by('-date_added'):
        post_ = {
            'id':post.id,
            'op': post.op.full_name,
            'profile_id': Profile.objects.get(user=post.op).id,
            'op_pic': UserUpload.objects.get(id=Profile.objects.get(user=post.op).profile_pic.id).image.url,
            'text': post.text,
            'date_added': post.date_added,
            'like_count': PostLike.objects.filter(post_id=post.id, is_liked=True).count(),
            'is_liked': PostLike.objects.filter(post_id=post.id, user=current_user, is_liked=True).exists(),
            'mutable': True if post.op == current_user else False,
            'comment_count': PostComment.objects.filter(post_id=post.id).count(),
            'comments': [],
        }

        for comment in PostComment.objects.filter(post_id=post.id):
            post_['comments'].append({
                'id': comment.id,
                'commenter': comment.commenter.full_name,
                'commenter_pic': UserUpload.objects.get(id=Profile.objects.get(user=comment.commenter).profile_pic.id).image.url,
                'profile_id': Profile.objects.get(user=comment.commenter).id,
                'text': comment.text,
                'date_added': comment.date_added,
                'like_count': PostCommentLike.objects.filter(post_comment_id = comment.id, is_liked=True).count(),
                'is_liked': PostCommentLike.objects.filter(post_comment_id = comment.id, user=current_user, is_liked=True).exists(),
                'mutable': True if comment.commenter == current_user else False,
            })

        context['posts'].append(post_)
    
    return context['posts']


@user_login_required
def view_profile(request, name, id):
    context = {}

    try:

        if request.method == 'GET':
            if Profile.objects.get(id=id).user == request.user:
                return HttpResponseRedirect(reverse("profile:my_profile"))

            else:
                profile = Profile.objects.get(id=id)
                context['profile'] = profile
                context['profile_id'] = id
                context['profile_user_name'] = name.title().replace('-', ' ')
                # context['profile_user_id'] = NewUser.objects.get(email=profile.user).id

                sender_receiver = Friend.objects.filter(sender=request.user, receiver=profile.user).first()
                receiver_sender = Friend.objects.filter(sender=profile.user, receiver=request.user).first()

                # print(sender_receiver[0].)

                context['friends'] = False
                if sender_receiver:
                    if sender_receiver.confirmed:
                        context['friends'] = True
                    else:
                        context['sent_request'] = True
                elif receiver_sender:
                    if receiver_sender.confirmed:
                        context['friends'] = True
                    else:
                        context['received_request'] = True
                else:
                    context['friends'] = False
                # print("This")
                
                profile_is_public = UserSetting.objects.filter(user=profile.user, profile_visibility="public").exists()
                profile_is_visible_to_friends = UserSetting.objects.filter(user=profile.user, profile_visibility="friends").exists()

                if profile_is_public or (context['friends'] == True and profile_is_visible_to_friends):
                    context['info'] = {
                        'bio': profile.bio,
                        'education': profile.education,
                        'rel_status': profile.rel_status,
                        'work': profile.work,
                        'location': profile.location,
                    }

                posts_public = UserSetting.objects.filter(user=profile.user, post_visibility="public").exists()
                post_visible_to_friends = UserSetting.objects.filter(user=profile.user, post_visibility="friends").exists()
                
                context['posts'] = {}
                if posts_public or (context['friends'] == True and post_visible_to_friends):
                    context['posts'] = get_posts(request.user, profile.user)
                    # print(context['posts'])

    except Exception as e:
        print("error in view_profile", e)
        return HttpResponseRedirect(reverse('users:home'))

    return render(request, 'user_profile/view_profile.html', context)


@user_login_required
def my_profile(request):
    context = {'posts':[]}

    try:
        profile = Profile.objects.get(user=request.user)
        profile_form = ProfileForm(initial={
            'bio':profile.bio,
            'education':profile.education,
            'rel_status':profile.rel_status,
            'work':profile.work,
            'location': profile.location,
        })

        if request.method == 'POST':
            profile_form = ProfileForm(request.POST, request.FILES)

            if profile_form.is_valid():
                if 'pic' in request.FILES:
                    # print('profile_form is valid')
                    if UserUpload.objects.filter(user=request.user).count() < 2:
                        user_upload = UserUpload(image = request.FILES['pic'])
                        user_upload.user = request.user
                        user_upload.upload_type = "profile_pic"
                        user_upload.save()

                        profile.profile_pic = user_upload
                        
                    else:
                        messages.warning(request, "You can't upload more than 2 images.")

                profile.bio = profile_form.cleaned_data.get('bio')
                profile.education = profile_form.cleaned_data.get('education')
                profile.rel_status = profile_form.cleaned_data.get('rel_status')
                profile.work = profile_form.cleaned_data.get('work')
                profile.location = profile_form.cleaned_data.get('location')
                profile.save()

        # if profile.profile_pic:
            # context['profile_pic'] = UserUpload.objects.get(id=profile.profile_pic.id).image.url
        # else:
        #     context['profile_pic'] = UserUpload.objects.get(image="default_pic.svg").image.url
        
        context['bio'] = profile.bio
        context['education'] = profile.education
        context['rel_status'] = profile.rel_status
        context['work'] = profile.work
        context['location'] = profile.location
        context['form'] = profile_form
        context['profile_pic'] = UserUpload.objects.get(id=profile.profile_pic.id).image.url
        context['posts'] = get_posts(request.user, request.user)
        
        # print("These are the posts:", context['posts'])

    except Exception as e:
        print("error in profile", e)
        messages.error(request,'Server error')
        return HttpResponseRedirect(reverse('users:home'))

    return render(request, 'user_profile/my_profile.html', context)