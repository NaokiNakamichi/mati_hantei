import collections
import random
import copy
import time


# 入力に対して待ちを判定するクラス。
class hantei:
    def __init__(self):
        self.hantei_time = 0
    # 三つの数字（牌）が連番かどうかをCheck
    def renban_check(self, x):
        x.sort()
        if (x[0] + 1 == x[1]) and (x[1] + 1 == x[2]):
            return True
        else:
            return False

    # ４枚の牌に対して待ちを確認する。
    def check_4(self, nyuryoku):
        a = range(1, 10)
        k = str(nyuryoku)
        tehai = []
        hora = []
        for i in k:
            tehai.append(int(i))
        if len(set(tehai)) == 1:
            return []
        else:
            for i in a:
                kari_tehai = tehai + [i]
                if len(set(kari_tehai)) != len(kari_tehai):
                    c = collections.Counter(kari_tehai)
                    for key, value in c.items():
                        if value > 1:
                            kari_tehai.remove(key)
                            kari_tehai.remove(key)
                            if len(set(kari_tehai)) == 1:
                                hora.append(i)
                            if self.renban_check(kari_tehai):
                                hora.append(i)
                            kari_tehai.append(key)
                            kari_tehai.append(key)
            return set(hora)

    # 連番（順子）を取り除く. １３枚の入力なら１０枚の返り値
    def remove_3_syuntsu(self, x, i):
        x.remove(i)
        x.remove(i + 1)
        x.remove(i + 2)
        return x

    # 同じ三つの数字（刻子）を取り除く。上と同様
    def remove_3_kotsu(self, x, i):
        x.remove(i)
        x.remove(i)
        x.remove(i)
        return x

    def list_to_int(self, x):
        k = ""
        for j in x:
            k += str(j)
        l = int(k)
        return l

    def sweap_3(self, x):
        tehai = []
        sweap_list = []
        for i in str(x):
            tehai.append(int(i))
        tehai.sort()
        c = collections.Counter(tehai)
        syurui = set(tehai)
        for i in range(1, 8):
            kari_tehai = copy.deepcopy(tehai)
            if (i in syurui) and (i + 1 in syurui) and (i + 2 in syurui):
                k = self.remove_3_syuntsu(kari_tehai, i)
                sweap_list.append(self.list_to_int(k))
        for i in range(1, 10):
            kari_tehai = copy.deepcopy(tehai)
            if c[i] > 2:
                k = self.remove_3_kotsu(kari_tehai, i)
                sweap_list.append(self.list_to_int(k))
        return sweap_list

    def hanteikun(self, x):
        start = time.time()
        kouho_1 = self.sweap_3(x)
        hora = set()
        for k in kouho_1:
            kouho_2 = self.sweap_3(k)
            for j in kouho_2:
                kouho_3 = self.sweap_3(j)
                for l in kouho_3:
                    hora = hora | set(self.check_4(l))
        self.hantei_time = time.time() - start
        return hora


class generate_mondai(hantei):
    def __init__(self, sakuseisuu):
        super(generate_mondai, self).__init__()
        self.sakuseisuu = sakuseisuu
        self.result = {}

    def generate_q(self):
        question = []
        for _ in range(13):
            question.append(str(random.randint(1, 9)))
        c = collections.Counter(question)
        kaisuu = c.most_common()[0][1]
        if kaisuu > 3:
            question = False
        else:
            question = int("".join(sorted(question)))
        return question

    def generate_a(self):
        while len(self.result) < self.sakuseisuu:
            q = self.generate_q()
            if q:
                k = self.hanteikun(q)
                if len(k) > 2:
                    self.result[q] = k
        return self.result

    def generate_swift(self):
        if self.result:
            for key, value in self.result.items():
                tmp = []
                for i in range(1, 10):
                    if i in value:
                        tmp.append(True)
                    else:
                        tmp.append(False)

                # swiftの構文
                # self.list.append(QuestionAnswer(imageList: ["2","2","2","3","4","4","4","5","6","6","7","7","8"], boolList: [false,false,false,false,false,true,true,false,true]))
                print("self.list.append(QuestionAnswer(imageList: {}, boolList: {}))".format(list(str(key)), tmp))
        else:
            print("解答を作ってません")