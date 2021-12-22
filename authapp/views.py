from django.shortcuts import render

# Create your views here.

# Create your views here.

import sys

from django.shortcuts import render, HttpResponseRedirect

from authapp.forms import MaapUserLoginForm
from authapp.forms import MaapUserRegisterForm
from authapp.forms import MaapUserEditForm, MaapUserProfileEditForm

from django.contrib import auth
from django.urls import reverse


def login(request):
    title = 'вход'
    # get next (when buy unauthenticated
    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST':
        login_form = MaapUserLoginForm(data=request.POST)

        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)
            # когда срабатывает враппер логин-рек (при попытке заказа) в таком виде адресс http://127.0.0.1:8000/auth/login/?next=/basket/add/3/
            # при заходе возврат на ту страницу заказа

            if user and user.is_active:
                auth.login(request, user)
                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect(reverse('main'))

            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main'))
    else:
        login_form = MaapUserLoginForm()

    content = {'title': title, 'login_form': login_form, 'next': next}

    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))

# def register(request):
#     return HttpResponseRedirect(reverse('main'))

def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = MaapUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = MaapUserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)


# def edit(request):
#     return HttpResponseRedirect(reverse('main'))


def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = MaapUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = MaapUserEditForm(instance=request.user)

    content = {'title': title, 'edit_form': edit_form}

    return render(request, 'authapp/edit.html', content)


def email_sched(request):
    title = 'редактирование режима оповещения'

    if request.method == 'POST':
        edit_form = MaapUserProfileEditForm(request.POST, request.FILES, instance=request.user.maapuserprofile)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:email_sched'))
    else:
        edit_form = MaapUserProfileEditForm(instance=request.user.maapuserprofile)

    content = {'title': title, 'edit_form': edit_form}

    return render(request, 'authapp/email_sched.html', content)
