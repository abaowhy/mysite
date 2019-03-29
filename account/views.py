from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, UserprofileForm, UserInfoForm, UserForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, UserInfo
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return HttpResponse("Wellcome You. You have been authenticated successfully")
            else:
                return HttpResponse("Sorry. Your username or password is not right.")
        else:
            return HttpResponse("Invalid login")
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request, 'account/login.html', {'form': login_form})


def register(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserprofileForm(request.POST)
        if user_form.is_valid()*userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)
            return HttpResponseRedirect(reverse('account:user_login'))
        else:
            return HttpResponseRedirect(reverse('account:user_register'))
    else:
        user_form = RegistrationForm()
        userprofile_form = UserprofileForm()
        return render(request, 'account/register.html', {'form': user_form, 'profile': userprofile_form})


@login_required(login_url='/account/login')
def myself(request):
    user = User.objects.get(username=request.user.username)
    user_info = UserInfo.objects.get(user=request.user)
    user_profile = UserProfile.objects.get(user=request.user)

    return render(request, 'account/myself.html', {'user': user, 'user_info': user_info, 'user_profile': user_profile})


@login_required(login_url='/account/login')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=request.user)
    user_info = UserInfo.objects.get(user=request.user)

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_profile_form = UserprofileForm(request.POST)
        user_info_from = UserInfoForm(request.POST)

        if user_form.is_valid()*user_profile_form.is_valid()*user_info_from.is_valid():
            user_cd = user_form.cleaned_data
            user_profile_cd = user_profile_form.cleaned_data
            user_info_cd = user_info_from.cleaned_data

            user.email = user_cd['email']
            user_profile.birth = user_profile_cd['birth']
            user_profile.phone = user_profile_cd['phone']
            user_info.school = user_info_cd['school']
            user_info.company = user_info_cd['company']
            user_info.profession = user_info_cd['profession']
            user_info.address = user_info_cd['address']
            user_info.aboutme = user_info_cd['aboutme']

            user.save()
            user_profile.save()
            user_info.save()
        return HttpResponseRedirect("/account/my-information")
    else:
        user_form = UserForm(instance=request.user)
        user_profile_form = UserprofileForm(initial={'birth': user_profile.birth, 'phone': user_profile.phone})
        user_info_from = UserInfoForm(initial={'school': user_info.school, 'company': user_info, 'profession': user_info.profession, 'address': user_info.address, 'aboutme': user_info.aboutme})

        return render(request, 'account/myself_edit.html', {'user_from': user_form, 'user_profile': user_profile_form, 'user_info': user_info_from})


def my_image(request):
    if request.method == "POST":
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user=request.user)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse('1')
    else:
        return render(request, 'account/imagecrop.html',)

