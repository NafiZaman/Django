from django.contrib import messages
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from functools import wraps

import json
from friend.models import Friend
from post.models import Post, PostComment
from users.models import NewUser

def user_login_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:user_login'))
        else:
            return view_func(request, *args, **kwargs)
    
    return wrapper_func

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:home'))
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not allowed to view this page.")
        return wrapper_func

    return decorator

def check_for_op(view_func):
    def wrapper_func(request, *args, **kwargs):
        try:
            if 'post' in request.POST:
                if request.user == Post.objects.get(id=int(request.POST.get('post'))).op:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse(json.dumps({'server_error':True}))

            elif 'comment' in request.POST:
                if request.user == PostComment.objects.get(id=int(request.POST.get('comment'))).commenter:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse(json.dumps({'server_error':True}))
            else:
                HttpResponse(json.dumps({'server_error':True}))

        except Exception as e:
            print("error in check_for_op", e)
            return HttpResponse(json.dumps({'server_error':True}))
    
    return wrapper_func

def ajax_login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(json.dumps({'login_required': True}))
        else:
            return view(request, *args, **kwargs)
    return wrapper

def ajax_check_friend_status(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        try:
            op = None
            if 'post_id' in request.POST:
                op = Post.objects.get(id=request.POST.get('post_id')).op
            elif 'post_comment_id' in request.POST:
                # print("HERE HRE")
                post = PostComment.objects.get(id=request.POST.get('post_comment_id')).post
                op = Post.objects.get(id=post.id).op
                # print(op)

            if op:
                if op == request.user or Friend.objects.filter(sender=request.user, receiver=op, confirmed=True).exists() or Friend.objects.filter(sender=op, receiver=request.user, confirmed=True).exists():
                    return view(request, *args, **kwargs)
                else:
                    messages.info(request, "Add this person to like or comment on their posts")
                    return HttpResponse(json.dumps({'not_friends': True}))
            else:
                messages.error(request, "Server error")
                return HttpResponse(json.dumps({'server_error':True}))

        except Exception as e:
            print("error in ajax_check_friend_status", e)
            messages.error(request, "Server error")
            return HttpResponse(json.dumps({'server_error':True}))
    return wrapper