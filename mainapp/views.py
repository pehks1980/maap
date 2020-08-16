# Create your views here.

from datetime import datetime
import pytz
from collections import OrderedDict

from django.contrib.auth.decorators import login_required
# from mainapp.models import ProductCategory, Product
# from basketapp.models import Basket
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from django.core.files.storage import default_storage
from django.urls import reverse

from cron import cron_notify

from .forms import Ans_Form
from .forms import AppModForm
from .models import MaapLesson, MaapReport

from authapp.models import MaapUserProfile

from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# create copy

from .mul_app import SetAppMode, eval, check_ans, GetAppModeDesc, finish_lesson, printMatrix
import os, json

# from .mainapp import mul_app

@login_required
def main(request):

    title = 'главная maap v 1.0'

    # a = MaapReport()

    # last change
    if request.method == 'POST':
        form_app = AppModForm(request.POST)
        if form_app.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # picked = form.cleaned_data.get('picked')
            # do something with your results

            # ans=cleaned_data.get("answer")
            ans = form_app.cleaned_data.get('app_mode')
            print(ans)

            # make up lesson log
            lesson = MaapLesson(user=request.user)
            # reset app

            (lesson.mult, lesson.addi, lesson.subt, lesson.divn) = SetAppMode(ans)

            lesson.mode = ' '.join(ans)

            # print(lesson.pk)

            # set mode for app

            # get time from js browser of user
            val = request.POST.get('tstamp')
            val_li = list(val.split("/"))

            start_date = {'day': val_li[0],
                          'mon': val_li[1],
                          'year': val_li[2],
                          'hour': val_li[3],
                          'min': val_li[4],
                          'sec': val_li[5]}

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

            # file_name = 'lesson_data.json'
            # file_content_string = json.dumps(favor_ans)
            # content_file = ContentFile(file_content_string)
            # generacte filefield
            report = MaapReport()
            # report.file_rep.save(file_name, content_file)
            report.save()

            lesson.report_id = report.pk

            lesson.save()

            print(lesson.pk)
            # save primary key for this session lesson (id)

            # start to ajax version mathemj
            return HttpResponseRedirect(f'/mathemj/{lesson.pk}')
    else:  # GET
        form_app = AppModForm()

    # products = Product.objects.all()[:3]
    #links_menu = {}  # ProductCategory.objects.all()

    content = {'title': title, 'form': form_app}

    return render(request, 'mainapp/index.html', content)

def checkCron(request):
    #call cron method to check & debug
    jobs = MaapUserProfile.objects.filter(user=request.user)
    cron_notify(jobs, dont_wait=True)
    title = 'check cron'
    content = {'title': title,}
    return render(request, 'mainapp/lala.html', content)

def uncheckEmail(request,email,id):
    #call cron method to check & debug
    try:
        user_prof = MaapUserProfile.objects.get(id=int(id))#only new accounts
        if user_prof.enabled == True:
            user_prof.enabled = False
            user_prof.save()
            result = 'successful'
            print(f'uncheck ok')
            return render(request, 'authapp/email_uncheck.html')
            #return JsonResponse({'result': result})
        else:
            result = 'unsuccessful'
            print(f'error uncheck')
            return render(request, 'authapp/email_uncheck.html')
            #return JsonResponse({'result': result})

    except Exception as e:
        print(f'error uncheck user : {e.args}')
        return HttpResponseRedirect(reverse('main'))



def mathem(request, pk):
    title = 'Математика '

    txt0 = None
    txt00 = None

    list_txt = []

    lesson = MaapLesson.objects.get(user=request.user, pk=pk)

    code = 0
    txt2 = ''
    # обработчик обрабватывает все реквесты страницы и GET и POST
    if request.method == 'GET':
        form = Ans_Form()

        hist = json.loads(lesson.hist)  # load hist from db

        a, b, code, hist1 = eval(lesson.mult, lesson.addi, lesson.subt, lesson.divn, lesson.nx, lesson.ny, lesson.ax,
                                 lesson.two_digit, lesson.sx, \
                                 lesson.no_minus, lesson.no_dec_mul, hist, lesson.hist_depth)

        lesson.a1 = a  # update db
        lesson.b1 = b
        lesson.c1 = code
        lesson.hist = json.dumps(hist1)

        t = datetime.now()

        # copy data to db in json format

        tim = {'min': t.minute,
               'sec': t.second}

        js_tim = json.dumps(tim)

        print(js_tim)

        lesson.qst_time = js_tim

        print(f'aha {lesson.qst_time}')

        lesson.save()

        txt1 = f"вопрос {lesson.ans_amount} правильных: {lesson.ans_correct}"

        list_txt.append(txt1)
        #code 1 * 2 + 3 - 4 /
        if code == 1:
            txt2 = f'cколько будет {a} X {b} =?'
        if code == 2:
            txt2 = f'cколько будет {a} + {b} =?'
        if code == 3:
            txt2 = f'cколько будет {a} - {b} =?'
        if code == 4:
            divsign =u'\u00F7';
            txt2 = f'cколько будет {a} {divsign} {b} =?'

        list_txt.append(txt2)

        txt3 = ''  # f'a1={a}, b1={b}, c1={code}'

        qst = {'txt0': txt0, 'txt00': txt00, 'txt1': txt1, 'txt2': txt2, 'txt3': txt3, 'list_txt': list_txt}

        content = {'title': title, 'form': form, 'qst': qst}

        return render(request, 'mainapp/mathem.html', content)

    difference = 0
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
        # ans=cleaned_data.get("answer")
        form = Ans_Form(request.POST)

        if form.is_valid():
            # ans = request.POST.get('answer')
            ans = form.cleaned_data.get("answer")
            val = request.POST.get('tstamp')
            val_li = list(val.split(" "))

            d1 = int(val_li[0]) * 60 + int(val_li[1])  # current time 0 - min 1 - sec

            print(f'post {lesson.qst_time} {val_li}')
            time_dic = json.loads(lesson.qst_time)

            d2 = time_dic['min'] * 60 + time_dic['sec']

            diff = d1 - d2 - 1

            if diff < 0:
                diff = 0
            # print (ans,a,b,code)

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
        # decrease amount of questions as quit was pressed

        lesson.ans_amount -= 1

        lesson.save()
        return HttpResponseRedirect(f'/finish/{lesson.pk}')

@csrf_exempt
def clock_ajax1(request):
    if request.is_ajax():
        post_data = json.loads(request.body)
        state = post_data['state']
        url = f"/clockj/{state['ans_correct']}/{state['ans_amount']}"
        return JsonResponse({
            'success': True,
            'url': url,
        })


def clockj(request,ans_correct=None,ans_amount=None):
    title = 'Часы'

    pk = 1

    if ans_amount == None:
        state = {
            'ans_amount' : 1,
            'ans_correct' : 0
        }
    else:
        state = {
            'ans_amount': ans_amount,
            'ans_correct': ans_correct
        }

    txt1 = f"вопрос {state['ans_amount']} правильных: {state['ans_correct']}"

    txt2 = f'cколько времени на часах ?'

    qst = {'txt1': txt1, 'txt2': txt2}

    content = {'title': title, 'qst': qst, 'pk1': pk, 'state': state }

    return render(request, 'mainapp/clock_test.html', content)

@csrf_exempt
def clock_ajax(request):
    if request.is_ajax():

        # print (request.json())
        # updatedData = json.loads(request.body.decode('UTF-8'))
        post_ans = json.loads(request.body)

        print(post_ans)
        # (pk1 pk2 diff)

        list_txt = []

        # compute diff time

        val = post_ans['time']

        val_li = list(val.split(" "))

        d1 = int(val_li[0]) * 60 + int(val_li[1])  # current time 0 - min 1 - sec

        #print(f'post {lesson.qst_time} {val_li}')

        #time_dic = json.loads(lesson.qst_time)

        #d2 = time_dic['min'] * 60 + time_dic['sec']

        #diff = d1 - d2 - 1

        #if diff < 0:
        #    diff = 0
        state = post_ans['state']

        if (post_ans['cor_time']['hr'] == int(post_ans['ans_time']['hr'])) and (post_ans['cor_time']['min'] == int(post_ans['ans_time']['min'])):
            row1 = f"Oтвет верный, на часах {post_ans['cor_time']['hr']} час, {post_ans['cor_time']['min']} минут"
            state['ans_correct'] = state['ans_correct'] + 1
        else:
            row1 = f"Oтвет НЕ верный, на часах сейчас {post_ans['cor_time']['hr']} час, {post_ans['cor_time']['min']} минут"

        state['ans_amount'] = state['ans_amount'] + 1

        list_txt.append(row1)

        row2 = f"Ответ занял {d1} сек"
        list_txt.append(row2)

        ans = {'list_txt': list_txt}

        content = {'ans': ans, 'pk1': post_ans['pk1'], 'state': state}

        result = render_to_string(
            'mainapp/includes/inc_clockk.html',
            context=content,
            request=request)

        return JsonResponse({'result': result,
                             'ans_correct' : state['ans_correct'],
                             'ans_amount' : state['ans_amount']
                             })




def mathemj(request, pk):
    title = 'Математика '

    txt0 = None
    txt00 = None

    list_txt = []

    lesson = MaapLesson.objects.get(user=request.user, pk=pk)

    code = 0
    txt2 = ''
    # обработчик обрабватывает все реквесты страницы и GET и POST
    if request.method == 'GET':
        form = Ans_Form()

        hist = json.loads(lesson.hist)  # load hist from db

        a, b, code, hist1 = eval(lesson.mult, lesson.addi, lesson.subt, lesson.divn, lesson.nx, lesson.ny, lesson.ax,
                                 lesson.two_digit, lesson.sx, \
                                 lesson.no_minus, lesson.no_dec_mul, hist, lesson.hist_depth)

        lesson.a1 = a  # update db
        lesson.b1 = b
        lesson.c1 = code
        lesson.hist = json.dumps(hist1)

        t = datetime.now()

        # copy data to db in json format

        tim = {'min': t.minute,
               'sec': t.second}

        js_tim = json.dumps(tim)

        print(js_tim)

        lesson.qst_time = js_tim

        print(f'aha {lesson.qst_time}')

        lesson.save()

        txt1 = f"вопрос {lesson.ans_amount} правильных: {lesson.ans_correct}"

        list_txt.append(txt1)
        #code 1 * 2 + 3 - 4 /
        if code == 1:
            txt2 = f'cколько будет {a} X {b} =?'
        if code == 2:
            txt2 = f'cколько будет {a} + {b} =?'
        if code == 3:
            txt2 = f'cколько будет {a} - {b} =?'
        if code == 4:
            divsign =u'\u00F7';
            txt2 = f'cколько будет {a} {divsign} {b} =?'

        list_txt.append(txt2)

        txt3 = ''  # f'a1={a}, b1={b}, c1={code}'

        qst = {'txt0': txt0, 'txt00': txt00, 'txt1': txt1, 'txt2': txt2, 'txt3': txt3, 'list_txt': list_txt}

        content = {'title': title, 'form': form, 'qst': qst, 'pk1' : pk}

        return render(request, 'mainapp/mathem_aj.html', content)

    difference = 0
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
        # ans=cleaned_data.get("answer")
        form = Ans_Form(request.POST)

        if form.is_valid():
            # ans = request.POST.get('answer')
            ans = form.cleaned_data.get("answer")
            val = request.POST.get('tstamp')
            val_li = list(val.split(" "))

            d1 = int(val_li[0]) * 60 + int(val_li[1])  # current time 0 - min 1 - sec

            print(f'post {lesson.qst_time} {val_li}')
            time_dic = json.loads(lesson.qst_time)

            d2 = time_dic['min'] * 60 + time_dic['sec']

            diff = d1 - d2 - 1

            if diff < 0:
                diff = 0
            # print (ans,a,b,code)

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
        # decrease amount of questions as quit was pressed

        lesson.ans_amount -= 1

        lesson.save()
        return HttpResponseRedirect(f'/finish/{lesson.pk}')



#ignore csrf shiled as it gets 403 when you send json as POST
@csrf_exempt
def mathem_ajax(request):
   if request.is_ajax():

       #print (request.json())
       #updatedData = json.loads(request.body.decode('UTF-8'))
       post_ans = json.loads(request.body)

       print (post_ans)
       #(pk1 pk2 diff)

       list_txt = []

       lesson = MaapLesson.objects.get(user=request.user, pk=post_ans['pk1'])

       #compute diff time

       val = post_ans['time']

       val_li = list(val.split(" "))

       d1 = int(val_li[0]) * 60 + int(val_li[1])  # current time 0 - min 1 - sec

       print(f'post {lesson.qst_time} {val_li}')

       time_dic = json.loads(lesson.qst_time)

       d2 = time_dic['min'] * 60 + time_dic['sec']

       diff = d1 - d2 - 1

       if diff < 0:
           diff = 0

       #here


       favor_ans = json.loads(lesson.favor_ans)

       # debug diff +=15
       if diff > lesson.favor_thresold_time:
           already_in = False
           for id, key in favor_ans.items():
               a = key['a']
               b = key['b']
               if lesson.a1 == a and lesson.b1 == b:
                   already_in = True

           if already_in == False:
               elem = {'a': lesson.a1,
                       'b': lesson.b1,
                       'c': lesson.c1,
                       'd': diff}  # a,b,op,diff_time
               # make new index
               idx = 0
               for i in favor_ans.keys():
                   if int(i) > idx:
                       idx = int(i)

               favor_ans[idx + 1] = elem
               # to add to favor_ans
               # store it in db
               lesson.favor_ans = json.dumps(favor_ans)
               # favor_ans.append(elem)

       txt00, check_res = check_ans(int(post_ans['pk2']), lesson.a1, lesson.b1, lesson.c1)

       if check_res == 1:
           lesson.ans_correct += 1
           # update average time
           lesson.ans_sum = lesson.ans_sum + diff
           lesson.avg_ans_time = int(lesson.ans_sum / lesson.ans_correct)
       else:
           try:
               wrong_ans = json.loads(lesson.wrong_ans, object_pairs_hook=OrderedDict)
           except:
               # make first item
               wrong_ans = []
           wrong_ans.append(OrderedDict(a=lesson.a1, b=lesson.b1, c=lesson.c1, diff=int(diff), ans=int(post_ans['pk2'])))
           lesson.wrong_ans = json.dumps(wrong_ans)

       lesson.ans_amount += 1

       lesson.save()

       list_txt.append(txt00)

       txt22 = f"время затраченное на ответ {diff} сек"

       list_txt.append(txt22)

       txt1 = f'a1={lesson.a1}, b1={lesson.b1}, c1={lesson.c1}, ans_num={lesson.ans_amount}, ans_corr={lesson.ans_correct}'
       # add mult table
       if lesson.c1 == 1 and check_res == 0 and lesson.a1 < lesson.nx + 1 and lesson.b1 < lesson.ny + 1:  # if multip in range 10*12
           mult_tabl = []
           ny = lesson.ny
           nx = lesson.nx
           for i in range(1, ny + 1):
               row = []
               for j in range(1, nx + 1):
                   row.append(i * j)
               mult_tabl.append(row)

           # self.printMatrix(self.mult_tabl,0,0,0)
           mul_tab = printMatrix(mult_tabl, lesson.a1 * lesson.b1, lesson.a1, 0)
           cor_ans = lesson.a1 * lesson.b1
           cor_ans = ">" + str(cor_ans)
       else:
           mul_tab = ''
           cor_ans = ''

       ans = {'txt00': txt00, 'txt22': txt22, 'txt1': txt1, 'mul_tab': mul_tab, 'list_txt': list_txt, 'ans': cor_ans}

       content = {'ans': ans, 'pk1' : post_ans['pk1']}

       result = render_to_string(
           'mainapp/includes/inc_mathemk.html',
           context=content,
           request=request)

       return JsonResponse({'result': result})

def mathemk(request, pk1, pk2, diff):
    title = 'главная maap v 1.0/проверка'

    if request.method == 'POST':
        print('clicknext')

        return HttpResponseRedirect(f'/mathem/{pk1}')
    else:  # GET
        # txt0=None
        # txt00=None
        list_txt = []

        lesson = MaapLesson.objects.get(user=request.user, pk=pk1)

        # txt0=f"ваш ответ был {pk}"

        # list_txt.append(txt0)
        # add to dict if diff time > favor_thresold_time:

        favor_ans = json.loads(lesson.favor_ans)

        # debug diff +=15
        if diff > lesson.favor_thresold_time:
            already_in = False
            for id, key in favor_ans.items():
                a = key['a']
                b = key['b']
                if lesson.a1 == a and lesson.b1 == b:
                    already_in = True

            if already_in == False:
                elem = {'a': lesson.a1,
                        'b': lesson.b1,
                        'c': lesson.c1,
                        'd': diff}  # a,b,op,diff_time
                # make new index
                idx = 0
                for i in favor_ans.keys():
                    if int(i) > idx:
                        idx = int(i)

                favor_ans[idx + 1] = elem
                # to add to favor_ans
                # store it in db
                lesson.favor_ans = json.dumps(favor_ans)
                # favor_ans.append(elem)

        txt00, check_res = check_ans(int(pk2), lesson.a1, lesson.b1, lesson.c1)


        if check_res == 1:
            lesson.ans_correct += 1
            #update average time
            lesson.ans_sum = lesson.ans_sum + diff
            lesson.avg_ans_time  = int (lesson.ans_sum  / lesson.ans_correct)
        else:
            try:
                wrong_ans = json.loads(lesson.wrong_ans, object_pairs_hook=OrderedDict)
            except:
                #make first item
                wrong_ans = []
            wrong_ans.append(OrderedDict(a=lesson.a1, b=lesson.b1, c=lesson.c1, diff=int(diff), ans=int(pk2)) )
            lesson.wrong_ans = json.dumps(wrong_ans)


        lesson.ans_amount += 1

        lesson.save()

        list_txt.append(txt00)

        txt22 = f"время затраченное на ответ {diff} сек"

        list_txt.append(txt22)

        txt1 = f'a1={lesson.a1}, b1={lesson.b1}, c1={lesson.c1}, ans_num={lesson.ans_amount}, ans_corr={lesson.ans_correct}'
        # add mult table
        if lesson.c1 == 1 and check_res == 0 and lesson.a1 < lesson.nx+1 and lesson.b1 < lesson.ny+1:  # if multip in range 10*12
            mult_tabl = []
            ny = lesson.ny
            nx = lesson.nx
            for i in range(1, ny + 1):
                row = []
                for j in range(1, nx + 1):
                    row.append(i * j)
                mult_tabl.append(row)

            # self.printMatrix(self.mult_tabl,0,0,0)
            mul_tab = printMatrix(mult_tabl, lesson.a1 * lesson.b1, lesson.a1, 0)
            cor_ans = lesson.a1 * lesson.b1
            cor_ans = ">" + str(cor_ans)
        else:
            mul_tab = ''
            cor_ans = ''

        ans = {'txt00': txt00, 'txt22': txt22, 'txt1': txt1, 'mul_tab': mul_tab, 'list_txt': list_txt, 'ans': cor_ans}

        content = {'title': title, 'ans': ans}

        return render(request, 'mainapp/mathemk.html', content)


def clean_str(str):
    result = ""
    i = 0
    add = False
    while i < len(str):
        # if ord(str[i]) > ord('0') and ord(str[i])<ord('10'):
        if str[i].isdigit():
            result = result + str[i]
            add = True
        else:
            if add:
                result = result + ' '
                add = False
        i = i + 1

    return result


def clear_hist(request):
    #del from where ans_amount < ans_amount
    MaapLesson.objects.filter(user=request.user).delete()

    print(f'{datetime.now()}: {request.user.username} hist deleted, all !')
    return HttpResponseRedirect(f'/')

def clear_hist_5(request, ans_amount = 5):
    #del from where ans_amount < ans_amount
    MaapLesson.objects.filter(user=request.user, ans_amount__lt = ans_amount).delete()

    print(f'{datetime.now()}: {request.user.username} hist deleted, all with ans_amount < {ans_amount}')
    return HttpResponseRedirect(f'/')


def hist(request , page = 'None'):
    title = f'главная maap v 1.0/история уроков '

    print ('page=',page)

    list_hist = []
    rep_hist = []
    wrong_ans_hist = []
    #try to find if its empty
    ans_amount_gt = 10
    lessons = MaapLesson.objects.filter(user=request.user, ans_amount__gt=ans_amount_gt).order_by('id')

    list_hist_row = []

    if not lessons:
        print('no lessons')
        list_hist_row.append(f' пусто! ')
        list_hist_row.append(f' пусто! ')
        list_hist.append(list_hist_row)
        clr_but = False
        max_page = 1
    else:
        # fillup lists with data

        make_report(lessons, list_hist, rep_hist, wrong_ans_hist)

        #paginator self made
        n = 2 #reports per page
        # number of reports all
        items_cnt = len(list_hist) - 1
        # max page
        max_page = int(items_cnt / n)
        #make new page for the rest new page
        if  items_cnt > max_page*n:
            max_page = max_page + 1

        if page == 'None':
            #go to max page
            page = max_page
        else:
            #curr page if page param is given
            page = int(page)




        #no need
        #if max_page == 0:
        #    max_page = 1

        #slice list_hist per one page
        page_list_hist = list_hist[n*page-1:n*page-1+n]
        #make rep_hist, wrong_ans_hist lists corresponding to page_list_hist
        page_rep_hist = []
        page_wrong_ans_hist = []
        for list_item in page_list_hist:
            for rep_item in rep_hist:
                if rep_item[0] == list_item[0]:
                    page_rep_hist.append(rep_item)
            for wrong_ans_item in wrong_ans_hist:
                if wrong_ans_item[0] == list_item[0]:
                    page_wrong_ans_hist.append(wrong_ans_item)

        # page_rep_hist =
        clr_but = True

        paging = {'page':page,
                    'pages': [x for x in range(1,max_page+1) ],
                }

        #copy headers to paged version
        page_rep_hist.insert(0,rep_hist[0])
        page_list_hist.insert(0,list_hist[0])
        page_wrong_ans_hist.insert(0, wrong_ans_hist[0])

        #ans_page = {'list_hist': page_list_hist, 'rep_hist': page_rep_hist, 'wrong_ans_hist': page_wrong_ans_hist, 'clr_but': clr_but , 'paging' : paging}
        #generate tables list & tab_idx
        tables_list=[]

        #make shapka for every entity
        shapka_list_hist = list_hist[0]
        shapka_rep_hist = rep_hist[0]
        shapka_wrong_ans_list = wrong_ans_hist[0]

        #gen combined table from list rep wrong ans lists
        #1st row is list - 6 cols
        #2nd row is rep - 1 col N rows
        #3rd row is wrong ans 1 col N rows
        #+shapka for every entity

        for i in page_list_hist:
            table = []
            table.append(shapka_list_hist)
            table.append(i[:])
            add_shapka = True
            for y in page_rep_hist:
                if y[0] == i[0]:
                    if add_shapka == True:
                        table.append(shapka_rep_hist)
                        add_shapka = False
                    table.append(y[:])

            add_shapka = True
            for y in page_wrong_ans_hist:
                if y[0] == i[0]:
                    if add_shapka == True:
                        table.append(shapka_wrong_ans_list)
                        add_shapka = False
                    table.append(y[:])

            tables_list.append(table)
        #remove first item from tables_list
        del tables_list[0]

        ans_page = {'tab_list': tables_list, 'clr_but': clr_but, 'paging': paging}

        content = {'title': title, 'ans': ans_page}

        return render(request, 'mainapp/hist.html', content)

    ans = {'list_hist': list_hist, 'rep_hist': rep_hist, 'wrong_ans_hist': wrong_ans_hist , 'clr_but': clr_but}
    content = {'title': title, 'ans': ans}
    return render(request, 'mainapp/hist.html', content)

#compares reports - pk previous report, favor_ans current, result : favor_ans_res will be stored in db
def compare_reports(pk, favor_ans):
    try:
        lesson = get_object_or_404(MaapLesson, pk=pk)
    except:
        return favor_ans

    # add report here
    saved_report = lesson.report  # get report connected to pk lesson
    try:
        saved_report.file_rep.open('r')
        bytes_str = saved_report.file_rep.read()
        saved_str = bytes_str.decode()
        saved_report_favor_ans = json.loads(saved_str)
        saved_report.file_rep.close()

        favor_ans_res = {}

        # find the same operation and calculate difference
        for id, key in favor_ans.items():
            a = key['a']
            b = key['b']
            c = key['c']
            d = key['d']
            elem = {'a': a, 'b': b, 'c': c, 'd': d}  # a,b,o
            for id, key in saved_report_favor_ans.items():
                # setup element of dict to be returned
                if a == key['a']:
                    if b == key['b']:
                        if c == key['c']:
                            # same operation found make returned dictionary updated with differnce
                            diff = d - key['d'] #if current is longer then prev - then diff > 0
                            if diff != 0:
                                elem.update(e=diff)
                else: #case when multiplication vice versa operands
                    if a == key['b']:
                        if b == key['a']:
                            if c == 1:
                                diff = d - key['d']  # if current is longer then prev - then diff > 0
                                if diff != 0:
                                    elem.update(e=diff)


            # add new elem to result dict here
            # make new index
            idx = 0
            for i in favor_ans_res.keys():
                if int(i) > idx:
                    idx = int(i)

            favor_ans_res[idx + 1] = elem

        return favor_ans_res

    except:
        return favor_ans


def make_report(lessons, list_hist, rep_hist, wrong_ans_hist):

   # print(list_txt)

    # make headers of the table history
    list_hist_row = []
    list_hist_row.append(f'id')
    list_hist_row.append(f' Дата занятия')
    list_hist_row.append(f' Режим упр.')
    list_hist_row.append(f' Общее время')
    list_hist_row.append(f' Кол-во вопросов')
    list_hist_row.append(f' % Правильных')
    list_hist_row.append(f' Ср. время ответа')
    list_hist.append(list_hist_row)

    # make separate list for report
    rep_hist_row = []
    rep_hist_row.append(f'id')
    rep_hist_row.append(f' Отчет: история трудных ответов ')
    rep_hist.append(rep_hist_row)

    # make separate list for wrong answers
    wrong_ans_row = []
    wrong_ans_row.append(f'id')
    wrong_ans_row.append(f' Отчет: история неверных ответов ')
    wrong_ans_hist.append(wrong_ans_row)


    for i in lessons:
        list_hist_row = []
        # add id lesson
        list_hist_row.append(f'{i.id}')

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

        if (i.avg_ans_time):
            list_hist_row.append(f' {i.avg_ans_time} сек')
        else:
            list_hist_row.append(f' нет данных')

        list_hist.append(list_hist_row)

        # add report here
        saved_report = i.report  # get report connected to i lesson
        try:
            saved_report.file_rep.open('r')
            bytes_str = saved_report.file_rep.read()
            saved_str = bytes_str.decode()
            #saved_report_favor_ans = json.loads(saved_str)
            saved_report.file_rep.close()
            #load dict report as d
            d = json.loads(saved_str)
            saved_report.file_rep.close()
            # use ordereddict to sort report by filed 'd' = time desc direction
            saved_report_favor_ans = OrderedDict(sorted(d.items(), key=lambda t: t[1]['d'], reverse=True))

            # insert id into each row of report
            # add report rows
            for id, key in saved_report_favor_ans.items():
                rep_hist_row = []
                rep_hist_row.append(f'{i.id}')
                a = key['a']
                b = key['b']
                c = key['c']
                d = key['d']
                if c == 1:
                    str_fav_ans = (f' {a} X {b} (={a * b}) занял {d} секунд')
                if c == 2:
                    str_fav_ans = (f' {a} + {b} (={a + b}) занял {d} секунд')
                if c == 3:
                    str_fav_ans = (f' {a} - {b} (={a - b}) занял {d} секунд')
                if c == 4:
                    divsign = u'\u00F7';
                    str_fav_ans = (f' {a} {divsign} {b} (={int (a / b)}) занял {d} секунд')

                diff = key.get('e')
                if diff:
                    if diff > 0:
                        str_fav_ans += f', разница c последним уроком => + {abs(diff)} сек :('
                    else:
                        str_fav_ans += f', разница c последним уроком => - {abs(diff)} сек :)'

                if c:
                    rep_hist_row.append(str_fav_ans)
                    rep_hist.append(rep_hist_row)  # one answer per one row


        except:
            rep_hist_row = []
            rep_hist_row.append(f'{i.id}')
            rep_hist_row.append(f' report - нет данных')
            rep_hist.append(rep_hist_row)

        #wrong ans hist
        try:
            wrong_ans = json.loads(i.wrong_ans, object_pairs_hook=OrderedDict)

            for key in wrong_ans:
                wrong_ans_row = []
                wrong_ans_row.append(f'{i.id}')
                a = key['a']
                b = key['b']
                c = key['c']
                d = key['diff']
                ans = key['ans']

                if c == 1:
                    str_fav_ans = (f' {a} X {b} = {ans} (={a * b}) занял {d} секунд')
                if c == 2:
                    str_fav_ans = (f' {a} + {b} = {ans} (={a + b}) занял {d} секунд')
                if c == 3:
                    str_fav_ans = (f' {a} - {b} = {ans} (={a - b}) занял {d} секунд')
                if c == 4:
                    divsign = u'\u00F7';
                    str_fav_ans = (f' {a} {divsign} {b} = {ans} (={int(a / b)}) занял {d} секунд')

                wrong_ans_row.append(str_fav_ans)
                wrong_ans_hist.append(wrong_ans_row)  # one answer per one row

        except:
            #no items all correct!
            wrong_ans_row = []
            wrong_ans_row.append(f'{i.id}')
            wrong_ans_row.append(f' неверных ответов не обнаружено ')
            wrong_ans_hist.append(wrong_ans_row)





def finish(request, pk):
    title = 'главная maap v 1.0/результаты'

    txt0 = None
    txt00 = None
    # call finish result

    # retrieve lesson from db
    lesson = get_object_or_404(MaapLesson, pk=pk)

    favor_ans = json.loads(lesson.favor_ans)
    # get time for this session
    start_date = json.loads(lesson.s_time)
    end_time = json.loads(lesson.f_time)

    diff_time = int(end_time['sec']) - int(start_date['sec']) + \
                (int(end_time['min']) - int(start_date['min'])) * 60 + \
                (int(end_time['hour']) - int(start_date['hour'])) * 3600

    f_time = int(diff_time / 60)

    #неправилльные ответы
    try:
        wrong_ans = json.loads(lesson.wrong_ans, object_pairs_hook=OrderedDict)
    except:
        # make first item
        wrong_ans = []

    list_txt = finish_lesson(f_time, lesson.ans_amount, lesson.ans_correct, favor_ans, wrong_ans, lesson.favor_thresold_time)

    txt1 = f'ans_num={lesson.ans_amount}, ans_corr={lesson.ans_correct}'

    favor_ans_cmp = compare_reports(pk - 1, favor_ans)  # func is to compare and update last lesson with previous - pk-1

    # make a report with favor_ans for now
    file_name = 'lesson_data.json'
    file_content_string = json.dumps(favor_ans_cmp)
    content_file = ContentFile(file_content_string.encode())
    # generacte filefield
    report = lesson.report

    report.file_rep.save(file_name, content_file)
    report.file_rep.close()

    report.save()



    lesson.save()

    list_hist = []
    rep_hist = []
    wrong_ans_hist = []

    #fillup lists with data

    ans_amount_gt = 4
    lessons = MaapLesson.objects.filter(user=request.user, ans_amount__gt=ans_amount_gt).order_by('id')

    make_report(lessons, list_hist, rep_hist, wrong_ans_hist)

    ans = {'txt0': txt0, 'txt00': txt00, 'txt1': txt1, 'list_txt': list_txt, 'list_hist': list_hist,
           'rep_hist': rep_hist, 'wrong_ans_hist': wrong_ans_hist }

    content = {'title': title, 'ans': ans}
    return render(request, 'mainapp/finish.html', content)
