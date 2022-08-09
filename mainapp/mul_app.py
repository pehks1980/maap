"""
mul_app модуль для вычислений примеров
"""
import random

from maap.settings import OPER_LIST1
from .drob import *


def bubble_sort(source_arr):
    """
    улучшение - используем флаг замены. если была хоть 1 замена вылетаем из цикла.
    в итоге время сортировки зависит от количества замен
    :rtype: object
    """
    zam = True
    n = 0
    while zam:
        # print(source_arr,"сч-ик замен ",n)
        zam = False
        for i in range(0, len(source_arr) - 1):
            if source_arr[i] > source_arr[i + 1]:
                tmp = source_arr[i + 1]
                source_arr[i + 1] = source_arr[i]
                source_arr[i] = tmp
                zam = True
                n += 1
                break

        if not zam:
            break

    return source_arr, n


def set_app_mode(list_mode):
    """
    set app mode for app
    :param list_mode:
    :return:
    """
    mult = 0
    addi = 0
    subt = 0
    divn = 0
    stolbik = 0
    drob = 0
    expr = 0

    for i in list_mode:
        if int(i) == 1:
            mult = 1
        if int(i) == 2:
            addi = 1
        if int(i) == 3:
            subt = 1
        if int(i) == 4:
            divn = 1
        if int(i) == 5:
            stolbik = 1
        if int(i) == 6:
            drob = 1
        if int(i) == 7:
            expr = 1

    return mult, addi, subt, divn, stolbik, drob, expr


def get_app_mode_desc(lesson):
    """
    get current app mode
    :param lesson:
    :return:
    """
    mode = lesson.mode
    mult_cnt = lesson.mult_cnt
    addi_cnt = lesson.addi_cnt
    subt_cnt = lesson.subt_cnt
    divn_cnt = lesson.divn_cnt
    stolb_cnt = lesson.stolb_cnt
    drob_cnt = lesson.drob_cnt
    expr_cnt = lesson.expr_cnt

    a = b = c = d = e = f = g = ''

    for i in mode:
        if i == '1':
            a = '*'
            if mult_cnt:
                a += f'={mult_cnt}'
        if i == '2':
            b = ' +'
            if addi_cnt:
                b += f'={addi_cnt}'
        if i == '3':
            c = ' -'
            if subt_cnt:
                c += f'={subt_cnt}'
        if i == '4':
            divsign = u'\u00F7'
            d = f' {divsign}'
            if divn_cnt:
                d += f'={divn_cnt}'
        if i == '5':
            e = f' ст.'
            if stolb_cnt:
                e += f'={stolb_cnt}'
        if i == '6':
            f = f' др.'
            if drob_cnt:
                f += f'={drob_cnt}'
        if i == '7':
            g = f' выр.'
            if expr_cnt:
                g += f'={expr_cnt}'

    return f'{a}{b}{c}{d}{e}{f}{g}'


def printMatrix(s, hl, a, b):
    """
    Do heading
    :param s:
    :param hl:
    :param a:
    :param b:
    :return:
    """
    result = []
    row = [" "]
    for j in range(len(s[0])):
        row.append(j + 1)

    result.append(row)

    # Matrix contents
    for i in range(len(s)):
        row = []
        row.append(i + 1)  # Row nums
        for j in range(len(s[0])):
            if hl == s[i][j]:
                if j == (a - 1):
                    row.append(">" + str(s[i][j]))
                else:
                    row.append(s[i][j])
            else:
                row.append(s[i][j])
        result.append(row)

    # print(result)
    return result


def get_ops(same_znam, DROBI_PLUS_SET):
    # если оба включены то, генерим с
    sub_choice = random.randint(0, 1)
    # генерит операнды с одним знаменателем
    if same_znam is True and sub_choice == 1:
        znam = random.randint(3, 25)
        chis_a = random.randint(1, int(znam / 2) + 1)
        chis_b = random.randint(1, int(znam / 2))
        a = {'chis': chis_a,
             'znam': znam,
             'inte': 0
             }
        b = {'chis': chis_b,
             'znam': znam,
             'inte': 0
             }
    else:
        # выьрка операндов из таблицы
        a = random.choice(DROBI_PLUS_SET)
        b = random.choice(DROBI_PLUS_SET)
    return a, b


def eval_quest(nx, ny, ax, two_digit, no_minus, sx, no_dec_mul, hist, hist_depth, app_mode):
    """
    choice the next question from random, take into account previous answers hist
    :param nx:
    :param ny:
    :param ax:
    :param two_digit:
    :param sx:
    :param no_minus:
    :param no_dec_mul:
    :param hist:
    :param hist_depth:
    :return:
    """
    code = None
    a = 0
    b = 0
    # param sets upper range for +,- questions operands
    up_range = 80
    # param sets minimum diff b/w operands to avoid  such 34+1 questions like
    range_diff = 7

    stolbik = False
    drob = False
    expr = False

    while True:
        already_in_hist = False
        # choice type of question *-+/ if code is not chosen already
        if code is None:
            while True:
                stolbik = False
                drob = False
                expr = False

                code = random.randint(1, 7)
                if (app_mode['mult'] == 1) and (code == 1):
                    break
                if (app_mode['addi'] == 1) and (code == 2):
                    break
                if (app_mode['subt'] == 1) and (code == 3):
                    break
                if (app_mode['divn'] == 1) and (code == 4):
                    break
                if (app_mode['stolbik'] == 1) and (code == 5):
                    break
                if (app_mode['drob'] == 1) and (code == 6):
                    break
                if (app_mode['expr'] == 1) and (code == 7):
                    break

        # mul a,b 2..10 2..12 mult table 10X12
        if code == 1:
            # mul op
            mul_op_ratio = 10
            op = random.randint(1, 100)
            if op > mul_op_ratio:
                a = random.randint(2, nx)
                b = random.randint(2, ny)
            else:  # a*10,100,100
                digs = [10 ** x for x in range(1, 4)]
                a = random.randint(2, ny * nx)
                b = random.choice(digs)

        # +
        if code == 2:
            if random.randint(0, 3) == 3:
                # 25% prob rate 100-200  div 2
                a = random.randint(10, 20) * 10
                b = random.randint(10, ax - 20)
            else:
                while True:
                    a = random.randint(1, ax)
                    b = random.randint(1, ax)

                    if two_digit:
                        if a > up_range > b:
                            if abs(a - b) > range_diff:
                                break
                        else:
                            if b > up_range > a:
                                if abs(a - b) > range_diff:
                                    break
                        continue

        # -
        if code == 3:
            print(f'вычитание {sx}')
            two_digit = True
            while True:
                a = random.randint(1, sx)
                b = random.randint(1, sx)

                if two_digit:
                    if a > up_range and b < up_range and abs(a - b) > range_diff:
                        break
                    else:
                        if b > up_range and a < up_range and abs(a - b) > range_diff:
                            break

            if no_minus:
                if a < b:
                    tmp = a  # swap it so there is no minus
                    a = b
                    b = tmp
                    # a, b = b, a

            # if no_dec_mul:  # no 10s in multiplication
            #     if (a == 10) or (b == 10):
            #         already_in_hist = True
            #         continue

        # div on multiple table:
        if code == 4:
            if random.randint(0, 1) == 0:
                # 25% prob rate 100-200  div 2
                a = random.randint(10, 20) * 10 + random.randint(0, 4) * 2
                b = 2
            else:
                # mul table div 72 div 8
                ops = [random.randint(2, nx), random.randint(2, ny)]
                a1 = ops[0]
                b1 = ops[1]
                a = a1 * b1
                b = random.choice(ops)

        # check if we go these already
        for _, key in hist.items():
            ha = key['a']
            hb = key['b']
            hcode = key['c']
            if a == ha and b == hb and code == hcode:
                already_in_hist = True

        # v stolbik
        if code == 5:
            stolbik = True
            #     # chose 0 - + 1 - - 2 *
            oper = random.randint(0, 2)

            # oper = ''
            # while True:
            #     # chose 0 - + 1 - - 2 *
            #     oper = random.randint(0, 2)
            #     if (app_mode['mult'] == 1) and (oper == 2):
            #         break
            #     if (app_mode['addi'] == 1) and (oper == 1):
            #         break
            #     if (app_mode['subt'] == 1) and (oper == 0):
            #         break
            #     if app_mode['divn'] == 1:
            #         break
            #     if (app_mode['divn'] == 0) and (app_mode['mult'] == 0) and (app_mode['subt'] == 0) and (
            #             app_mode['addi'] == 0):
            #         break

            # -
            if oper == 0:
                a = random.randint(99, 999)
                b = random.randint(19, 99)
                code = 3
            # +
            if oper == 1:
                a = random.randint(99, 9999)
                b = random.randint(99, 4999)
                if a + b > 9999:
                    a = random.randint(99, 4999)
                code = 2
            # *
            if oper == 2:
                a = random.randint(10, 99)
                b = random.randint(10, 99)
                code = 1

        # drob
        if code == 6:
            drob = True
            # rule for generating a and b
            # in this case выбор будет рандомный либо с таким же знаменателм либо из таблицы
            same_znam = True
            #set_choice = True

            # chose 1=* 2=+ 3=- 4=/(div) 5= denormalize 6 - ! normalize
            # селектор операций - разрешает возможность выбора какой либо операции
            oper_set = (1, 2, 3, 4, 5, 6)
            oper = random.choice(oper_set)

            # oper = 1
            # drobi!!

            # we get code == 6 oper = operation
            # now we have to choose a,b - operands
            # *
            if oper == 1:
                a, b = get_ops(False, DROBI_MULT_SET)
            # +
            if oper == 2:
                a, b = get_ops(same_znam, DROBI_PLUS_SET)
            # -
            if oper == 3:
                a, b = get_ops(same_znam, DROBI_MINUS_SET)
                # check and exchange ops to avoid negative results in primer (for simplicity)
                if a['chis'] / a['znam'] < b['chis'] / b['znam']:
                    a, b = b, a
            # /
            if oper == 4:
                a, b = get_ops(False, DROBI_MULT_SET)
            # =
            if oper == 5 or oper == 6:
                # rnd choose type of fraction to transform
                chis = random.randint(1, 6)
                znam = random.randint(1, 6)
                if chis > znam:
                    tmp = chis
                    chis = znam
                    znam = tmp
                if chis == znam:
                    znam += random.randint(1, 6)
                # chis must be > znam
                a = {'chis': chis,
                     'znam': znam,
                     'inte': random.randint(1, 4)
                     }
                d1 = Drob(chis=a['chis'], znam=a['znam'], inte=a['inte'])
                print(d1)
                if oper == 5:
                    # denormalize drob ie 12 / 5 = 2 2/5
                    d1.denormalize()
                if oper == 6:
                    pass

                a = {'chis': d1.chis,
                     'znam': d1.znam,
                     'inte': d1.inte
                     }

                b = {'chis': 0,
                     'znam': 0,
                     'inte': 0,
                     }
                print(a)

            # in case of drob = true code is operation +-/*=
            code = oper

        # expr
        if code == 7:
            expr = True
            # 34 + ( 239 - 606 : 6 ) * 4 - 393 : 3 =
            # ex = a [ -+] br_rez [*:] c [+-] d [*:] e
            # b = a1 op1[-+] b1 op2[*:] c1
            expr_brackets_rezult = 0
            expr_brackets_rezult_str = '( '
            # make up and compute brackets expression

            a1 = random.randint(69, 149)
            expr_brackets_rezult_str += str(a1)

            op2 = random.choice(['*', ':'])
            if op2 == '*':
                c1 = random.randint(2, 5)
                b1 = random.randint(2, 25)
                expr_brackets_rezult = c1 * b1

            if op2 == ':':
                c1 = random.randint(2, 8)
                # for chosen divider find integer rest with
                while True:
                    b1 = random.randint(99, 199)
                    if b1 % c1 == 0:
                        break
                expr_brackets_rezult = b1 / c1
            expr_brackets_rezult_str_1 = str(b1) + " " + op2 + " " + str(c1)
            op1 = random.choice(['-', '+'])
            if op1 == '-':
                expr_brackets_rezult = int(a1 - expr_brackets_rezult)
            if op1 == '+':
                expr_brackets_rezult = int(a1 + expr_brackets_rezult)
            expr_brackets_rezult_str += " " + op1 + " " + expr_brackets_rezult_str_1 + " )"

            # do same as per outer expr
            # 34 + ( 239 - 606 : 6 ) * 4 - 393 : 3 =
            # ex = a op1[ -+] br_rez op2[ *] c op3[ +-] d op4[ *:] e
            expr_rezult = 0
            expr_rezult_op4_str = ' '
            op4 = random.choice(['', '*', ":"])
            if op4 == '*':
                d = random.randint(2, 6)
                e = random.randint(2, 39)
                expr_rezult_op4 = d * e
                expr_rezult_op4_str = " " + str(d) + " " + op4 + " " + str(e) + " "

            if op4 == ':':
                e = random.randint(2, 8)
                # for chosen divider find integer rest with
                while True:
                    d = random.randint(99, 199)
                    if d % e == 0:
                        break
                expr_rezult_op4 = d / e
                expr_rezult_op4_str = " " + str(d) + " " + op4 + " " + str(e) + " "
            if op4 == '':
                expr_rezult_op4 = 0
                expr_rezult_op4_str = ''

            op2 = random.choice(['', '*'])
            if op2 == '*':
                c = random.randint(2, 5)
                expr_rezult_op2 = expr_brackets_rezult * c
                expr_rezult_op2_str = expr_brackets_rezult_str + " " + op2 + " " + str(c) + " "
            if op2 == '':
                expr_rezult_op2 = expr_brackets_rezult
                expr_rezult_op2_str = expr_brackets_rezult_str + " "

            op1 = random.choice(['', '-', '+'])
            if op1 == '-':
                a = random.randint(199, 499)
                expr_rezult = a - expr_rezult_op2
                expr_rezult_str = str(a) + " " + op1 + " " + expr_rezult_op2_str

            if op1 == '+':
                a = random.randint(49, 109)
                expr_rezult = a + expr_rezult_op2
                expr_rezult_str = str(a) + " " + op1 + " " + expr_rezult_op2_str

            if op1 == '':
                expr_rezult_str = expr_rezult_op2_str
                expr_rezult = expr_rezult_op2

            op3 = random.choice(['-', '+'])
            if op3 == '-' and op4 != '':
                expr_rezult = expr_rezult - expr_rezult_op4
                expr_rezult_str = expr_rezult_str + " " + op3 + " " + expr_rezult_op4_str

            if op3 == '+' and op4 != '':
                expr_rezult = expr_rezult + expr_rezult_op4
                expr_rezult_str = expr_rezult_str + " " + op3 + " " + expr_rezult_op4_str

            # at the end we got
            # expr_rezult - result of calculating expression
            # expr_rezult_str - expression string
            # we put a = expr_rezult
            #        b = expr_rezult_str
            a = str(int(expr_rezult))
            b = expr_rezult_str
        if not already_in_hist:
            break

    # add new primer to
    elem = {'a': a,
            'b': b,
            'c': code}  # a,b,op,diff_time
    # make new index
    idx = 0
    for i in hist.keys():
        if int(i) > idx:
            idx = int(i)
    # idx = int(max(hist.keys()))
    hist[idx + 1] = elem
    # to add to favor_ans

    if idx > hist_depth:
        del hist[f'{idx - hist_depth}']
    #     hist.popleft()

    # stolbik t - if operation is stolbik (because code is replaced with +-*)
    return a, b, code, stolbik, drob, expr, hist


# check_ans_drob - check if answer is drob
def check_ans_drob(ans, a, b, code):
    #opers = ['X', '+', '-', divsign, '=', '!']
    oper = OPER_LIST1[code - 1]

    # calculate answer

    d1 = Drob(chis=a['chis'], znam=a['znam'], inte=a['inte'])
    d2 = Drob(chis=b['chis'], znam=b['znam'], inte=b['inte'])
    divsign = u'\u00F7'

    # check calc sectio
    # oper = divsign

    # d1 = Drob(chis=2, znam=5, inte=0)

    # d2 = Drob(chis=4, znam=5, inte=0)
    # print('drob info', d1, d2, oper)

    d1.denormalize()
    d2.denormalize()
    # print(d1, d2)
    # +
    if oper == '+':
        d1.add(d2.chis, d2.znam)
    # -
    if oper == '-':
        d1.subst(d2.chis, d2.znam)
    # *
    if oper == 'X':
        d1.mult(d2.chis, d2.znam)
    # /
    if oper == divsign:
        d1.divide(d2.chis, d2.znam)

    # в d1 ответ, нормализуем
    d1.normalize()
    # = на преобразование ничего не делаем. (ответ уже нормализован)
    if oper == '=':
        pass
    # ! обратное преобразование (normlize)
    if oper == '!':
        d1.denormalize()
    d1_int = d1.inte
    if d1.inte == 0:
        d1_int = ''

    res = {
        'chis': d1.chis,
        'znam': d1.znam,
        'inte': d1_int
    }
    if d1.chis == 0:
        res = {
            'chis': '',
            'znam': '',
            'inte': d1_int
        }

    a_int = ''
    b_int = ''
    res_int = ''
    if a['inte'] != 0:
        a_int = a['inte']
    if b['inte'] != 0:
        b_int = b['inte']
    if res['inte'] != 0:
        res_int = res['inte']
    # case of 0
    if d1.chis == 0 and d1.inte == 0:
        res_int = 0
        res['chis'] = ''
        res['znam'] = ''

    if oper == '=' or oper == '!':
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

                                <p class="sup">{res_int}
                                    <div class="frac">
                                        <span>{res['chis']}</span>
                                        <span class="symbol">/</span>
                                        <span class="bottom">{res['znam']}</span>
                                    </div>
                                </p>
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
    
                        <p class="sup">{res_int}
                            <div class="frac">
                                <span>{res['chis']}</span>
                                <span class="symbol">/</span>
                                <span class="bottom">{res['znam']}</span>
                            </div>
                        </p>
                    </div>
                    '''
    # ans = '1 2/3'
    # ans = '2/3'
    # ans = ' 1 2/3 '
    ans = ans.strip()
    # ans_int_list = ans.split(' ')
    # disasemble string and reassemble with
    ans_int_list = ' '.join(ans.split()).split(' ')
    # ans_int_list = list(filter(lambda x: x != '', ans))
    ans_int = 0
    ans_drob = []
    if len(ans_int_list) == 1:
        ans_drob = ans_int_list[0].split('/')
        if len(ans_drob) == 1:
            ans_int = int(ans_drob[0])
        else:
            ans_int = 0
    elif len(ans_int_list) == 2:
        ans_drob = ans_int_list[1].split('/')
        ans_int = int(ans_int_list[0])

    print(f'result={d1}, user answer=(int) {ans_int} , (drob)={ans_drob}')
    try:
        ans_drob = list(map(int, ans_drob))
    except:
        return drob1, 0

    # check if answer is correct
    answer_correct = 0

    if d1.inte == ans_int:
        if d1.chis == 0:
            answer_correct = 1
        elif len(ans_drob) == 2:
            if (d1.znam == ans_drob[1]) and (d1.chis == ans_drob[0]):
                answer_correct = 1

    return drob1, answer_correct


def check_ans(ans, a1, b1, c1):
    """
    check given answer
    :param ans:
    :param a1:
    :param b1:
    :param c1:
    :return: str
    """
    a = a1
    b = b1
    code = c1

    print(f'check ans= {a},{b},{code}')
    res = 0

    if code == 1:
        res = a * b
    if code == 2:
        res = a + b
    if code == 3:
        res = a - b
    if code == 4:
        res = int(a / b)

    # op ok do the business
    if res == int(ans):

        if code == 1:
            return f" ответ - правильный {a} X {b} = {ans}", 1
        if code == 2:
            return f" ответ - правильный {a} + {b} = {ans}", 1
        if code == 3:
            return f" ответ - правильный {a} - {b} = {ans}", 1
        if code == 4:
            divsign = u'\u00F7'
            return f" ответ - правильный {a} {divsign} {b} = {ans}", 1

    if code == 1:
        return f" ответ - не верный  {a} X {b} = {res}", 0
    if code == 2:
        return f" ответ - не верный  {a} + {b} = {res}", 0
    if code == 3:
        return f" ответ - не верный  {a} - {b} = {res}", 0
    if code == 4:
        divsign = u'\u00F7'
        return f" ответ - не верный  {a} {divsign} {b} = {res}", 0


def finish_lesson(lesson, f_time, favor_ans, wrong_ans, favor_thresold_time):
    """
    finish a lesson
    :param lesson:
    :param f_time:
    :param favor_ans:
    :param wrong_ans:
    :param favor_thresold_time:
    :return:
    """
    reply = []
    ans_num = lesson.ans_amount
    ans_corr = lesson.ans_correct

    reply.append("пока!")
    if ans_num > 1:
        mode_description = get_app_mode_desc(lesson)
        reply.append(
            f"\n вопросов было {ans_num} ({mode_description}), число правильных {ans_corr}, "
            f"процент правильных {int((ans_corr / ans_num) * 100)} %")
        reply.append(f' всего прошло времени {f_time} мин')

        reply.append(f' трудные примеры: {len(favor_ans.keys()) - 1}')
        # sort by time,desc
        # sub_li1 = sorted(favor_ans, key=lambda x: x[2],reverse=True)

        for _, key in favor_ans.items():
            a = key['a']
            b = key['b']
            c = key['c']
            d = key['d']
            if c == 1:
                reply.append(f' {a} X {b} (={a * b}) занял {d} секунд '
                             f'(порог {favor_thresold_time}) сек')
            if c == 2:
                reply.append(f' {a} + {b} (={a + b}) занял {d} секунд '
                             f'(порог {favor_thresold_time}) сек')
            if c == 3:
                reply.append(f' {a} - {b} (={a - b}) занял {d} секунд '
                             f'(порог {favor_thresold_time}) сек')
            if c == 4:
                divsign = u'\u00F7'
                reply.append(f' {a} {divsign} {b} (={int(a / b)}) занял '
                             f'{d} секунд (порог {favor_thresold_time}) сек')

        reply.append(f' неправильные примеры: {len(wrong_ans)}')

        divsign = u'\u00F7'
        oper_list = ['X', '+', '-', divsign, '=', '/=', '#']

        for i in wrong_ans:
            a = i['a']
            b = i['b']
            c = i['c']
            d = i['diff']
            ans = i['ans']

            oper = oper_list[c - 1]

            if not isinstance(a, int):
                # a,b drob
                if oper == '=' or oper == '/=':
                    reply.append(f""" {a['inte']} {a['chis']}/{a['znam']} = {ans} занял {d} сек""")
                elif oper != '#':
                    if a['inte'] == 0:
                        drob_a = f"{a['chis']}/{a['znam']}"
                    else:
                        drob_a = f"{a['inte']} {a['chis']}/{a['znam']}"
                    if b['inte'] == 0:
                        drob_b = f"{b['chis']}/{b['znam']}"
                    else:
                        drob_b = f"{b['inte']} {b['chis']}/{b['znam']}"

                    reply.append(f""" {drob_a} {oper} {drob_b} = {ans} занял {d} сек""")
                else:
                    # expression operation
                    reply.append(f""" выр: {b} = {ans} (={a}) занял {d} сек""")
            else:
                # a,b integer
                if oper == '*':
                    reply.append(f' {a} {oper} {b} = {ans} (={a * b}) занял {d} сек')
                if oper == '+':
                    reply.append(f' {a} {oper} {b} = {ans} (={a + b}) занял {d} сек')
                if oper == '-':
                    reply.append(f' {a} {oper} {b} = {ans} (={a - b}) занял {d} сек')
                if oper == divsign:
                    reply.append(f' {a} {oper} {b} = {ans} (={int(a / b)}) занял {d} сек')

    return reply
