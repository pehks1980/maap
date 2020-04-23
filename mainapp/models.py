import collections
import random

from django.db import models

from django.conf import settings

# Create your models here.

import random, collections, time, threading

from datetime import datetime

import random



class MulApp():

    # улучшение - используем флаг замены. если была хоть 1 замена вылетаем из цикла.
    # в итоге время сортировки зависит от количества замен.
    def bubble_sort(self, source_arr):
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

    def SetAppMode(self, list):
        self.mult = 0
        self.addi = 0
        self.subt = 0
        for i in list:
            if int(i) == 1:
                self.mult = 1
            if int(i) == 2:
                self.addi = 1
            if int(i) == 3:
                self.subt = 1

    def GetAppModeDesc(self, list):
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

    def printMatrix(self, s, hl, a, b):
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

    def __init__(self):
        # init...
        self.mult = 1
        self.addi = 1
        self.subt = 1
        self.hist_depth = 5

        # mult
        # mult=1#1-yes 0 -no
        self.nx = 12  # range
        self.ny = 10
        # add
        # addi=1
        self.ax = 50  # range
        # subc
        # subt=1
        self.sx = 50
        # no minus in answer substract
        self.no_minus = 1
        # no dec in multip
        self.no_dec_mul = 1
        # two_digit nuber a or b in +-
        self.two_digit = 1

        self.favor_ans_depth = 10
        self.favor_ans_depth_min = 4  # if more it starts to take questions from favor_ans_queue

        self.favor_thresold_time = 14

        self.start_time = 0

        self.ans_num = 1
        self.ans_corr = 0

        self.mult_tabl = []

        self.hist = collections.deque()

        self.favor_ans = collections.deque()

        # code op storage
        self.a1 = 0
        self.b1 = 0
        self.c1 = 0
        self.now = []
        self.lesson_id = 0
        self.end_time = []
        self.mode = []

        for i in range(1, self.ny + 1):
            row = []
            for j in range(1, self.nx + 1):
                row.append(i * j)
            self.mult_tabl.append(row)

        self.printMatrix(self.mult_tabl, 0, 0, 0)

        self.size = 13
        self.array = [i for i in range(self.size)]
        random.shuffle(self.array)

        print(self.array)

        self.new_array, self.k = self.bubble_sort(self.array)

        print(self.new_array, self.k)

        random.seed(self.k)

    def f(self):
        return 'hello world'

    def getstatus(self):

        return f"status"

    def eval(self):
        while True:
            already_in_hist = False

            while True:
                code = random.randint(1, 3)
                if (self.mult == 1) and (code == 1):
                    break
                if (self.addi == 1) and (code == 2):
                    break
                if (self.subt == 1) and (code == 3):
                    break

            if code == 1:
                a = random.randint(2, self.nx)
                b = random.randint(2, self.ny)
            if code == 2:
                while True:
                    a = random.randint(1, self.ax)
                    b = random.randint(1, self.ax)

                    if self.two_digit:
                        if a > 10 or b > 10:
                            break
                        else:
                            continue

            if code == 3:
                while True:
                    a = random.randint(1, self.sx)
                    b = random.randint(1, self.sx)

                    if self.two_digit:
                        if a > 10 or b > 10:
                            break
                        else:
                            continue

                    if a != b:
                        break

                #        print(a,b)

                if self.no_minus:
                    if a < b:
                        tmp = a  # swap it so there is no minus
                        a = b
                        b = tmp

                if self.no_dec_mul:  # no 10s in multiplication
                    if (a == 10) or (b == 10):
                        already_in_hist = True
                        continue

            for x in self.hist:
                if a == x[0] and b == x[1] and code == x[2]:
                    already_in_hist = True

            if already_in_hist == False:
                break
        # add new primer to histqueue

        ch1 = []  # hist chunk 0 result 1 op
        ch1.append(a)
        ch1.append(b)
        ch1.append(code)
        self.hist.append(ch1)

        if len(self.hist) > self.hist_depth:
            self.hist.popleft()

        self.a1 = a
        self.b1 = b
        self.c1 = code
        return a, b, code

    def check_ans(self, ans, diff):
        a = self.a1
        b = self.b1
        code = self.c1

        if code == 1:
            res = a * b
        if code == 2:
            res = a + b
        if code == 3:
            res = a - b

        self.ans_num += 1

        if diff > self.favor_thresold_time:
            already_in = False
            for x in self.favor_ans:
                if a == x[0] and b == x[1]:
                    already_in = True

            if already_in == False:
                elem = []  # a,b,op,diff_time
                elem.append(a)
                elem.append(b)
                elem.append(code)
                elem.append(diff)
                self.favor_ans.append(elem)

        if ans != 'q':
            if ans == 'c':
                if code == 1:
                    # printMatrix(mult_tabl, res, a, b)
                    return f" подсказка : ответ - правильный {a} X {b} = {res}", 1
                if code == 2:
                    return (f" подсказка : ответ - правильный {a} + {b} = {res}", 1)
                if code == 3:
                    return (f" подсказка : ответ - правильный {a} - {b} = {res}", 1)
            else:
                # op ok do the business
                if res == int(ans):
                    self.ans_corr += 1
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

            # difference = 4
            # self.f_time +=difference
            # print(f' время затраченное на ответ {difference} сек')

    #
    # else:

    def finish(self, f_time):
        reply = []
        reply.append("пока!")
        if self.ans_num > 1:
            self.ans_num = self.ans_num - 1
            reply.append(
                f"\n вопросов было {self.ans_num}, число правильных {self.ans_corr}, процент правильных {int((self.ans_corr / self.ans_num) * 100)} %")
            reply.append(f' всего прошло времени {int(f_time / 60)} мин')

            reply.append(f' трудные примеры: {len(self.favor_ans)}')
            # sort by time,desc
            sub_li1 = sorted(self.favor_ans, key=lambda x: x[2], reverse=True)

            for i in sub_li1:
                if i[2] == 1:
                    reply.append(
                        f' {i[0]} X {i[1]} (={i[0] * i[1]}) занял {i[3]} секунд (порог {self.favor_thresold_time}) сек')
                if i[2] == 2:
                    reply.append(
                        f' {i[0]} + {i[1]} (={i[0] + i[1]}) занял {i[3]} секунд (порог {self.favor_thresold_time}) сек')
                if i[2] == 3:
                    reply.append(
                        f' {i[0]} - {i[1]} (={i[0] - i[1]}) занял {i[3]} секунд (порог {self.favor_thresold_time}) сек')

        return reply


class MaapLesson(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lesson')

    date = models.CharField(verbose_name='s_time', max_length=24, blank=True)
    s_time = models.CharField(verbose_name='s_time', max_length=12, blank=True)
    f_time = models.CharField(verbose_name='f_time', max_length=12, blank=True)
    # mode=models.PositiveIntegerField(verbose_name='mode', null=True)
    mode = models.CharField(verbose_name='mode', max_length=12, blank=True)
    ans_amount = models.PositiveIntegerField(verbose_name='ans_amount', null=True)  # integer NULL!
    ans_correct = models.PositiveIntegerField(verbose_name='ans_correct', null=True)

    Ma = MulApp()

    def __str__(self):
        return self.user_id







