# Create your views here.

from datetime import datetime

from django.contrib.auth.decorators import login_required
# from mainapp.models import ProductCategory, Product
# from basketapp.models import Basket
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .forms import Ans_Form
from .forms import AppModForm
from .models import MaapLesson


#create copy

from .mul_app import SetAppMode, eval, check_ans, GetAppModeDesc, finish_lesson, printMatrix


#from .mainapp import mul_app

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

            (lesson.mult, lesson.addi, lesson.subt) = SetAppMode(ans)

            lesson.mode = ' '.join(ans)

           # print(lesson.pk)

            # set mode for app

            # get time from js browser of user
            val = request.POST.get('tstamp')
            val_li = list(val.split("/"))

            start_date = {'day':val_li[0],
                          'mon':val_li[1],
                          'year':val_li[2],
                          'hour':val_li[3],
                          'min':val_li[4],
                          'sec':val_li[5]}

            lesson.s_time = json.dumps(start_date)

            print(lesson.s_time)

            # make 1 st object in favour ans queue
            favor_ans = {1: {'a': 0,
                             'b': 0,
                             'c': 0,
                             'd': 0}
                         }
            lesson.favor_ans = json.dumps(favor_ans)

            # make 1 st object in hist  queue
            hist = {1: {'a': 0,
                        'b': 0,
                        'c': 0}
                    }
            lesson.hist = json.dumps(hist)


            lesson.save()

            print(lesson.pk)
            #save primary key for this session lesson (id)


            return HttpResponseRedirect(f'/mathem/{lesson.pk}')
    else:#GET
        form = AppModForm()

    #products = Product.objects.all()[:3]
    links_menu = {}#ProductCategory.objects.all()

    content = {'title': title, 'form': form, 'category': links_menu}

    return render(request, 'mainapp/index.html', content)
import os,json
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
        hist = json.loads(lesson.hist)#load hist from db

        a, b, code, hist1 = eval(lesson.mult,lesson.addi,lesson.subt,lesson.nx,lesson.ny,lesson.ax,lesson.two_digit,lesson.sx,\
                            lesson.no_minus,lesson.no_dec_mul,hist,lesson.hist_depth)

        lesson.a1 = a#update db
        lesson.b1 = b
        lesson.c1 = code
        lesson.hist = json.dumps(hist1)

        t = datetime.now()

        #copy data to db in json format

        tim = {'min':t.minute,
               'sec':t.second}

        js_tim=json.dumps(tim)

        print(js_tim)

        lesson.qst_time = js_tim

        print(f'aha {lesson.qst_time}')

        lesson.save()

        txt1 = f"вопрос {lesson.ans_amount} правильных: {lesson.ans_correct}"

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

        content = {'title': title, 'form': form, 'qst': qst}

        return render(request, 'mainapp/mathem.html', content)

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

        d1 = int(val_li[0])*60+int(val_li[1])#current time 0 - min 1 - sec

        print(f'post {lesson.qst_time} {val_li}')
        time_dic = json.loads(lesson.qst_time)

        d2 = time_dic['min']*60 + time_dic['sec']

        diff= d1-d2-1



        if diff < 0:
            diff = 0
        #print (ans,a,b,code)

        return HttpResponseRedirect(f'/mathemk/{lesson.pk}/{ans}/{diff}')

    if request.method == 'POST':
        print('clickfinish')
        val = request.POST.get('tstamp1')
        val_li = list(val.split("/"))

        # update db with finish time
        tim = {'hour': val_li[3],
               'min': val_li[4],
               'sec': val_li[5]}

        lesson.f_time = json.dumps(tim)

        print(f'fin time {lesson.f_time}')
        #decrease amount of questions as quit was pressed

        lesson.ans_amount -= 1

        lesson.save()
        return HttpResponseRedirect(f'/finish/{lesson.pk}')



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
        #add to dict if diff time > favor_thresold_time:

        favor_ans = json.loads(lesson.favor_ans)

        #debug diff +=15
        if diff > lesson.favor_thresold_time:
            already_in = False
            for id, key in favor_ans.items():
                a = key['a']
                b = key['b']
                if lesson.a1 == a and lesson.b1 == b:
                    already_in = True

            if already_in == False:
                elem = {'a':lesson.a1,
                        'b':lesson.b1,
                        'c': lesson.c1,
                        'd': diff}  # a,b,op,diff_time
                #make new index
                idx = 0
                for i in favor_ans.keys():
                    if int(i) > idx:
                        idx = int(i)

                favor_ans[idx+1] = elem
                # to add to favor_ans
                #store it in db
                lesson.favor_ans = json.dumps(favor_ans)
                # favor_ans.append(elem)

        txt00, check_res = check_ans(int(pk2),int(diff),lesson.a1,lesson.b1,lesson.c1)

        lesson.ans_amount += 1
        if check_res == 1:
            lesson.ans_correct +=1

        lesson.save()

        list_txt.append(txt00)

        txt22=f"время затраченное на ответ {diff} сек"

        list_txt.append(txt22)

        txt1 = f'a1={lesson.a1}, b1={lesson.b1}, c1={lesson.c1}, ans_num={lesson.ans_amount}, ans_corr={lesson.ans_correct}'
        #add mult table
        if lesson.c1 == 1 and check_res == 0:#if multip
            mult_tabl = []
            ny = lesson.ny
            nx = lesson.nx
            for i in range(1, ny + 1):
                row = []
                for j in range(1, nx + 1):
                    row.append(i * j)
                mult_tabl.append(row)

            # self.printMatrix(self.mult_tabl,0,0,0)
            mul_tab = printMatrix(mult_tabl, lesson.a1*lesson.b1, lesson.a1,0)
            cor_ans = lesson.a1*lesson.b1
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
            start_date = json.loads(i.s_time)
            new_date = start_date['day'] + '.' + start_date['mon'] + '.' + start_date['year']
            new_time = start_date['hour'] + ':' + start_date['min'] + ':' + start_date['sec']

            list_hist_row.append(f'{new_date} {new_time}')
            # tab mode
            a = str(
                i.mode)  # when only one char from db it assumes digital as int so we need to explicitly change it to str again!
            list_hist_row.append(GetAppModeDesc(a))

            try:
                end_time = json.loads(i.f_time)

                diff_time = int(end_time['sec']) - int(start_date['sec']) + \
                            (int(end_time['min']) - int(start_date['min'])) * 60 + \
                            (int(end_time['hour']) - int(start_date['hour'])) * 3600

                list_hist_row.append(f'{int(diff_time / 60)} мин.')
            except:
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

    favor_ans = json.loads(lesson.favor_ans)
    #get time for this session
    start_date = json.loads(lesson.s_time)
    end_time = json.loads(lesson.f_time)

    diff_time = int(end_time['sec']) - int(start_date['sec']) + \
                (int(end_time['min']) - int(start_date['min'])) * 60 + \
                (int(end_time['hour']) - int(start_date['hour'])) * 3600

    f_time = int (diff_time / 60)

    list_txt = finish_lesson(f_time, lesson.ans_amount, lesson.ans_correct, favor_ans, lesson.favor_thresold_time)

    txt1 = f'ans_num={lesson.ans_amount}, ans_corr={lesson.ans_correct}'

    lesson.save()

    list_hist=[]
    list_hist_row=[]



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
        start_date = json.loads(i.s_time)
        new_date = start_date['day'] +'.'+ start_date['mon']+ '.' + start_date['year']
        new_time = start_date['hour'] +':'+ start_date['min']+ ':' + start_date['sec']

        list_hist_row.append(f'{new_date} {new_time}')
        # tab mode
        a = str(i.mode)  # when only one char from db it assumes digital as int so we need to explicitly change it to str again!
        list_hist_row.append(GetAppModeDesc(a))

        try:
            end_time = json.loads(i.f_time)

            diff_time =   int(end_time['sec']) - int(start_date['sec']) + \
                        ( int(end_time['min']) - int(start_date['min']) ) * 60 +\
                        ( int(end_time['hour']) - int(start_date['hour']) ) * 3600

            list_hist_row.append(f'{int(diff_time / 60)} мин.')
        except:
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