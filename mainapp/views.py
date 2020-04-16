from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404

import mul_app
from datetime import datetime


#from mainapp.models import ProductCategory, Product
#from basketapp.models import Basket
import random
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import Ans_Form
from .forms import AppModForm
from .models import MaapLesson
from django.contrib.auth.decorators import login_required
#create copy
Ma = mul_app.MulApp()

@login_required
def main(request):
    title = 'главная maap v 1.0'

    form = AppModForm(request.POST or None)
# last change
    if request.method == 'POST' and form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #picked = form.cleaned_data.get('picked')
            # do something with your results

            #ans=cleaned_data.get("answer")
            ans = form.cleaned_data.get('app_mode')
            print(ans)

            # reset app
            Ma.__init__()

            #set mode for app
            Ma.SetAppMode(ans)
            Ma.mode = ' '.join(ans)
            #get time from js browser of user
            val = request.POST.get('tstamp')
            val_li = list(val.split("/"))
            Ma.start_time=val_li
            print(val_li)
            #make up lesson log
            lesson = MaapLesson(user=request.user)
            lesson.date= " ".join(val_li[:3])
            lesson.s_time= " ".join(val_li[3:])
            lesson.mode = Ma.mode+'k'
            print(lesson.pk)
            lesson.save()

            print(lesson.pk)
            #save primary key for this session lesson (id)
            Ma.lesson_id = lesson.pk

            return HttpResponseRedirect(f'/mathem/')

    #products = Product.objects.all()[:3]
    links_menu = {}#ProductCategory.objects.all()

    content = {'title': title, 'form': form, 'category': links_menu}

    return render(request, 'mainapp/index.html', content)

def mathem(request):
    title = 'главная maap v 1.0'

    txt0=None
    txt00=None

    list_txt = []


    form = Ans_Form(request.POST or None)

    code=0
    txt2=''
    #обработчик обрабватывает все реквесты страницы и GET и POST
    if request.method == 'GET':
        a, b, code = Ma.eval()
        t = datetime.now()
        Ma.now.clear()
        Ma.now.append(t.minute)
        Ma.now.append(t.second)
        print('aha')


    txt1 = f"вопрос {Ma.ans_num} правильных: {Ma.ans_corr}"

    list_txt.append(txt1)

    if code == 1:
        txt2 = f'cколько будет {a} X {b} =?'
    if code == 2:
        txt2 = f'cколько будет {a} + {b} =?'
    if code == 3:
        txt2 = f'cколько будет {a} - {b} =?'

    list_txt.append(txt2)

    txt3 = ''#f'a1={a}, b1={b}, c1={code}'

    qst = {'txt0': txt0, 'txt00': txt00, 'txt1': txt1, 'txt2': txt2, 'txt3': txt3, 'list_txt': list_txt}


    difference=0
    # if this is a POST request we need to process the form data
    if request.method == 'POST' and form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
        #ans=cleaned_data.get("answer")


        #ans = request.POST.get('answer')
        ans = form.cleaned_data.get("answer")
        val = request.POST.get('tstamp')
        val_li = list(val.split(" "))

        d1 = int(val_li[0])*60+int(val_li[1])
        d2 = Ma.now[0]*60+Ma.now[1]
        diff= d1-d2-1

        print(val_li, Ma.now, diff)

        if diff < 0:
            diff = 0
        #print (ans,a,b,code)
        return HttpResponseRedirect(f'/mathemk/{ans}/{diff}')

    if request.method == 'POST':
        print('clickfinish')
        val = request.POST.get('tstamp1')
        val_li = list(val.split("/"))
        Ma.end_time = val_li
        return HttpResponseRedirect(f'/finish/')

    content = {'title': title, 'form': form, 'qst': qst}


    return render(request, 'mainapp/mathem.html', content)

def mathemk(request, pk, diff):
    title = 'главная maap v 1.0/проверка'

    #txt0=None
    #txt00=None
    list_txt=[]



   # txt0=f"ваш ответ был {pk}"

    #list_txt.append(txt0)

    txt00, check_res = Ma.check_ans(int(pk),int(diff))

    list_txt.append(txt00)

    txt22=f"время затраченное на ответ {diff} сек"

    list_txt.append(txt22)

    txt1 = f'a1={Ma.a1}, b1={Ma.b1}, c1={Ma.c1}, ans_num={Ma.ans_num}, ans_corr={Ma.ans_corr}'

    if Ma.c1 == 1 and check_res==0:#if multip
        mul_tab = Ma.printMatrix(Ma.mult_tabl,Ma.a1*Ma.b1,Ma.a1,0)
        cor_ans = Ma.a1*Ma.b1
        cor_ans = ">"+str(cor_ans)
    else:
        mul_tab = ''
        cor_ans=''

    ans = {'txt00': txt00, 'txt22':txt22, 'txt1': txt1, 'mul_tab': mul_tab, 'list_txt': list_txt, 'ans':cor_ans}

    content = {'title': title, 'ans': ans}

    return render(request, 'mainapp/mathemk.html', content)

def clean_str(str):
    result=""
    i=0
    add = False
    while i<len(str):
        #if ord(str[i]) > ord('0') and ord(str[i])<ord('10'):
        if str[i].isdigit():
            result=result+str[i]
            add = True
        else:
            if add:
                result=result+' '
                add = False
        i=i+1


    return result

def clear_hist(request):
    lessons = MaapLesson.objects.filter(user=request.user)
    lessons.delete()

    print('hist deleted')
    return HttpResponseRedirect(f'/')

def hist(request):
    title = 'главная maap v 1.0/история'
    list_hist = []
    list_hist_row = []
    lessons = MaapLesson.objects.filter(user=request.user)

    list_hist_row = []

    if not lessons:
        print('no lessons')
        list_hist_row.append(f' пусто! ')
        list_hist.append(list_hist_row)
        clr_but=False
    else:
        # make headers of the table history
        list_hist_row = []
        list_hist_row.append(f' Дата занятия')
        list_hist_row.append(f' Режим упр.')
        list_hist_row.append(f' Общее время')
        list_hist_row.append(f' Кол-во вопросов')
        list_hist_row.append(f' % Правильных')
        list_hist.append(list_hist_row)

        for i in lessons:
            list_hist_row = []

            # tab date start dATE time
            new_date = '.'.join(i.date.split())
            new_time = ':'.join(i.s_time.split())

            list_hist_row.append(f'{new_date} {new_time}')
            # tab mode
            a = str(
                i.mode)  # when only one char from db it assumes digital as int so we need to explicitly change it to str again!
            list_hist_row.append(Ma.GetAppModeDesc(a))

            # tab session time secs
            if (i.f_time):
                a1 = clean_str(i.f_time)
                a = a1.split(" ")

                b1 = clean_str(i.s_time)
                b = b1.split(" ")
                # append overall time of session
                diff_time = (int(a[0]) - int(b[0])) * 3600 + (int(a[1]) - int(b[1])) * 60 + int(a[2]) - int(b[2])
                list_hist_row.append(f'{int(diff_time / 60)} мин.')
            else:
                list_hist_row.append(f' нет данных')

            # tab amount
            if (i.ans_amount):
                list_hist_row.append(i.ans_amount)
            else:
                list_hist_row.append(f' нет данных')
            # tab percent correct
            if (i.ans_amount and i.ans_correct):
                corr_percent = int((i.ans_correct / i.ans_amount) * 100)
                list_hist_row.append(f' {corr_percent} %')
            else:
                list_hist_row.append(f' нет данных')

            # next row
            list_hist.append(list_hist_row)

        clr_but=True

    ans = {'list_hist': list_hist,  'clr_but':clr_but}

    content = {'title': title, 'ans': ans}

    return render(request, 'mainapp/hist.html', content)

def finish(request):
    title = 'главная maap v 1.0/результаты'

    txt0=None
    txt00=None
    #call finish result

    list_txt = Ma.finish(1)
    # retrieve lesson from db
    lesson = get_object_or_404(MaapLesson, pk=Ma.lesson_id)
    #update record
    lesson.ans_correct = Ma.ans_corr

    lesson.ans_amount = Ma.ans_num

    lesson.f_time = ' '.join(Ma.end_time[3:])

    #lesson.mode = Ma.mode
    #close edied db lesson record
    lesson.save()

    print (list_txt)

    txt1 = f'ans_num={Ma.ans_num}, ans_corr={Ma.ans_corr}'

    list_hist=[]
    list_hist_row=[]
    lessons = MaapLesson.objects.filter(user=request.user)

    #make headers of the table history
    list_hist_row = []
    list_hist_row.append(f' Дата занятия')
    list_hist_row.append(f' Режим упр.')
    list_hist_row.append(f' Общее время')
    list_hist_row.append(f' Кол-во вопросов')
    list_hist_row.append(f' % Правильных')
    list_hist.append(list_hist_row)

    for i in lessons:
        list_hist_row = []

        #tab date start dATE time
        new_date = '.'.join(i.date.split())
        new_time = ':'.join(i.s_time.split())

        list_hist_row.append(f'{new_date} {new_time}')
        # tab mode
        a = str(i.mode)  # when only one char from db it assumes digital as int so we need to explicitly change it to str again!
        list_hist_row.append(Ma.GetAppModeDesc(a))

        # tab session time secs
        if (i.f_time):
            a1 = clean_str(i.f_time)
            a = a1.split(" ")

            b1 = clean_str(i.s_time)
            b = b1.split(" ")
            # append overall time of session
            diff_time = (int(a[0]) - int(b[0])) * 3600 + (int(a[1]) - int(b[1])) * 60 + int(a[2]) - int(b[2])
            list_hist_row.append(f'{int(diff_time / 60)} мин.')
        else:
            list_hist_row.append(f' нет данных')

        #tab amount
        if (i.ans_amount):
            list_hist_row.append(i.ans_amount)
        else:
            list_hist_row.append(f' нет данных')
        #tab percent correct
        if (i.ans_amount and i.ans_correct):
            corr_percent = int( (i.ans_correct / i.ans_amount )* 100)
            list_hist_row.append(f' {corr_percent} %')
        else:
            list_hist_row.append(f' нет данных')

        #next row
        list_hist.append(list_hist_row)


    ans = {'txt0': txt0, 'txt00': txt00, 'txt1': txt1, 'list_txt': list_txt, 'list_hist':list_hist}
    

    content = {'title': title, 'ans': ans}
    return render(request, 'mainapp/finish.html', content)