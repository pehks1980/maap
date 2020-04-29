import random,collections, time, threading

from datetime import datetime
import random


#улучшение - используем флаг замены. если была хоть 1 замена вылетаем из цикла.
# в итоге время сортировки зависит от количества замен
def bubble_sort(source_arr):
    zam=True
    n=0
    while zam:
        #print(source_arr,"сч-ик замен ",n)
        zam=False
        for i in range(0, len(source_arr)-1):
            if source_arr[i] > source_arr[i+1]:
                tmp =source_arr[i+1]
                source_arr[i+1] = source_arr[i]
                source_arr[i] = tmp
                zam = True
                n +=1
                break

        if zam==False:
            break

    return source_arr,n

def SetAppMode(list):
    mult=0
    addi=0
    subt=0
    for i in list:
        if int(i)==1:
            mult=1
        if int(i)==2:
            addi=1
        if int(i)==3:
            subt=1

    return (mult,addi,subt)

def GetAppModeDesc(list):
    #result=[]
    a=''
    b=''
    c=''
    for i in list:
        if i=='1':
            a='*,'
        if i=='2':
            b='+,'
        if i=='3':
            c='-'

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
        row=[]
        row.append(i + 1)  # Row nums
        for j in range(len(s[0])):
            if hl == s[i][j]:
                if j == (a - 1):
                    row.append(">"+str(s[i][j]))
                else:
                    row.append(s[i][j])
            else:
                row.append(s[i][j])
        result.append(row)

    #print(result)
    return result

def eval(mult, addi, subt, nx, ny, ax, two_digit, sx, no_minus, no_dec_mul, hist, hist_depth):
    while True:
        already_in_hist = False

        while True:
            code = random.randint(1,3)
            if (mult==1) and (code == 1):
                break
            if (addi==1) and (code == 2):
                break
            if (subt==1) and (code == 3):
                break


        if code == 1:
            a = random.randint(2, nx)
            b = random.randint(2, ny)
        if code == 2:
            while True:
                a = random.randint(1, ax)
                b = random.randint(1, ax)

                if two_digit:
                    if a > 10 or b > 10:
                        break
                    else:
                        continue

        if code == 3:
            while True:
                a = random.randint(1, sx)
                b = random.randint(1, sx)

                if two_digit:
                    if a>10 or b>10:
                        break
                    else:
                        continue

                if a != b:
                    break

#        print(a,b)

            if no_minus:
                if a<b:
                    tmp=a#swap it so there is no minus
                    a = b
                    b=tmp

            if no_dec_mul:#no 10s in multiplication
                if (a == 10) or (b == 10):
                    already_in_hist = True
                    continue

        for id, key in hist.items():
            ha = key['a']
            hb = key['b']
            hcode = key['c']
            if a == ha and b == hb and code == hcode:
                already_in_hist=True

        if already_in_hist==False:
            break

    #add new primer to
    elem = {'a': a,
            'b': b,
            'c': code}  # a,b,op,diff_time
    # make new index
    idx=0
    for i in hist.keys():
        if int(i)>idx:
            idx = int(i)
    #idx = int(max(hist.keys()))
    hist[idx+1] = elem
    # to add to favor_ans

    if idx > hist_depth:
        del hist[f'{idx-hist_depth}']
    #     hist.popleft()

    return a,b,code,hist

def check_ans(ans, diff, a1, b1, c1):
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



    if ans != 'q':
        if ans == 'c':
            if code == 1:
                # printMatrix(mult_tabl, res, a, b)
                return (f" подсказка : ответ - правильный {a} X {b} = {res}", 0)
            if code == 2:
                return (f" подсказка : ответ - правильный {a} + {b} = {res}", 0)
            if code == 3:
                return (f" подсказка : ответ - правильный {a} - {b} = {res}", 0)
        else:
            # op ok do the business
            if res == int(ans):

                if code == 1:
                    return (f" ответ - правильный {a} X {b} = {ans}", 1)
                if code == 2:
                    return (f" ответ - правильный {a} + {b} = {ans}", 1)
                if code == 3:
                    return (f" ответ - правильный {a} - {b} = {ans}", 1)

            else:
                if code == 1:
                    return (f" ответ - не верный  {a} X {b} = {res}", 0)
                    # return (f' смотрите подсказку в таблице:')
                    # returnMatrix(mult_tabl, res, a, b)
                if code == 2:
                    return (f" ответ - не верный  {a} + {b} = {res}", 0)
                if code == 3:
                    return (f" ответ - не верный  {a} - {b} = {res}", 0)

def finish_lesson(f_time,ans_num, ans_corr, favor_ans, favor_thresold_time):
    reply=[]
    reply.append("пока!")
    if ans_num > 1:
        reply.append(f"\n вопросов было {ans_num}, число правильных {ans_corr}, процент правильных {int((ans_corr/ans_num)*100)} %")
        reply.append(f' всего прошло времени {int(f_time/60)} мин')

        reply.append(f' трудные примеры: {len(favor_ans.keys())-1}')
        #sort by time,desc
        #sub_li1 = sorted(favor_ans, key=lambda x: x[2],reverse=True)


        for id,key in favor_ans.items():
            a=key['a']
            b=key['b']
            c=key['c']
            d=key['d']
            if c == 1:
                reply.append(f' {a} X {b} (={a * b}) занял {d} секунд (порог {favor_thresold_time}) сек')
            if c == 2:
                reply.append(f' {a} + {b} (={a + b}) занял {d} секунд (порог {favor_thresold_time}) сек')
            if c == 3:
                reply.append(f' {a} - {b} (={a - b}) занял {d} секунд (порог {favor_thresold_time}) сек')

    return reply

    # def __init__(self):
    #     #init...
    #     self.mult = 1
    #     self.addi = 1
    #     self.subt = 1
    #     self.hist_depth = 5
    #
    #     # mult
    #     # mult=1#1-yes 0 -no
    #     self.nx = 12  # range
    #     self.ny = 10
        # add
        # addi=1
        # self.ax = 50  # range
        # # subc
        # # subt=1
        # self.sx = 50
        # # no minus in answer substract
        # self.no_minus = 1
        # # no dec in multip
        # self.no_dec_mul = 1
        # # two_digit nuber a or b in +-
        # self.two_digit = 1
        #
        # self.favor_ans_depth = 10
        # self.favor_ans_depth_min = 4  # if more it starts to take questions from favor_ans_queue
        #
        # self.favor_thresold_time = 14
        #
        # self.start_time = 0
        #
        # self.ans_num = 1
        # self.ans_corr = 0
        #
        # self.mult_tabl = []
        #
        # self.hist = collections.deque()
        #
        # self.favor_ans = collections.deque()
        #
        # #code op storage
        # self.a1 = 0
        # self.b1 = 0
        # self.c1 = 0
        # self.now=[]
        # self.lesson_id=0
        # self.end_time=[]
        # self.mode=[]
        #
        # for i in range(1, self.ny + 1):
        #     row = []
        #     for j in range(1, self.nx + 1):
        #         row.append(i * j)
        #     self.mult_tabl.append(row)
        #
        # self.printMatrix(self.mult_tabl,0,0,0)

        # self.size = 13
        # self.array = [i for i in range(self.size)]
        # random.shuffle(self.array)
        #
        # print(self.array)
        #
        # self.new_array, self.k = self.bubble_sort(self.array)
        #
        # print(self.new_array, self.k)
        #
        # random.seed(self.k)





    #
    #
    # if random.randint(1,3)==3:
    #     if len(favor_ans) > favor_ans_depth_min:
    #         print(f' попробуйте снова решить задачу:')
    #         idx=random.randint(0,len(favor_ans)-1)
    #         a=favor_ans[idx][0]
    #         b=favor_ans[idx][1]
    #         code=favor_ans[idx][2]#code oper - 1-mul,2-add,3-sub
    #
    #
    # ch1=[]#hist chunk 0 result 1 op
    # ch1.append(a)
    # ch1.append(b)
    # ch1.append(code)
    # hist.append(ch1)
    #
    # if len(hist) > hist_depth:
    #     hist.popleft()
    #
    # if len(favor_ans) > favor_ans_depth:
    #     favor_ans.popleft()
    #
    #
    #
    # print(f"\n вопрос {ans_num}, число правильных {ans_corr}")
    #
    #
    # if code == 1:
    #     print(f"\n введите сколько будет {a} X {b} (q - exit) (c-podskazka)")
    # if code == 2:
    #     print(f"\n введите сколько будет {a} + {b} (q - exit) (c-podskazka)")
    # if code == 3:
    #     if a==b:
    #         print("xxx")
    #
    #     print(f"\n введите сколько будет {a} - {b} (q - exit) (c-podskazka)")
    #
    # #print(time.ctime())
    #
    # now = datetime.now()
    #
    # while True:
    #     ans = input()
    #     if ans!='':
    #         break
    #
    # later = datetime.now()
    #
    # difference = int((later - now).total_seconds())
    #
    # if difference >favor_thresold_time:
    #     already_in=False
    #
    #     for x in favor_ans:
    #         if a == x[0] and b == x[1]:
    #             already_in=True
    #
    #     if already_in==False:
    #         elem=[]#a,b,op,diff_time
    #         elem.append(a)
    #         elem.append(b)
    #         elem.append(code)
    #         elem.append(difference)
    #         favor_ans.append(elem)
    #
    # #print(time.ctime())


    
            # difference = 4
            # self.f_time +=difference
            # print(f' время затраченное на ответ {difference} сек')
    #
    # else:

