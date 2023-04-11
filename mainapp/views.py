# Create your views here.
import base64
import json
import random
from collections import OrderedDict
from datetime import datetime
from time import sleep

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from maap.settings import NX, NY, AX, SX, TWO_DIGIT, NO_MINUS, \
    NO_DEC_MUL, HIST_DEPTH, FAVOR_THRESOLD_TIME, OPER_LIST, OPER_LIST1

from authapp.models import MaapUserProfile
from maap.local_settings import PROBE_TEST, START_DATE
from .cron import cron_notify
from .forms import Ans_Form
from .forms import AppModForm
from .models import MaapLesson, MaapReport
from .mul_app import set_app_mode, eval_quest, check_ans, check_ans_drob, \
    get_app_mode_desc, finish_lesson, printMatrix
from .drob import Drob


@login_required
def main(request):
    title = 'главная maap v 1.0'

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
            lesson.mult, lesson.addi, lesson.subt, lesson.divn, lesson.stolbik, \
            lesson.drob, lesson.expr, lesson.drobexpr = set_app_mode(ans)

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
    # links_menu = {}  # ProductCategory.objects.all()

    content = {'title': title, 'form': form_app}

    return render(request, 'mainapp/index.html', content)


def checkCron(request):
    # call cron method to check & debug
    jobs = MaapUserProfile.objects.filter(user=request.user)
    cron_notify(jobs, dont_wait=True)
    title = 'check cron'
    content = {'title': title, }
    return render(request, 'mainapp/lala.html', content)


def uncheckEmail(request, email, id):
    # call cron method to check & debug
    try:
        user_prof = MaapUserProfile.objects.get(id=int(id))  # only new accounts
        if user_prof.enabled:
            user_prof.enabled = False
            user_prof.save()
            result = 'successful'
            print(f'uncheck ok')
            return render(request, 'authapp/email_uncheck.html')
            # return JsonResponse({'result': result})
        else:
            result = 'unsuccessful'
            print(f'error uncheck')
            return render(request, 'authapp/email_uncheck.html')
            # return JsonResponse({'result': result})

    except Exception as e:
        print(f'error uncheck user : {e.args}')
        return HttpResponseRedirect(reverse('main'))


# deprecated moved from mathem-mathemk to mathemj-mathem_ajax question-answer
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

        app_mode = {
            'mult': lesson.mult,
            'addi': lesson.addi,
            'subt': lesson.subt,
            'stolbik': lesson.stolbik,
            'drob': lesson.drob,
        }

        a, b, code, hist1 = eval_quest(lesson.mult, lesson.addi, lesson.subt,
                                       lesson.divn, NX, NY, AX,
                                       TWO_DIGIT, SX, NO_MINUS,
                                       NO_DEC_MUL, hist, HIST_DEPTH, app_mode)

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
        # code 1 * 2 + 3 - 4 /
        if code == 1:
            txt2 = f'cколько будет {a} X {b} =?'
        if code == 2:
            txt2 = f'cколько будет {a} + {b} =?'
        if code == 3:
            txt2 = f'cколько будет {a} - {b} =?'
        if code == 4:
            divsign = u'\u00F7'
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


def clockj(request, ans_correct=None, ans_amount=None):
    title = 'Часы'

    pk = 1

    if ans_amount == None:
        state = {
            'ans_amount': 1,
            'ans_correct': 0,
            'diff': {'hour': 0,
                     'minute': 0
                     }
        }
    else:
        state = {
            'ans_amount': ans_amount,
            'ans_correct': ans_correct,

        }

    txt1 = f"вопрос {state['ans_amount']} правильных: {state['ans_correct']}"

    txt2 = f'cколько времени на часах ?'

    # shuffle for special question with difference
    # flag = False
    # spec_quest_ratio = 30
    # get sected 1 - before 2 exact 3 after
    op = random.randint(1, 3)

    # if op > spec_quest_ratio:
    #    flag = True

    # exact
    if op == 2:
        diff = {'hours': 0,
                'minutes': 0
                }
    # before
    if op == 1:
        mins = [0, 5, 10, 15, 25, 30]
        diff = {'hours': random.randint(1, 2),
                'minutes': random.choice(mins)
                }
        txt2 = f'cколько времени на часах БЫЛО {diff["hours"]} час и {diff["minutes"]} мин НАЗАД??'
        diff['hours'] = -abs(diff['hours'])
        diff['minutes'] = -abs(diff['minutes'])
    # after
    if op == 3:
        mins = [0, 5, 10, 15, 25, 30]
        diff = {'hours': random.randint(1, 2),
                'minutes': random.choice(mins)
                }
        txt2 = f'cколько времени на часах будет через {diff["hours"]} час и {diff["minutes"]} мин??'

    qst = {'txt1': txt1, 'txt2': txt2}

    content = {'title': title, 'qst': qst, 'pk1': pk, 'state': state, 'diff': diff}

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

        # print(f'post {lesson.qst_time} {val_li}')

        # time_dic = json.loads(lesson.qst_time)

        # d2 = time_dic['min'] * 60 + time_dic['sec']

        # diff = d1 - d2 - 1

        # if diff < 0:
        #    diff = 0
        state = post_ans['state']
        # morph parse of russian hour minute
        dct_choice = [
            {'val1': 0, 'val2': 1, 'msg': ''},
            {'val1': 2, 'val2': 4, 'msg': 'А'},
            {'val1': 5, 'val2': 12, 'msg': 'ОВ'},
        ]
        rem_okonch_h = list(filter(lambda x: x['val1'] <= post_ans['cor_time']['hr'] <= x['val2'], dct_choice))

        dct_choice1 = [
            {'val1': 0, 'val2': 0, 'msg': ''},
            {'val1': 1, 'val2': 1, 'msg': 'А'},
            {'val1': 2, 'val2': 4, 'msg': 'Ы'},
            {'val1': 5, 'val2': 9, 'msg': ''},
        ]

        msg_m = ''  # if min in 10-20 - no ending
        # testing post_ans['cor_time']['min'] = 15
        if post_ans['cor_time']['min'] >= 21:
            rem_okonch_m = list(
                filter(lambda x: x['val1'] <= post_ans['cor_time']['min'] % 10 <= x['val2'], dct_choice1))
            msg_m = rem_okonch_m[0]['msg']

        if post_ans['cor_time']['min'] <= 9:
            rem_okonch_m = list(
                filter(lambda x: x['val1'] <= post_ans['cor_time']['min'] % 10 <= x['val2'], dct_choice1))
            msg_m = rem_okonch_m[0]['msg']

        if (post_ans['cor_time']['hr'] == int(post_ans['ans_time']['hr'])) and (
                post_ans['cor_time']['min'] == int(post_ans['ans_time']['min'])):
            row1 = f"Oтвет верный! - {post_ans['cor_time']['hr']} ЧАС{rem_okonch_h[0]['msg']}, {post_ans['cor_time']['min']} МИНУТ{msg_m}"
            state['ans_correct'] = state['ans_correct'] + 1
        else:
            row1 = f"Oтвет НЕ верный, правильный ответ: {post_ans['cor_time']['hr']} ЧАС{rem_okonch_h[0]['msg']}, {post_ans['cor_time']['min']} МИНУТ{msg_m}"

        state['ans_amount'] = state['ans_amount'] + 1

        list_txt.append(row1)

        row2 = f"Ответ занял {d1} сек"
        row2 = f" "
        list_txt.append(row2)

        ans = {'list_txt': list_txt}

        content = {'ans': ans, 'pk1': post_ans['pk1'], 'state': state}

        result = render_to_string(
            'mainapp/includes/inc_clockk.html',
            context=content,
            request=request)

        return JsonResponse({'result': result,
                             'ans_correct': state['ans_correct'],
                             'ans_amount': state['ans_amount']
                             })


@csrf_exempt
def mathemj(request, pk):
    """
    Ф-ия в режиме диалога сетапит вопрос из колоды в случ. порядке
    GET - вывод вопроса
    POST1 - проверка ответа(не для аджакс версии- сейчас работает аджакс - mathem_ajax)
    POST2 - завершение урока
    """
    title = 'Математика '
    print("matemj clicked.. db req..")
    txt0 = None
    txt00 = None

    list_txt = []

    lesson = MaapLesson.objects.get(user=request.user, pk=pk)
    print("matemj db request finished")
    code = 0
    txt2 = ''
    # setup question
    if request.method == 'GET':
        print("question.next")
        form = Ans_Form()
        hist = json.loads(lesson.hist)  # load hist from db

        app_mode = {
            'mult': lesson.mult,
            'addi': lesson.addi,
            'subt': lesson.subt,
            'divn': lesson.divn,
            'stolbik': lesson.stolbik,
            'drob': lesson.drob,
            'expr': lesson.expr,
            'drobexpr': lesson.drobexpr,
        }

        elem, stolbik, drob, expr, drobexpr, hist1 = eval_quest(NX, NY, AX, TWO_DIGIT,
                                                            NO_MINUS, SX, NO_DEC_MUL, hist, HIST_DEPTH, app_mode)
        print(f"eval quest finish a= {elem['a']}, b={elem['b']} code = {elem['c']}")
        # update db
        a = elem['a']
        b = elem['b']
        #additional parameter in case of drob expression
        #a - calculated answer, b - question expression=?, bb1 - correct answer expression
        bb1 = elem.get('b1')
        bb2 = elem.get('b2')
        code = elem['c']

        if expr:
            lesson.is_expr = True
            lesson.a1_expr = json.dumps(a)
            lesson.b1_expr = json.dumps(b)
        elif drob:
            lesson.a1_drob = json.dumps(a)
            lesson.b1_drob = json.dumps(b)
            lesson.is_drob = True
        elif drobexpr:
            lesson.is_drobexpr = True
            lesson.a1_drobexpr = json.dumps(a)
            lesson.b1_drobexpr = json.dumps(b)
            lesson.bb1_drobexpr = json.dumps(bb1)
            lesson.bb2_drobexpr = json.dumps(bb2)
        else:
            lesson.a1 = a
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

        txt1 = f"вопрос {lesson.ans_amount} правильных: {lesson.ans_correct}"

        list_txt.append(txt1)
        # opers = ['X', '+', '-', '/', '=', '!', '#']
        oper = OPER_LIST1[code - 1]

        # maket stolbika for +/-

        stolb1 = stolb2 = ''
        if stolbik:
            if oper == '+' or oper == '-':
                stolb1 = f'''<div class="primer">

                <p class="sup1">{oper}
                    <div class="frac">
                        <span class="top1">{a}</span>
                        <span class="middle1">{b}</span>

                            <div class="ap-otp-inputs" data-length="4">
                                <input class="ap-otp-input" type="tel" maxlength="1" data-index="0">
                                <input class="ap-otp-input" type="tel" maxlength="1" data-index="1">
                                <input class="ap-otp-input" type="tel" maxlength="1" data-index="2">
                                <input class="ap-otp-input" type="tel" maxlength="1" data-index="3">
                            </div>
                    </div>
                </p>  
                </div>
                '''

            if oper == 'X':
                stolb2 = f'''
                <div class="primer">

                <p class="sup1">{oper}
                    <div class="frac">
                        <span class="top1">{a}</span>
                        <span class="middle1">{b}</span>

                            <div class="ap-otp-inputs" data-length="4">
                                <input class="ap-otp-input" type="tel" maxlength="1" data-index="0">
                                <input class="ap-otp-input" type="tel" maxlength="1" data-index="1">
                                <input class="ap-otp-input" type="tel" maxlength="1" data-index="2">
                                <input class="ap-otp-input" type="tel" maxlength="1" data-index="3">
                            </div>

                        <div class="ap-otp-inputs1" data-length="3">
                                <input class="ap-otp-input" type="tel" maxlength="1" data-index="0">
                                <input class="ap-otp-input" type="tel" maxlength="1" data-index="1">
                                <input class="ap-otp-input" type="tel" maxlength="1" data-index="2">

                            </div>

                        <div class="ap-otp-inputs" data-length="4">
                                <input class="ap-otp-input" type="tel" maxlength="1" data-index="0">
                                <input class="ap-otp-input" type="tel" maxlength="1" data-index="1">
                                <input class="ap-otp-input" type="tel" maxlength="1" data-index="2">
                                <input class="ap-otp-input" type="tel" maxlength="1" data-index="3">
                            </div>
                    </div>
                </p>

            </div>
            '''

            a = b = code = 0
            lesson.stolb_cnt += 1

        drob1 = ''
        if drobexpr:
            lesson.drobexpr_cnt += 1
            drob1 = b
            a = b = code = 0

        if drob:
            # a_int = a.get('inte')
            # if a_int == None:
            #     a_int = ''
            # b_int = b.get('inte')
            # if b_int == None:
            #     b_int = ''

            a_int = b_int = ''
            if a['inte'] != 0:
                a_int = a['inte']
            if b['inte'] != 0:
                b_int = b['inte']

            if oper == "=" or oper == "!":
                drob1 = f'''
                            <div class="primer">
                                <p class="sup">{a_int}
                                    <div class="frac">
                                        <span>{a['chis']}</span>
                                        <span class="symbol">/</span>
                                        <span class="bottom">{a['znam']}</span>
                                    </div>
                                </p>

                                <div class="oper">
                                    <span>=</span>
                                </div>

                                <p class="sup">?</p>
                            </div>
                            '''
            else:
                drob1 = f'''
                <div class="primer">
                    <p class="sup">{a_int}
                        <div class="frac">
                            <span>{a['chis']}</span>
                            <span class="symbol">/</span>
                            <span class="bottom">{a['znam']}</span>
                        </div>
                    </p>
    
                    <div class="oper">
                        <span>{oper}</span>
                    </div>
    
                    <p class="sup">{b_int}
                        <div class="frac">
                            <span>{b['chis']}</span>
                            <span class="symbol">/</span>
                            <span class="bottom">{b['znam']}</span>
                        </div>
                    </p>
    
                    <div class="oper">
                        <span>=</span>
                    </div>
    
                    <p class="sup">?</p>
                </div>
                '''
            a = b = code = 0
            lesson.drob_cnt += 1

        # code 1 * 2 + 3 - 4 /
        if code == 1:
            txt2 = f'cколько будет {a} X {b} =?'
            lesson.mult_cnt += 1
        # oper = 'X'
        if code == 2:
            txt2 = f'cколько будет {a} + {b} =?'
            lesson.addi_cnt += 1
        # oper = '+'
        if code == 3:
            txt2 = f'cколько будет {a} - {b} =?'
            lesson.subt_cnt += 1
        # oper = '-'
        if code == 4:
            divsign = u'\u00F7'
            txt2 = f'cколько будет {a} {divsign} {b} =?'
            lesson.divn_cnt += 1
        if code == 7:
            txt2 = f'cколько будет {b} =?'
            lesson.expr_cnt += 1

        list_txt.append(txt2)

        lesson.save()

        txt3 = ''  # f'a1={a}, b1={b}, c1={code}'

        qst = {'txt0': txt0, 'txt00': txt00, 'txt1': txt1, 'txt2': txt2, 'txt3': txt3,
               'list_txt': list_txt, 'stolb1': stolb1, 'stolb2': stolb2, 'drob1': drob1, 'expr': expr}

        content = {'title': title, 'form': form, 'qst': qst, 'pk1': pk}

        return render(request, 'mainapp/mathem_aj.html', content)

    difference = 0
    # in case answer pressed
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

    # in case of finish key pressed
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


# ignore csrf shiled as it gets 403 when you send json as POST
@csrf_exempt
def mathem_ajax(request):
    if request.is_ajax():

        # print (request.json())
        # updatedData = json.loads(request.body.decode('UTF-8'))
        post_ans = json.loads(request.body)

        print(post_ans)
        # (pk1 pk2 diff)

        list_txt = []

        lesson = MaapLesson.objects.get(user=request.user, pk=int(post_ans['pk1']))

        # compute diff time

        val = post_ans['time']

        val_li = list(val.split(" "))

        d1 = int(val_li[0]) * 60 + int(val_li[1])  # current time 0 - min 1 - sec

        print(f'post {lesson.qst_time} {val_li}')

        time_dic = json.loads(lesson.qst_time)

        d2 = time_dic['min'] * 60 + time_dic['sec']

        diff = d1 - d2 - 1

        if diff < 0:
            diff = 0

        # here

        favor_ans = json.loads(lesson.favor_ans)

        # debug diff +=15
        if diff > FAVOR_THRESOLD_TIME:
            already_in = False
            for _, key in favor_ans.items():
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
        # если приходит '' как pk2
        pk2_chr = post_ans['pk2']
        if pk2_chr == '':
            ans = 0
        else:
            ans = pk2_chr

        c1 = lesson.c1

        txt00 = ''
        check_res = 0
        drob_txt = ''
        if lesson.is_expr:
            a1 = json.loads(lesson.a1_expr)
            b1 = json.loads(lesson.b1_expr)
            lesson.is_expr = False
            if int(ans) == int(a1):
                txt00 = f" ответ - правильный! {b1} = {a1}"
                check_res = 1
            else:
                txt00 = f" ответ - не верный! {b1} = {a1}"
        elif lesson.is_drob:
            a1 = json.loads(lesson.a1_drob)
            b1 = json.loads(lesson.b1_drob)
            drob_txt, check_res = check_ans_drob(ans, a1, b1, c1)
            if check_res == 1:
                txt00 = f" ответ - правильный "
            else:
                txt00 = f" ответ - не верный "
            lesson.is_drob = False
        elif lesson.is_drobexpr:
            #a1 calculated answer, bb1 drob expression with answer
            #bb2 drob expression in text form for report (gets to b1)
            a1 = json.loads(lesson.a1_drobexpr)
            b1 = json.loads(lesson.bb2_drobexpr)
            bb1 = json.loads(lesson.bb1_drobexpr)
            drob_txt = bb1

            ans = ans.strip()
            ans = ans.split()
            a1 = a1.strip()
            a1 = a1.split()

            #case when answer is only inte without drob
            #or only drob chast
            if len(a1) == 1 and len(ans) == 1:
                if a1[0] == ans[0]:
                    check_res = 1
            else:
                #case when inte = 0
                if a1[0] == '0':
                    #check second part only
                    if a1[1] == ans[0]:
                        check_res = 1
                else:
                    #case 1 0/0
                    if a1[1] == '0/0':
                        #remove a1 from list
                        a1.pop()
                    if len(a1) == len(ans):
                        #check whole drob inte and drob parts
                        if a1[0] == ans[0] and a1[1] == ans[1]:
                            check_res = 1

            if check_res == 1:
                txt00 = f" ответ - правильный "
            else:
                txt00 = f" ответ - не верный "
            lesson.is_drobexpr = False
        else:
            a1 = lesson.a1
            b1 = lesson.b1

            txt00, check_res = check_ans(int(ans), a1, b1, c1)

        lesson.ans_amount = lesson.ans_amount + 1

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
                pk2_chr = post_ans['pk2']
                if pk2_chr == '':
                    ans = 0
                else:
                    ans = pk2_chr
            wrong_ans.append(
                OrderedDict(a=a1, b=b1, c=c1, diff=int(diff), ans=ans))
            lesson.wrong_ans = json.dumps(wrong_ans)

        lesson.save()

        list_txt.append(txt00)

        txt22 = f"время, затраченное на ответ: {diff} сек"

        list_txt.append(txt22)

        txt1 = f'a1={a1}, b1={b1}, c1={c1}, ans_num={lesson.ans_amount}, ans_corr={lesson.ans_correct}'

        mul_tab = ''
        cor_ans = ''
        if not lesson.drob:
            # add mult table
            if lesson.c1 == 1 and check_res == 0 and lesson.a1 < NX + 1 and lesson.b1 < NY + 1:  # if multip in range 10*12
                mult_tabl = []
                ny = NY
                nx = NX
                for i in range(1, ny + 1):
                    row = []
                    for j in range(1, nx + 1):
                        row.append(i * j)
                    mult_tabl.append(row)

                # self.printMatrix(self.mult_tabl,0,0,0)
                mul_tab = printMatrix(mult_tabl, lesson.a1 * lesson.b1, lesson.a1, 0)
                cor_ans = lesson.a1 * lesson.b1
                cor_ans = ">" + str(cor_ans)
        # txt1 = ''
        ans = {'txt00': txt00, 'txt22': txt22, 'txt1': txt1, 'mul_tab': mul_tab, 'drob': drob_txt, 'list_txt': list_txt,
               'ans': cor_ans, }

        content = {'ans': ans, 'pk1': post_ans['pk1']}

        result = render_to_string(
            'mainapp/includes/inc_mathemk.html',
            context=content,
            request=request)

        return JsonResponse({'result': result})


# deprecated moved from mathem-mathemk to mathemj-mathem_ajax question-answer
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
        if diff > FAVOR_THRESOLD_TIME:
            already_in = False
            for _, key in favor_ans.items():
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
            # update average time
            lesson.ans_sum = lesson.ans_sum + diff
            lesson.avg_ans_time = int(lesson.ans_sum / lesson.ans_correct)
        else:
            try:
                wrong_ans = json.loads(lesson.wrong_ans, object_pairs_hook=OrderedDict)
            except:
                # make first item
                wrong_ans = []
            wrong_ans.append(OrderedDict(a=lesson.a1, b=lesson.b1, c=lesson.c1, diff=int(diff), ans=int(pk2)))
            lesson.wrong_ans = json.dumps(wrong_ans)

        lesson.ans_amount += 1

        lesson.save()

        list_txt.append(txt00)

        txt22 = f"время затраченное на ответ {diff} сек"

        list_txt.append(txt22)

        txt1 = f'a1={lesson.a1}, b1={lesson.b1}, c1={lesson.c1}, ans_num={lesson.ans_amount}, ans_corr={lesson.ans_correct}'
        # add mult table
        if lesson.c1 == 1 and check_res == 0 and lesson.a1 < NX + 1 and lesson.b1 < NY + 1:  # if multip in range 10*12
            mult_tabl = []
            ny = NY
            nx = NX
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
    # del from where ans_amount < ans_amount
    MaapLesson.objects.filter(user=request.user).delete()

    print(f'{datetime.now()}: {request.user.username} hist deleted, all !')
    return HttpResponseRedirect(f'/')


def clear_hist_5(request, ans_amount=5):
    # del from where ans_amount < ans_amount
    MaapLesson.objects.filter(user=request.user, ans_amount__lt=ans_amount).delete()

    print(f'{datetime.now()}: {request.user.username} hist deleted, all with ans_amount < {ans_amount}')
    return HttpResponseRedirect(f'/')


def hist(request, page='None'):
    title = f'главная maap v 1.0/история уроков '

    print('page=', page)

    list_hist = []
    rep_hist = []
    wrong_ans_hist = []
    # try to find if its empty
    # minimum amount of answer to listed in reports
    ans_amount_gt = 6
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

        # paginator self made
        n = 3  # reports per page
        # number of reports all
        items_cnt = len(lessons) - 1
        # max page
        max_page = int(items_cnt / n)
        # make new page for the rest new page
        if items_cnt > max_page * n:
            max_page = max_page + 1

        if page == 'None':
            # go to max page
            page = max_page
        else:
            # curr page if page param is given
            page = int(page)

        # calc start lesson on this page
        lesson_id = n * page - 1
        # get from db only what we need for this page
        make_report(lessons, lesson_id, n, list_hist, rep_hist, wrong_ans_hist)

        page_list_hist = list_hist
        page_rep_hist = rep_hist
        page_wrong_ans_hist = wrong_ans_hist

        # # slice list_hist per one page
        # page_list_hist = list_hist   #[n * page - 1:n * page - 1 + n]
        # # make rep_hist, wrong_ans_hist lists corresponding to page_list_hist
        # page_rep_hist = []
        # page_wrong_ans_hist = []
        # for list_item in page_list_hist:
        #     for rep_item in rep_hist:
        #         if rep_item[0] == list_item[0]:
        #             page_rep_hist.append(rep_item)
        #     for wrong_ans_item in wrong_ans_hist:
        #         if wrong_ans_item[0] == list_item[0]:
        #             page_wrong_ans_hist.append(wrong_ans_item)
        #
        # # page_rep_hist =
        #
        #
        # # copy headers to paged version
        # page_rep_hist.insert(0, rep_hist[0])
        # page_list_hist.insert(0, list_hist[0])
        # page_wrong_ans_hist.insert(0, wrong_ans_hist[0])

        # ans_page = {'list_hist': page_list_hist, 'rep_hist': page_rep_hist, 'wrong_ans_hist': page_wrong_ans_hist, 'clr_but': clr_but , 'paging' : paging}
        # generate tables list & tab_idx
        tables_list = []

        # make shapka for every entity
        shapka_list_hist = list_hist[0]
        shapka_rep_hist = rep_hist[0]
        shapka_wrong_ans_list = wrong_ans_hist[0]

        # gen combined table from list rep wrong ans lists
        # 1st row is list - 6 cols
        # 2nd row is rep - 1 col N rows
        # 3rd row is wrong ans 1 col N rows
        # insert shapka for every entity (initially its only in the begining

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
        # remove first item from tables_list
        del tables_list[0]

        clr_but = True

        paging = {'page': page,
                  'pages': [x for x in range(1, max_page + 1)],
                  }

        ans_page = {'tab_list': tables_list, 'clr_but': clr_but, 'paging': paging}

        content = {'title': title, 'ans': ans_page}

        return render(request, 'mainapp/hist.html', content)

    ans = {'list_hist': list_hist, 'rep_hist': rep_hist, 'wrong_ans_hist': wrong_ans_hist, 'clr_but': clr_but}
    content = {'title': title, 'ans': ans}
    return render(request, 'mainapp/hist.html', content)


# compares reports - pk previous report, favor_ans current, result : favor_ans_res will be stored in db
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
                            diff = d - key['d']  # if current is longer then prev - then diff > 0
                            if diff != 0:
                                elem.update(e=diff)
                else:  # case when multiplication vice versa operands
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
    except Exception as e:
        print("compare reports error: ", e)
        return favor_ans


def print_report_row(key):
    a = key['a']
    b = key['b']
    c = key['c']
    d = key['d']
    str_fav_ans = ''
    divsign = u'\u00F7'

    oper = OPER_LIST[c - 1]
    if not isinstance(a, int):
        a_inte = ''
        if a.get('inte'):
            a_inte = a['inte']
        drob_a = f"{a_inte} {a['chis']}/{a['znam']}"

        if oper == '=' or oper == '/=':
            str_fav_ans = (f"""{drob_a} {oper} {d} сек""")
        # a,b drob
        else:
            b_inte = ''
            if b.get('inte'):
                b_inte = b['inte']
            drob_b = f"{b_inte} {b['chis']}/{b['znam']}"

            str_fav_ans = f""" {drob_a} {oper} {drob_b} занял {d} сек"""
    else:
        # a,b integer
        if c == 1:
            str_fav_ans = f' {a} X {b} (={a * b}) занял {d} секунд'
        if c == 2:
            str_fav_ans = f' {a} + {b} (={a + b}) занял {d} секунд'
        if c == 3:
            str_fav_ans = f' {a} - {b} (={a - b}) занял {d} секунд'
        if c == 4:
            divsign = u'\u00F7'
            str_fav_ans = f' {a} {divsign} {b} (={int(a / b)}) занял {d} секунд'

    diff = key.get('e')
    if diff:
        if diff > 0:
            str_fav_ans += f', разница c последним уроком => + {abs(diff)} сек :('
        else:
            str_fav_ans += f', разница c последним уроком => - {abs(diff)} сек :)'
    return str_fav_ans


def print_wrong_report_row(key):
    a = key['a']
    b = key['b']
    c = key['c']
    d = key.get('diff')
    ans = key.get('ans')

    str_fav_ans = ''
    divsign = u'\u00F7'
    # oper_list = ['X', '+', '-', divsign, '=', '=', '#']
    oper = OPER_LIST[c - 1]
    if not isinstance(a, int):
        if c == 8:
            if a[0] == '0':
                a.pop(0)
            elif a[1] == '0/0':
                    a.pop()
            str_fav_ans = f" др.выр: {b} {' '.join(a)}  ( отв. = {' '.join(ans)} ) (занял {d} секунд)"
        elif oper == '#':
            str_fav_ans = f' выр: {b} = {a}  ( отв. = {ans} ) (занял {d} секунд)'
        else:
            # ans_inte = ''
            # if ans.get('inte') != None:
            #    ans_inte = ans['inte']
            drob_ans = f" {ans}"  # //{ans_inte} {ans['chis']}/{ans['znam']}"
            a_inte = ''
            if a.get('inte'):
                a_inte = a['inte']
            drob_a = f"{a_inte} {a['chis']}/{a['znam']}"

            if oper == '=' or oper == '/=':
                str_fav_ans = f"""{drob_a} {oper} {drob_ans} (занял {d} сек)"""
            # a,b drob
            else:
                b_inte = ''
                if b.get('inte'):
                    b_inte = b['inte']
                drob_b = f"{b_inte} {b['chis']}/{b['znam']}"
                str_fav_ans = f""" {drob_a} {oper} {drob_b} {drob_ans} (занял {d} сек)"""
    else:
        # a,b integer
        if c == 1:
            str_fav_ans = f' {a} X {b} (={a * b}) {ans} (занял {d} секунд)'
        if c == 2:
            str_fav_ans = f' {a} + {b} (={a + b}) {ans} (занял {d} секунд)'
        if c == 3:
            str_fav_ans = f' {a} - {b} (={a - b}) {ans} (занял {d} секунд)'
        if c == 4:
            divsign = u'\u00F7'
            str_fav_ans = f' {a} {divsign} {b} (={int(a / b)}) {ans} (занял {d} секунд)'

    return str_fav_ans


def make_report(lessons, lesson_id, n, list_hist, rep_hist, wrong_ans_hist):
    # print(list_txt)

    # make headers of the table history
    list_hist_row = []
    list_hist_row.append(f'id')
    list_hist_row.append(f' Дата занятия')
    list_hist_row.append(f' Режим упр. (Кол-во)')
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

    for i in lessons[lesson_id - 1:lesson_id - 1 + n]:
        list_hist_row = []
        # add id lesson
        list_hist_row.append(f'{i.id}')

        # tab date start dATE time
        start_date = json.loads(i.s_time)
        new_date = start_date['day'] + '.' + start_date['mon'] + '.' + start_date['year']
        new_time = start_date['hour'] + ':' + start_date['min'] + ':' + start_date['sec']

        list_hist_row.append(f'{new_date} {new_time}')
        # tab mode + description amount of each ops questions
        # a = str(
        #    i.mode)  # when only one char from db it assumes digital as int so we need to explicitly change it to str again!
        list_hist_row.append(get_app_mode_desc(i))

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
            # saved_report_favor_ans = json.loads(saved_str)
            saved_report.file_rep.close()
            # load dict report as d from saved str
            d = json.loads(saved_str)
            saved_report.file_rep.close()
            # use ordereddict to sort report by filed 'd' = time desc direction
            saved_report_favor_ans = OrderedDict(sorted(d.items(), key=lambda t: t[1]['d'], reverse=True))
            # insert id into each row of report
            # add report rows

            for id, key in saved_report_favor_ans.items():
                rep_hist_row = [f'{i.id}']
                str_fav_ans = print_report_row(key)
                # if key.get('c'):
                rep_hist_row.append(str_fav_ans)
                rep_hist.append(rep_hist_row)  # one answer per one row

        except Exception as e:
            rep_hist_row = []
            rep_hist_row.append(f'{i.id}')
            rep_hist_row.append(f' report - нет данных error: {e}')
            rep_hist.append(rep_hist_row)

        # wrong ans hist
        try:
            if i.wrong_ans != '':
                wrong_ans = json.loads(i.wrong_ans, object_pairs_hook=OrderedDict)

                for key in wrong_ans:
                    wrong_ans_row = []
                    wrong_ans_row.append(f'{i.id}')

                    str_fav_ans = print_wrong_report_row(key)

                    wrong_ans_row.append(str_fav_ans)
                    wrong_ans_hist.append(wrong_ans_row)  # one answer per one row
            else:
                wrong_ans_row = []
                wrong_ans_row.append(f'{i.id}')
                wrong_ans_row.append(f' неверных ответов не обнаружено ')
                wrong_ans_hist.append(wrong_ans_row)


        except Exception as e:
            # no items all correct!
            wrong_ans_row = []
            wrong_ans_row.append(f'{i.id}')
            wrong_ans_row.append(f' неверных ответов не обнаружено error: {e}, {i.wrong_ans}')
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

    # неправилльные ответы
    try:
        wrong_ans = json.loads(lesson.wrong_ans, object_pairs_hook=OrderedDict)
    except:
        # make first item
        wrong_ans = []

    list_txt = finish_lesson(lesson, f_time, favor_ans, wrong_ans, FAVOR_THRESOLD_TIME)

    txt1 = f'ans_num={lesson.ans_amount}, ans_corr={lesson.ans_correct}'

    favor_ans_cmp = compare_reports(pk - 1, favor_ans)  # func is to compare and update last lesson with previous - pk-1

    # make a report with favor_ans for now
    file_name = 'lesson_data.json'
    file_content_string = json.dumps(favor_ans_cmp)
    content_file = ContentFile(file_content_string.encode())
    # generate filefield
    report = lesson.report
    report.file_rep.save(file_name, content_file)
    report.file_rep.close()

    report.save()
    lesson.save()

    list_hist = []
    rep_hist = []
    wrong_ans_hist = []

    # #fillup lists with data
    #
    # ans_amount_gt = 4
    # lessons = MaapLesson.objects.filter(user=request.user, ans_amount__gt=ans_amount_gt).order_by('id')
    #
    # make_report(lessons, list_hist, rep_hist, wrong_ans_hist)

    ans = {'txt0': txt0, 'txt00': txt00, 'txt1': txt1, 'list_txt': list_txt, 'list_hist': list_hist,
           'rep_hist': rep_hist, 'wrong_ans_hist': wrong_ans_hist}

    content = {'title': title, 'ans': ans}

    return render(request, 'mainapp/finish.html', content)

# function which check availbility from kubernetes probe
# :8000/__heartbeat__
#
def checkHeartBeat(request):
    if request.method == 'GET':

        if PROBE_TEST == 1:
            CURR = datetime.now()
            td = (CURR - START_DATE).seconds
            if td > 180 and td < 460:
                print(f'st = {START_DATE}, curr = {CURR}, td = {td}, probe test {PROBE_TEST}, status=500')
                sleep(5)
                return HttpResponse(status=500)
        print('Probetest=', PROBE_TEST, 'status=200')
        return HttpResponse(status=200)
    return HttpResponse(status=200)
