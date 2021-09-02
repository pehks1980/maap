
DROBI_PLUS_SET = [
    {'chis': 1, 'znam': 5},
    {'chis': 1, 'znam': 4},
    {'chis': 1, 'znam': 3},
    {'chis': 2, 'znam': 3},
    {'chis': 3, 'znam': 5},
]

DROBI_MINUS_SET = [

]

DROBI_MULT_SET = [

]

class Drob:
    def __init__(self, chis, znam, inte=0):
        self.chis = chis
        self.znam = znam
        self.inte = inte

    def normalize(self):
        def iter1():
            if self.chis > self.znam:
                z = self.gcd(self.chis, self.znam)
                if z > 0:
                    self.inte += z
                    self.chis = self.chis - self.znam
                    iter1()
            else:
                return
        # call inline func recursively
        iter1()

    def denormalize(self):
        if self.inte > 0:
            self.chis = self.inte * self.znam + self.chis
            self.inte = 0

    def add(self, chis, znam):
        self.denormalize()
        x = self.chis * znam + chis * self.znam
        y = self.znam * znam
        z = self.gcd(x, y)
        self.chis = x // z
        self.znam = y // z

    def subst(self, chis, znam):
        self.denormalize()
        x = self.chis * znam - chis * self.znam
        y = self.znam * znam
        z = self.gcd(x, y)
        self.chis = x // z
        self.znam = y // z

    def divide(self, chis, znam):
        self.mult(znam, chis)

    def mult(self, chis, znam):
        x = self.chis * chis
        y = self.znam * znam
        z = self.gcd(x, y)
        self.chis = x // z
        self.znam = y // z

    def __str__(self):
        return f'{self.inte} {self.chis}/{self.znam}'

    def gcd(self, x, y):
        while y != 0:
            (x, y) = (y, x % y)
        return x

#
# d1 = Drob(chis=1, znam=5)
#
# d2 = Drob(chis=1, znam=4)
# print(d1, d2)
#
# d1.denormalize()
# d2.denormalize()
#
# print(d1, d2)
#
# d1.add(d2.chis, d2.znam)
#
# print(d1)
#
# d1.normalize()
# print(d1)
#
# d1.denormalize()
# print(d1)
