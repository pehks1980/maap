import random, collections, time, threading

from datetime import datetime
import random


# улучшение - используем флаг замены. если была хоть 1 замена вылетаем из цикла.
# в итоге время сортировки зависит от количества замен
def bubble_sort(source_arr):
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

        if zam == False:
            break

    return source_arr, n


def SetAppMode(list):
    mult = 0
    addi = 0
    subt = 0
    divn = 0

    for i in list:
        if int(i) == 1:
            mult = 1
        if int(i) == 2:
            addi = 1
        if int(i) == 3:
            subt = 1
        if int(i) == 4:
            divn = 1

    return (mult, addi, subt, divn)


def GetAppModeDesc(list):
    # result=[]
    a = ''
    b = ''
    c = ''
    for i in list:
        if i == '1':
            a = '*,'
        if i == '2':
            b = '+,'
        if i == '3':
            c = '-'

    return f'{a}{b}{c}'


def printMatrix(s, hl, a, b):
    # Do heading
    result = []
    row = []
    row.append(" ")
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

#choce the next question from random, take into account previous answers hist
def eval(mult, addi, subt, divn, nx, ny, ax, two_digit, sx, no_minus, no_dec_mul, hist, hist_depth):

    code = None

    while True:
        already_in_hist = False
        #choice type of question *-+/ if code is not chosen already
        if code == None:
            while True:
                code = random.randint(1, 4)
                if (mult == 1) and (code == 1):
                    break
                if (addi == 1) and (code == 2):
                    break
                if (subt == 1) and (code == 3):
                    break
                if (divn == 1) and (code == 4):
                    break
        #mul a,b 2..10 2..12 mult table 10X12
        if code == 1:
            #mul op
            mul_op_ratio = 10
            op = random.randint(1, 100)
            if op > mul_op_ratio:
                a = random.randint(2, nx)
                b = random.randint(2, ny)
            else:#a*10,100,100
                digs = [ 10**x for x in  range(1,4)]
                a = random.randint(2, ny*nx)
                b = random.choice(digs)

            #choice of

        #+
        if code == 2:
            if random.randint(0,3) == 3:
                #25% prob rate 100-200  div 2
                a = random.randint(10, 20) * 10
                b = random.randint(10, ax-20)
            else:
                while True:
                    a = random.randint(1, ax)
                    b = random.randint(1, ax)

                    if two_digit:
                        if a > 50 and b < 50:
                            break
                        else:
                            if b > 50 and a < 50:
                                break

                            continue
        #-
        if code == 3:
            while True:
                a = random.randint(1, sx)
                b = random.randint(1, sx)

                if two_digit:
                    if a > 10 or b > 10:
                        break
                    else:
                        continue

                if a != b:
                    break # exit

            #        print(a,b)

            if no_minus:
                if a < b:
                    tmp = a  # swap it so there is no minus
                    a = b
                    b = tmp

            if no_dec_mul:  # no 10s in multiplication
                if (a == 10) or (b == 10):
                    already_in_hist = True
                    continue
        #div on multiple table:
        if code == 4:
            if random.randint(0,3) == 3:
                #25% prob rate 100-200  div 2
                a = random.randint(10, 20) * 10
                b = 2
            else:
                #mul table div 72 div 8
                ops = []
                ops.append(random.randint(2, nx))
                ops.append(random.randint(2, ny))
                a1 = ops[0]
                b1 = ops[1]
                a = a1 * b1
                b = random.choice(ops)

        for id, key in hist.items():
            ha = key['a']
            hb = key['b']
            hcode = key['c']
            if a == ha and b == hb and code == hcode:
                already_in_hist = True

        if already_in_hist == False:
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

    return a, b, code, hist


def check_ans(ans, a1, b1, c1):
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
        res = int (a / b)


    # op ok do the business
    if res == int(ans):

        if code == 1:
            return (f" ответ - правильный {a} X {b} = {ans}", 1)
        if code == 2:
            return (f" ответ - правильный {a} + {b} = {ans}", 1)
        if code == 3:
            return (f" ответ - правильный {a} - {b} = {ans}", 1)
        if code == 4:
            divsign = u'\u00F7';
            return (f" ответ - правильный {a} {divsign} {b} = {ans}", 1)


    if code == 1:
        return (f" ответ - не верный  {a} X {b} = {res}", 0)
    if code == 2:
        return (f" ответ - не верный  {a} + {b} = {res}", 0)
    if code == 3:
        return (f" ответ - не верный  {a} - {b} = {res}", 0)
    if code == 4:
        divsign = u'\u00F7';
        return (f" ответ - не верный  {a} {divsign} {b} = {res}", 0)


def finish_lesson(f_time, ans_num, ans_corr, favor_ans, wrong_ans, favor_thresold_time):
    reply = []
    reply.append("пока!")
    if ans_num > 1:
        reply.append(
            f"\n вопросов было {ans_num}, число правильных {ans_corr}, процент правильных {int((ans_corr / ans_num) * 100)} %")
        reply.append(f' всего прошло времени {f_time} мин')

        reply.append(f' трудные примеры: {len(favor_ans.keys()) - 1}')
        # sort by time,desc
        # sub_li1 = sorted(favor_ans, key=lambda x: x[2],reverse=True)

        for id, key in favor_ans.items():
            a = key['a']
            b = key['b']
            c = key['c']
            d = key['d']
            if c == 1:
                reply.append(f' {a} X {b} (={a * b}) занял {d} секунд (порог {favor_thresold_time}) сек')
            if c == 2:
                reply.append(f' {a} + {b} (={a + b}) занял {d} секунд (порог {favor_thresold_time}) сек')
            if c == 3:
                reply.append(f' {a} - {b} (={a - b}) занял {d} секунд (порог {favor_thresold_time}) сек')
            if c == 4:
                divsign = u'\u00F7';
                reply.append(f' {a} {divsign} {b} (={int(a / b)}) занял {d} секунд (порог {favor_thresold_time}) сек')

        reply.append(f' неправильные примеры: {len(wrong_ans)}')

        for i in wrong_ans:
            a = i['a']
            b = i['b']
            c = i['c']
            d = i['diff']
            ans = i['ans']

            if c == 1:
                reply.append(f' {a} X {b} = {ans} (={a * b}) занял {d} сек')
            if c == 2:
                reply.append(f' {a} + {b} = {ans} (={a + b}) занял {d} сек')
            if c == 3:
                reply.append(f' {a} - {b} = {ans} (={a - b}) занял {d} сек')
            if c == 4:
                divsign = u'\u00F7';
                reply.append(f' {a} {divsign} {b} = {ans} (={int(a / b)}) занял {d} сек')

    return reply

