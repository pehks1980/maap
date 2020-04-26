from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404


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




@login_required
def main(request):
    title = 'главная maap v 1.0'

# last change
    if request.method == 'POST':
        form = AppModForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #picked = form.cleaned_data.get('picked')
            # do something with your results

            #ans=cleaned_data.get("answer")
            ans = form.cleaned_data.get('app_mode')
            print(ans)


            #make up lesson log
            lesson = MaapLesson(user=request.user)
            # reset app
            lesson.Ma.__init__()
            lesson.Ma.SetAppMode(ans)
            lesson.Ma.mode = ' '.join(ans)
            lesson.mode = lesson.Ma.mode+'k'
            print(lesson.pk)
            # set mode for app

            # get time from js browser of user
            val = request.POST.get('tstamp')
            val_li = list(val.split("/"))
            lesson.Ma.start_time = val_li
            print(val_li)

            lesson.save()
            #lesson.Ma.lesson_id = lesson.pk
            print(lesson.pk)
            #save primary key for this session lesson (id)


            return HttpResponseRedirect(f'/mathem/{lesson.pk}')
    else:#GET
        form = AppModForm()

    #products = Product.objects.all()[:3]
    links_menu = {}#ProductCategory.objects.all()

    content = {'title': title, 'form': form, 'category': links_menu}

    return render(request, 'mainapp/index.html', content)

def mathem(request,pk):
    title = 'Математика '

    txt0=None
    txt00=None

    list_txt = []


    form = Ans_Form(request.POST or None)

    lesson = MaapLesson.objects.get(user=request.user,pk=pk)

    code=0
    txt2=''
    #обработчик обрабватывает все реквесты страницы и GET и POST
    if request.method == 'GET':
        a, b, code = lesson.Ma.eval()
        t = datetime.now()
        lesson.Ma.now.clear()
        lesson.Ma.now.append(t.minute)
        lesson.Ma.now.append(t.second)
        print('aha')


    txt1 = f"вопрос {lesson.Ma.ans_num} правильных: {lesson.Ma.ans_corr}"

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
        d2 = lesson.Ma.now[0]*60+lesson.Ma.now[1]
        diff= d1-d2-1

        print(val_li, lesson.Ma.now, diff)

        if diff < 0:
            diff = 0
        #print (ans,a,b,code)
        lesson.save()
        return HttpResponseRedirect(f'/mathemk/{lesson.pk}/{ans}/{diff}')

    if request.method == 'POST':
        print('clickfinish')
        val = request.POST.get('tstamp1')
        val_li = list(val.split("/"))
        lesson.Ma.end_time = val_li

        lesson.save()
        return HttpResponseRedirect(f'/finish/{lesson.pk}')

    content = {'title': title, 'form': form, 'qst': qst}

    lesson.save()
    return render(request, 'mainapp/mathem.html', content)

def mathemk(request, pk1, pk2, diff):
    title = 'главная maap v 1.0/проверка'

    if request.method == 'POST':
        print('clicknext')

        return HttpResponseRedirect(f'/mathem/{pk1}')
    else:#GET
        #txt0=None
        #txt00=None
        list_txt=[]

        lesson = MaapLesson.objects.get(user=request.user, pk=pk1)

       # txt0=f"ваш ответ был {pk}"

        #list_txt.append(txt0)

        txt00, check_res = lesson.Ma.check_ans(int(pk2),int(diff))

        list_txt.append(txt00)

        txt22=f"время затраченное на ответ {diff} сек"

        list_txt.append(txt22)

        txt1 = f'a1={lesson.Ma.a1}, b1={lesson.Ma.b1}, c1={lesson.Ma.c1}, ans_num={lesson.Ma.ans_num}, ans_corr={lesson.Ma.ans_corr}'

        if lesson.Ma.c1 == 1 and check_res==0:#if multip
            mul_tab = lesson.Ma.printMatrix(lesson.Ma.mult_tabl,lesson.Ma.a1*lesson.Ma.b1,lesson.Ma.a1,0)
            cor_ans = lesson.Ma.a1*lesson.Ma.b1
            cor_ans = ">"+str(cor_ans)
        else:
            mul_tab = ''
            cor_ans=''

        ans = {'txt00': txt00, 'txt22':txt22, 'txt1': txt1, 'mul_tab': mul_tab, 'list_txt': list_txt, 'ans':cor_ans}

        content = {'title': title, 'ans': ans}

        lesson.save()
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
    title = f'главная maap v 1.0/история уроков '
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
            a = str(i.mode)  # when only one char from db it assumes digital as int so we need to explicitly change it to str again!
            list_hist_row.append(i.Ma.GetAppModeDesc(a))

            # tab session time secs
            if (i.f_time):
                a1 = clean_str(i.f_time)
                a = a1.split(" ")

                b1 = clean_str(i.s_time)
                b = b1.split(" ")
                # append overall time of session
                if len(a) == 0 or len(b) == 0:
                    diff_time = (int(a[0]) - int(b[0])) * 3600 + (int(a[1]) - int(b[1])) * 60 + int(a[2]) - int(b[2])
                    list_hist_row.append(f'{int(diff_time / 60)} мин.')
                else:
                    list_hist_row.append('нет данных')
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

def finish(request,pk):
    title = 'главная maap v 1.0/результаты'

    txt0=None
    txt00=None
    #call finish result

    # retrieve lesson from db
    lesson = get_object_or_404(MaapLesson, pk=pk)
    #update record
    list_txt = lesson.Ma.finish(1)

    lesson.ans_correct = lesson.Ma.ans_corr

    lesson.ans_amount = lesson.Ma.ans_num

    lesson.date = ' '.join(lesson.Ma.start_time[:3])

    lesson.s_time = ' '.join(lesson.Ma.start_time[3:])

    lesson.f_time = ' '.join(lesson.Ma.end_time[3:])


    #lesson.mode = Ma.mode
    #close edited db lesson record

    txt1 = f'ans_num={lesson.Ma.ans_num}, ans_corr={lesson.Ma.ans_corr}'

    list_hist=[]
    list_hist_row=[]
    lesson.save()

    print(list_txt)

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
        list_hist_row.append(i.Ma.GetAppModeDesc(a))

        # tab session time secs
        if (i.f_time):
            a1 = clean_str(i.f_time)
            a = a1.split(" ")

            b1 = clean_str(i.s_time)
            b = b1.split(" ")
            # append overall time of session
            if len(a) > 0 and len(b) > 0 :
                diff_time = (int(a[0]) - int(b[0])) * 3600 + (int(a[1]) - int(b[1])) * 60 + int(a[2]) - int(b[2])
                list_hist_row.append(f'{int(diff_time / 60)} мин.')
            else:
                list_hist_row.append('нет данных')
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