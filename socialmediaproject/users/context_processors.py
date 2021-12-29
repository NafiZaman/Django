from django.urls import reverse
# from django.contrib import messages
from django.http.response import HttpResponseRedirect

from post.models import *
# from friend.models import Friend
from upload.models import UserUpload
from user_profile.models import Profile
from users.models import NewUser#, UserSetting
from friend.models import Friend

from post.forms import PostCommentForm, PostForm

def get_comment_form(post_id):
    comment_form = PostCommentForm()
    comment_form.fields['text'].widget.attrs = {
        'id': "id-comment-text-" + str(post_id),
        'class': 'mt-3',
        'rows':1,
        'style':'resize:none;',
        'placeholder': 'Write a comment',
    }

    return comment_form

def get_posts(query, current_user):
    context = {'posts':[]}

    for post in Post.objects.raw(query):
        post_ = {
            'id':post.id,
            'op': post.op.full_name,
            'op_pic': UserUpload.objects.get(id=Profile.objects.get(user=post.op).profile_pic.id).image.url,
            'profile_id': Profile.objects.get(user=post.op).id,
            'text': post.text,
            'date_added': post.date_added,
            'like_count': PostLike.objects.filter(post_id=post.id, is_liked=True).count(),
            'is_liked': PostLike.objects.filter(post_id=post.id, user=current_user, is_liked=True).exists(),
            'comment_form': get_comment_form(post.id),
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

def extras(request):
    context = {'posts':[], 'people':[], 'post_form': PostForm()}

    try:
        if request.user.is_authenticated == False:
            # get public posts
            query = '''
                select pp.id, pp.op_id, pp.text, pp.date_added
                from users_usersetting
                inner join post_post pp on users_usersetting.user_id = pp.op_id
                where users_usersetting.post_visibility = 'public'
                --order by random()
                limit 5
            '''

            context['posts'] = get_posts(query, None)

            # get random users
            for user in NewUser.objects.all()[:5]:#.order_by('?')[:5]:
                context['people'].append({
                    'name': user.full_name,
                    'profile_pic': UserUpload.objects.get(id=Profile.objects.get(user=user).profile_pic.id).image.url,
                    'profile_id': Profile.objects.get(user=user).id,
                })

            context['post_form'].fields['text'].widget.attrs['placeholder'] = "What's on your mind?"
            context['pic'] = UserUpload.objects.get(image="default_pic.svg").image.url
            context['fname'] = "Anon"

        else:
            context['name'] = request.user.full_name
            context['fname'] = request.user.first_name
            context['pic'] = UserUpload.objects.get(id=Profile.objects.get(user=request.user).profile_pic.id).image.url

            # get all posts of my friends that have post visibility set to true
            query = '''
                select *
                from post_post
                where op_id in (
                    select user_id
                    from users_usersetting
                    where user_id in (
                        select sender_id
                        from friend_friend
                        where receiver_id = '{0}' and confirmed = true
                        union
                        select receiver_id
                        from friend_friend
                        where sender_id = '{1}' and confirmed = true
                        )
                    and post_visibility != 'private'
                    )
                or op_id = '{2}'
                order by date_added
                desc
                --limit 30
            '''.format(request.user.email, request.user.email, request.user.email)

            context['posts'] = get_posts(query, request.user)


            query = '''
                select id, email
                from users_newuser
                where email!='{0}' and email not in(
                    select receiver_id
                    from friend_friend
                    where sender_id = '{1}'

                    union

                    select sender_id
                    from friend_friend
                    where receiver_id = '{2}'
                    )
                --order by random()
                limit 5
            '''.format(request.user.email, request.user, request.user)

            for user in NewUser.objects.raw(query):
                context['people'].append({
                    'name': user.full_name,
                    'profile_pic': UserUpload.objects.get(id=Profile.objects.get(user=user).profile_pic.id).image.url,
                    'profile_id': Profile.objects.get(user=user).id,
                })

            context['post_form'].fields['text'].widget.attrs['placeholder'] = "What's on your mind " + request.user.first_name + "?"
            context['pending_requests'] = Friend.objects.filter(receiver_id=request.user, confirmed=False).exists()

    except Exception as e:
        print("error in context processor", e)
        return HttpResponseRedirect(reverse('users:home'))
    
    return context