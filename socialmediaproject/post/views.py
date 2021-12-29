from django.contrib import messages
# from django.shortcuts import render
from django.urls.base import reverse
from django.http.response import HttpResponseRedirect, JsonResponse
# from django.contrib.auth.decorators import login_required
from post.forms import PostForm
from users.decorators import ajax_check_friend_status, ajax_login_required, check_for_op, user_login_required 

from .models import *

@user_login_required
@check_for_op
def delete_post(request):
    try:
        if request.is_ajax() and request.method == 'POST':
            if 'post' in request.POST:
                post_id = int(request.POST.get('post'))
                Post.objects.get(id=post_id).delete()
            
            elif 'comment' in request.POST:
                comment_id = int(request.POST.get('comment'))
                PostComment.objects.get(id=comment_id).delete()

    except Exception as e:
        print('error in delete_post', e)
        messages.error(request, "Server error")
        return JsonResponse({'server_error':True})
    
    return JsonResponse({'success':True})


@ajax_login_required
@check_for_op
def update_post(request):
    try:
        if request.is_ajax() and request.method == 'POST':
            # print(request.POST)
            if 'post' in request.POST:
                post_id = int(request.POST.get('post'))
                post_text = request.POST.get('text')

                if post_text != '' and post_text.isspace() == False:
                    post = Post.objects.get(id=post_id)
                    post.text = post_text
                    post.save()

            elif 'comment' in request.POST:
                comment_id = int(request.POST.get('comment'))
                comment_text = request.POST.get('text')

                if comment_text != '' and comment_text.isspace() == False:
                    comment = PostComment.objects.get(id=comment_id)
                    comment.text = comment_text
                    comment.save()

    except Exception as e:
        print("error in update_post", e)
        messages.error(request, "Server error")
        return JsonResponse({'server_error':True})
    
    return JsonResponse({'success':True})

@ajax_login_required
@ajax_check_friend_status
def like_post_comment(request):

    context = {}

    try:
        if request.is_ajax() and request.method == 'POST':
            # print(request.POST)
            post_comment_id = int(request.POST.get('post_comment_id'))
            post_comment_like, created = PostCommentLike.objects.get_or_create(post_comment_id=post_comment_id, user=request.user)

            # if user has already liked the post
            if created == False:
                if post_comment_like.is_liked:
                    post_comment_like.is_liked = False
                else:
                    post_comment_like.is_liked = True
                post_comment_like.save()
            
            if post_comment_like.is_liked:
                context['liked'] = True
            else:
                context['liked'] = False
                
            context['like_count'] = PostCommentLike.objects.filter(post_comment_id=post_comment_id, is_liked=True).count()

    except Exception as e:
        print("error in like_post_comment", e)
        messages.error(request, 'Server error')
        context['server_error'] = True
    
    return JsonResponse(context)

# @login_required(login_url='users:user_login')
@user_login_required
def make_post(request):
    context = {}

    try:
        post_form = PostForm()
        if request.method == 'POST' and 'text' in request.POST:
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                # print(request.POST)
                Post.objects.create(
                    text = request.POST.get('text'),
                    op = request.user,
                )
            else:
                messages.warning(request, 'Posts cannot be empty!')
                # post_form.fields['text'].widget.attrs['placeholder'] = "What's on your mind " + request.user.first_name + "?"
                # context['post_form'] = post_form
                # return render(request, 'index.html', context)

    except Exception as e:
        print("error in make_post", e)
        return HttpResponseRedirect(reverse('users:home'))

    return HttpResponseRedirect(reverse('users:home'))

@ajax_login_required
@ajax_check_friend_status
def like_post(request):

    context = {}

    try:
        if request.is_ajax() and request.method == 'POST':
            # print(request.POST)
            post_id = int(request.POST.get('post_id'))
            post_like, created = PostLike.objects.get_or_create(post=Post.objects.get(id=post_id), user=request.user)

            # if user has already liked the post
            if created == False:
                if post_like.is_liked:
                    post_like.is_liked = False
                else:
                    post_like.is_liked = True
                post_like.save()
            
            context['is_liked'] = post_like.is_liked
            context['like_count'] = PostLike.objects.filter(post=post_id, is_liked=True).count()
            context['comment_count'] = PostComment.objects.filter(post_id=post_id).count()

    except Exception as e:
        print("error in like_post", e)
        messages.error(request, "Server error")
        context['server_error'] = True

    
    return JsonResponse(context)

@ajax_login_required
@ajax_check_friend_status
def add_post_comment(request):

    # context = {}

    try:
        if request.is_ajax() and request.method == 'POST':
            # print(request.POST)
            post_id = int(request.POST.get('post_id'))
            comment_text = request.POST.get('comment_text')
            
            if comment_text != '' and comment_text.isspace() == False:
                post_comment = PostComment()
                post_comment.post = Post.objects.get(id=post_id)
                post_comment.commenter = request.user
                post_comment.text = comment_text
                post_comment.save()

            # else:
            #     messages.warning(request, "Comment cannot be empty")
            #     context['empty_comment'] = True

    except Exception as e:
        print("error in add_post_comment", e)
        messages.error(request, "Server error")
        return JsonResponse({'server_error':True})

    
    return JsonResponse({'success':True})


# print(request.POST)
# context['server_error'] = True

# post_comment_id = int(request.POST.get('post_comment_id'))
# sentiment = request.POST.get('sentiment')

# post_comment_sentiment, created = PostCommentSentiment.objects.get_or_create(post_comment_id = post_comment_id, user=request.user)

# if created == False:
#     pass
    # if post_comment_sentiment.sentiment == 'like':
    #     if sentiment == 'like':
    #         post_comment_sentiment.sentiment = None
    #     elif sentiment == 'dislike':
    #         post_comment_sentiment.sentiment = sentiment

    # elif post_comment_sentiment.sentiment == 'dislike':
    #     if sentiment == 'dislike':
    #         post_comment_sentiment.sentiment = None
    #     elif sentiment == 'like':
    #         post_comment_sentiment.sentiment = sentiment
    
    # elif post_comment_sentiment.sentiment == None:
    #     post_comment_sentiment.sentiment = sentiment
# else:
#     if sentiment == 'like':
#         post_comment_sentiment.is_liked = True
#     elif sentiment == 'dislike':
#         post_comment_sentiment.is_disliked = True
    
# post_comment_sentiment.save()

# context['like_btn_text'] = "Like"
# context['dislike_btn_text'] = "Dislike"

# if post_comment_sentiment.is_liked:
#     context['like_btn_text'] = 'Liked!'
#     context['dislike_btn_text'] = 'Dislike'
# elif post_comment_sentiment.is_disliked:
#     context['like_btn_text'] = "Like"
#     context['dislike_btn_text'] = 'Disliked!'

# context['like_count'] = PostCommentSentiment.objects.filter(post_comment_id = post_comment_id, sentiment="like").count()
# context['dislike_count'] = PostCommentSentiment.objects.filter(post_comment_id = post_comment_id, sentiment="dislike").count()

# @login_required(login_url='users:user_login')
# @check_for_op
# def delete_comment(request):
#     # context = {}

#     try:
#         if request.method == 'POST':
#             comment_id = int(request.POST.get('delete_comment'))
#             PostComment.objects.get(id=comment_id).delete()

#     except Exception as e:
#         print('error in delete_post', e)
#         return HttpResponseRedirect(reverse('users:home'))
    
#     return HttpResponseRedirect(reverse('users:home'))