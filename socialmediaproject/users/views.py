from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.http.response import HttpResponseRedirect
# from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from difflib import SequenceMatcher
from friend.models import Friend
from upload.models import UserUpload

from users.models import NewUser, UserSetting
from user_profile.models import Profile

from .decorators import unauthenticated_user, user_login_required
from .forms import NewUserForm, UserSettingForm, PersonalInfoForm

def home(request):
    return render(request, 'index.html')

@unauthenticated_user
def register(request):
    context = {}

    try:
        form = NewUserForm()
        form.fields['password1'].label = ""
        form.fields['password2'].label = ""
        form.fields['password1'].help_text = ""
        form.fields['password2'].help_text = ""

        if request.method == 'POST':
            form = NewUserForm(request.POST)
            if form.is_valid():
                new_user=form.save()
                messages.success(request, "Account for "+form.cleaned_data.get('email')+" created successfully.")
                new_user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password1'],)
                login(request, new_user)
                return HttpResponseRedirect(reverse('users:home'))

        context['form'] = form
    except Exception as e:
        print("error in user_registration",e)
        return HttpResponseRedirect(reverse('users:home'))
    
    return render(request, 'users/register.html', context)

@unauthenticated_user
@never_cache
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('users:home'))
        else:
            messages.error(request, "Invalid email or password")

    return render(request, 'users/login.html')

# @login_required(login_url='users:user_login')
@user_login_required
def user_settings(request):
    context= {}
    
    try:
        user_setting = UserSetting.objects.get(user=request.user)
        # personal_info = NewUser.objects.get(user=request.user)
        form = UserSettingForm()
        pi_form = PersonalInfoForm()

        if request.method == 'POST':
            if 'settings' in request.POST:
                form = UserSettingForm(request.POST)
                if form.is_valid():
                    user_setting.post_visibility = form.cleaned_data.get('post_visibility')
                    user_setting.profile_visibility = form.cleaned_data.get('profile_visibility')
                    user_setting.upload_visibility = form.cleaned_data.get('upload_visibility')
                    user_setting.save()
                    messages.success(request, "Your settings have been saved.")

            elif 'info' in request.POST:
                pi_form = PersonalInfoForm(request.POST)
                if pi_form.is_valid():
                    request.user.first_name = pi_form.cleaned_data.get('first_name')
                    request.user.last_name = pi_form.cleaned_data.get('last_name')
                    request.user.dob = pi_form.cleaned_data.get('dob')
                    request.user.gender = pi_form.cleaned_data.get('gender')
                    request.user.save()
                    messages.success(request, "Your personal information have been saved.")
        
        form.fields['post_visibility'].initial = user_setting.post_visibility
        form.fields['profile_visibility'].initial = user_setting.profile_visibility
        form.fields['upload_visibility'].initial = user_setting.upload_visibility

        pi_form.fields['first_name'].initial = request.user.first_name
        pi_form.fields['last_name'].initial = request.user.last_name
        pi_form.fields['dob'].initial = request.user.dob
        pi_form.fields['gender'].initial = request.user.gender


        context['form'] = form
        context['pi_form'] = pi_form

    except Exception as e:
        print("error in user_settings", e)
        messages.error(request, "Server error")
        return HttpResponseRedirect(reverse('users:home'))
    
    return render(request, 'users/user_settings.html', context)

@user_login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:home'))

@user_login_required
def search_people(request):
    context = {'users':[]}
    
    try:
        if request.method == 'GET' and 'query' in request.GET:
            query = request.GET.get('query')

            if len(query) > 0:
                for user in NewUser.objects.filter(first_name__istartswith=query[0]):
                    if user != request.user:
                        sim_ratio = SequenceMatcher(None, query, user.first_name).ratio()
                        # print("This")
                        if sim_ratio*100 >= 15:
                            user_ = {
                                'name': user.full_name,
                                'pic': UserUpload.objects.get(id=Profile.objects.get(user=user).profile_pic.id).image.url,
                                'profile_id': Profile.objects.get(user=user).id,
                                'friends': False,
                                'sent_request':False,
                                'received_request':False,
                            }

                            if Friend.objects.filter(sender=request.user, receiver=user, confirmed=True).exists() or Friend.objects.filter(sender=user, receiver=request.user, confirmed=True).exists():
                                user_['friends'] = True
                            elif Friend.objects.filter(sender=request.user, receiver=user, confirmed=False).exists():
                                user_['sent_request'] = True
                            elif Friend.objects.filter(sender=user, receiver=request.user, confirmed=False).exists():
                                user['received_request'] = True
                            
                            context['users'].append(user_)

    except Exception as e:
        print("error in search_people", e)
        return HttpResponseRedirect(reverse('users:home'))
    
    return render(request, 'users/search.html', context)