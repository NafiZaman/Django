from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from users.models import Customer

from .models import Profile
from .forms import ProfileForm
from users.decorators import allowed_users


@login_required(login_url=['users:user_login'])
@allowed_users(allowed_roles=['customer'])
def my_profile(request):
    context = {}

    try:
        form = ProfileForm()
        user = Customer.objects.get(email=request.user)
        profile = Profile.objects.get(user=user)
        
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                user.phone = form.cleaned_data.get('phone')
                profile.username = form.cleaned_data.get('username')
                profile.date_of_birth = form.cleaned_data.get('date_of_birth')
                profile.address = form.cleaned_data.get('address')
                profile.post_code = form.cleaned_data.get('post_code')

                user.save()
                profile.save()

                messages.success(request, 'Profile updated!')

                return HttpResponseRedirect(reverse('user_profile:my_profile'))

        
        form.fields['username'].initial = profile.username
        form.fields['phone_number'].initial = user.phone_number
        form.fields['date_of_birth'].initial = profile.date_of_birth
        form.fields['address'].initial = profile.address
        form.fields['post_code'].initial = profile.post_code
        
        # print(form.fields['phone_number'].html)

        context['form'] = form
    
    except Exception as e:
        print(e)
        messages.error(request, 'Server error.')

    return render(request, 'user_profile/my_profile.html', context)

# @login_required(login_url=['users:user_login'])
# @allowed_users(allowed_roles=['customer'])
# def my_profile(request):
    # context = {}

    # try:
    #     if request.method == 'POST':
    #         form = PostForm(request.POST)

    #         if form.is_valid():
    #             post_content = request.POST.get('content')
    #             Post.objects.create(
    #                 author = request.user,
    #                 content = post_content
    #             )

    #     context['posts'] = []
    #     for post in Post.objects.filter(author=request.user).order_by('-date_posted'):
    #         context['posts'].append(
    #             {   
    #                 'id':post.id,
    #                 'post_content':post.content,
    #                 'date_posted': post.date_posted,
    #                 'like_btn_text': 'Like',
    #                 # 'like_btn_text': 'Liked! ' + str(post.likes.count()) if post.likes.filter(email=request.user).exists() else 'Like '+str(post.likes.count()),
    #             }
    #         )
    
    #     context['people'] = []
    #     for profile in Profile.objects.all():
    #         if Friend.objects.filter(email_1=request.user, email_2=profile.user).exists() == False:
    #             context['people'].append({
    #                 'profile_id': profile.id,
    #                 'name':profile.user.customer.full_name,
    #             })

    #     context['post_form'] = PostForm()

    # except Exception as e:
    #     print('error in profile app,', e)
    #     messages.warning(request, 'Internal Server Error')
    #     return HttpResponseRedirect(reverse('home:home'))

    # return render(request, 'user_profile/my_profile.html')


# def view_profile(request, profile_id):
#     context = {}

#     try:
#         profile = Profile.objects.get(pk=profile_id)

#         if request.method == 'POST':
#             if 'add_as_friend' in request.POST:
#                 if Friend.objects.filter(email_1=profile.user.email, email_2=request.user).exists() == False and Friend.objects.filter(email_1=request.user, email_2=profile.user.email).exists() == False:
#                     Friend.objects.create(email_1=NewUser.objects.get(email=request.user), email_2=NewUser.objects.get(email=profile.user.email), status='requested')
        
#         context['name'] = profile.user.customer.full_name
#         context['posts'] = []
#         for post in Post.objects.filter(author=profile.user.email).order_by('-date_posted'):
#             context['posts'].append(
#                 {   
#                     'id':post.id,
#                     'post_content':post.content,
#                     'date_posted': post.date_posted,
#                     'like_btn_text': 'Like',
#                     # 'like_btn_text': 'Liked! ' + str(post.likes.count()) if post.likes.filter(email=request.user).exists() else 'Like '+str(post.likes.count()),
#                 }
#             )

#         # This user has already sent you a friend request
#         friend_request_received = Friend.objects.filter(email_1=profile.user.email, email_2= request.user).first()
#         # You have sent a friend request to this user
#         friend_request_sent = Friend.objects.filter(email_1=request.user, email_2 = profile.user.email).first()

#         context['friend_status'] = 'none'
#         if friend_request_received:
#             if friend_request_received.status == 'requested':
#                 context['friend_status'] = 'received'
#             elif friend_request_received.status == 'confirmed':
#                 context['friend_status'] = 'confirmed'
#         elif friend_request_sent:
#             if friend_request_sent.status == 'requested':
#                 context['friend_status'] = 'sent'
#             elif friend_request_sent.status == 'confirmed':
#                 context['friend_status'] = 'confirmed'
        

#     except Exception as e:
#         print(e)
#         messages.warning(request, 'Internal server error')
#         return HttpResponseRedirect(reverse('home:home'))

#     return render(request, 'user_profile/profile.html', context)

# def like_post(request):
#     context = {}

#     # try:
#     #     if request.is_ajax and request.method == 'POST':
#     #         post_id = request.POST.get('post_id')
#     #         post = Post.objects.get(pk=post_id)
#     #         context['like_btn_text'] = "Like"
#     #         customer = Customer.objects.get(email=request.user)


#     #         # if post.profile.friends.filter(email=request.user).exists() == False:
#     #         #     context['not_friends'] = True
#     #         # elif post.likes.filter(email=request.user).exists():
#     #         #     post.likes.remove(customer)
#     #         # else:
#     #         #     post.likes.add(customer)
#     #         #     context['like_btn_text'] = "Liked! "
            
#     #         context['post_id'] = post_id
#     #         context['like_btn_text'] += str(post.likes.count()) 

#     # except Exception as e:
#     #     print('error:', e)
#     #     context['server_error'] = True

#     return JsonResponse(context)