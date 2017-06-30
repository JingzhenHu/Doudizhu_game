import random,copy,os

class Doudizhu:
    def __init__(self,dizhu=None,user=None):
        self.user = []
        self.point = 5
        self.a = []
        for a in range(0,54):
            self.a.append(a)
        self.cards = []
        self.n_grades = []
        self.c_grades = []
        self.card_type = ['solo', 'pair', 'rocket', 'trio', 'trio_solo', \
                            'trio_pair', 'pair_sister', 'boom', 'chain', \
                            'airplane', 'airplane_solo', 'airplane_pair', \
                            'four_solo', 'four_pair']
        type = ['diamond', 'clubs', 'hearts', 'spades']
        number = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
        score = []
        for i in range(1,14):
            score.append(i)
        index = 0
        score_index = 0
        for num in number:
            for t in type:
                pattern = ''.join([t, '_', num])
                pattern_score = score[score_index]
                self.cards.append((index, pattern))
                self.n_grades.append((index,pattern_score))
                self.c_grades.append((pattern,pattern_score))
                index += 1
            score_index += 1
        self.cards.append((52, 'BlackJoker'))
        self.cards.append((53, 'RedJoker'))
        self.n_grades.append((52,14))
        self.n_grades.append((53, 15))
        self.n_grades = dict(self.n_grades)
        self.c_grades.append(('BlackJoker',14))
        self.c_grades.append(('RedJoker', 15))
        self.c_grades = dict(self.c_grades)
        # print(self.cards)
        # print(self.n_grades)
        # print(self.c_grades)

    def submapping(self):
        cards_map = dict(self.cards)
        paistr1 = ''
        for i in range(len(self.str1)):
            paistr1 += cards_map[self.str1[i]] + ' '
        paistr2 = ''
        for i in range(len(self.str2)):
            paistr2 += cards_map[self.str2[i]] + ' '
        paistr3 = ''
        for i in range(len(self.str3)):
            paistr3 += cards_map[self.str3[i]] + ' '
        return paistr1,paistr2,paistr3

    def shuffleCards(self):
        random.shuffle(self.a)
        n=random.randint(1,54)
        b=self.a[:n]
        c=self.a[n:]
        self.a=c+b

    def dealingCards(self):
        self.str1=self.a[:-3:3]
        self.str2=self.a[1:-3:3]
        self.str3=self.a[2:-3:3]
        self.str4=self.a[-3:]

    def toBeLandholder(self):
        cards1,cards2,cards3 = self.submapping()
        com1, num1 = self.analysis(cards1)
        com2, num2 = self.analysis(cards2)
        com3, num3 = self.analysis(cards3)
        # Triky here, Instead of random
        # I let the mini turns user to be the landholder,
        # But we still cannot predict what will happen after adding
        # the rest three cards
        mini = min([num1,num2,num3])
        if (mini==num1):
            self.dizhu = 0
            self.str1 += self.str4
        if (mini==num2):
            self.dizhu = 1
            self.str2 += self.str4
        if (mini==num3):
            self.dizhu = 2
            self.str3 += self.str4
        cards_map = dict(self.cards)
        paistr4 = ''
        for i in range(len(self.str4)):
            paistr4 += cards_map[self.str4[i]] + ' '
        self.threeCard = paistr4



    def sort(self): #
        self.str1.sort(reverse=True)
        self.str2.sort(reverse=True)
        self.str3.sort(reverse=True)

    def sortWithPattern(self,card):
        c_num = []
        for key, value in self.cards:
            for item in card:
                if value == item:
                    c_num.append(key)
        c_num.sort(reverse=True)
        sortCards = []
        cards = dict(self.cards)
        for index in c_num:
            for item in cards:
                if item == index:
                    sortCards.append(cards[index])
        return sortCards

    def mapping(self):
        cards_map = dict(self.cards)
        paistr1=''
        for i in range (len(self.str1)):
            paistr1+=cards_map[self.str1[i]]+' '
        paistr2=''
        for i in range (len(self.str2)):
            paistr2+=cards_map[self.str2[i]]+' '
        paistr3=''
        for i in range (len(self.str3)):
            paistr3+=cards_map[self.str3[i]]+' '
        self.user.append(paistr1)
        self.user.append(paistr2)
        self.user.append(paistr3)

    def isSolo(self,card):
        if (isinstance(card,str)):
            card = card.split()
        bool = False
        if(card is not None and len(card) == 1):
            bool = True
        return bool

    def soloGra(self,card):
        return self.c_grades[card[0]]

    def isPair(self,card):
        if (isinstance(card,str)):
            card = card.split()
        bool = False
        if(card is not None and len(card) == 2):
            if(self.c_grades[card[0]] == self.c_grades[card[1]]):
                bool = True
        return bool

    def pairGra(self,card):
        return self.c_grades[card[0]]

    def isTrio(self,card):
        if (isinstance(card,str)):
            card = card.split()
        bool = False
        if(card is not None and len(card) == 3):
            if(self.c_grades[card[0]] == self.c_grades[card[1]] and \
                       self.c_grades[card[1]] == self.c_grades[card[2]]):
                bool = True
        return bool

    def TrioGra(self,card):
        return self.c_grades[card[0]]

    def isTrioWithSolo(self,card):
        if (isinstance(card,str)):
            card = card.split()
        bool = False
        c_num = []
        if(card is not None and len(card) == 4):
            card = self.sortWithPattern(card)
            if(self.c_grades[card[0]] == self.c_grades[card[1]] and \
                self.c_grades[card[1]] == self.c_grades[card[2]] and \
                self.c_grades[card[2]] != self.c_grades[card[3]]):
                bool = True
            if (self.c_grades[card[1]] == self.c_grades[card[2]] and \
                self.c_grades[card[2]] == self.c_grades[card[3]] and \
                self.c_grades[card[0]] != self.c_grades[card[1]]):
                bool = True
        return  bool

    def TrioSoloGra(self,card):
        card = self.sortWithPattern(card)
        return self.c_grades[card[1]]

    def isTrioWithPair(self, card):
        if (isinstance(card,str)):
            card = card.split()
        bool = False
        c_num = []
        if (card is not None and len(card) == 5):
            card = self.sortWithPattern(card)
            if (self.c_grades[card[0]] == self.c_grades[card[1]] and \
                        self.c_grades[card[1]] == self.c_grades[card[2]]):
                bool = True
            if (self.c_grades[card[2]] == self.c_grades[card[3]] and \
                        self.c_grades[card[3]] == self.c_grades[card[4]]):
                bool = True
        return bool

    def TrioPairGra(self,card):
        card = self.sortWithPattern(card)
        return self.c_grades[card[2]]

    def isBoom(self,card):
        if (isinstance(card,str)):
            card = card.split()
        bool = False
        c_num = []
        if(card is not None and len(card) == 4):
            if(self.c_grades[card[0]] == self.c_grades[card[1]] and \
                   self.c_grades[card[1]] == self.c_grades[card[2]] and \
                   self.c_grades[card[2]] == self.c_grades[card[3]]):
                bool = True
        return bool

    def BoomGra(self,card):
        return self.c_grades[card[0]]

    # length is between 5 and 12
    def isChain(self,card):
        if (isinstance(card,str)):
            card = card.split()
        if(card is not None):
            size = len(card)
            if(size < 5 or size > 12):
                return False
            card = self.sortWithPattern(card)
            for i in range(0,size-1):
                currGrade = self.c_grades[card[i]]
                proGrade = self.c_grades[card[i+1]]
                # 2, RedJoker, and BlackJoker cannot be in the chain
                if(currGrade==15 or currGrade==14 or currGrade==13):
                    return False
                elif(proGrade == 15 or proGrade ==14 or proGrade ==13):
                    return False
                elif(proGrade - currGrade != -1):
                    return False
        return True

    def chainGra(self,card):
        card = self.sortWithPattern(card)
        return len(card),self.c_grades[card[0]]

    def isRocket(self,card):
        if (isinstance(card,str)):
            card = card.split()
        bool = False
        if(card is not None and len(card) == 2):
            if (int(self.c_grades[card[0]]) + int(self.c_grades[card[1]]) == 29):
                bool = True
        return bool

    def isPairSisters(self,card):
        if (isinstance(card,str)):
            card = card.split()
        if (card is None):
            return False
        size = len(card)
        if (size < 6 or len(card)%2 != 0):
            return False
        else:
            card = self.sortWithPattern(card)
            index = 0
            while (index < size):
                if(self.c_grades[card[index]] != self.c_grades[card[index+1]]):
                    return False
                if(index < size - 2):
                    if(self.c_grades[card[index]] - self.c_grades[card[index+2]] != 1):
                        return False
                index += 2
        return True

    def pairSisGra(self,card):
        card = self.sortWithPattern(card)
        return len(card),self.c_grades[card[0]]

    def isAirplane(self,card):
        if (isinstance(card,str)):
            card = card.split()
        bool = False
        if (card is None):
            return bool
        size = len(card)
        if (size < 6 or size%3 != 0):
            return bool
        else:
            card = self.sortWithPattern(card)
            index = 0
            while (index < size):
                if (self.c_grades[card[index]] != self.c_grades[card[index + 1]] \
                or  self.c_grades[card[index+1]] != self.c_grades[card[index + 2]]):
                    return False
                if (index < size - 3):
                    if (self.c_grades[card[index]] - self.c_grades[card[index + 3]] != 1):
                        return False
                index += 3
        return True

    def airGra(self,card):
        card = self.sortWithPattern(card)
        return len(card),self.c_grades[card[0]]

    def isAirplaneWithSolo(self, card):
        if (isinstance(card,str)):
            card = card.split()
        bool = False
        if (card is None):
            return bool
        size = len(card)
        if(size < 8 and size%4 != 0):
            return bool
        else:
            card = self.sortWithPattern(card)
            fliterList = []
            index = 0
            while (index < size-2):
                if(self.c_grades[card[index]] == self.c_grades[card[index+1]] and \
                   self.c_grades[card[index+1]] == self.c_grades[card[index+2]]):
                    fliterList.append(card[index])
                    fliterList.append(card[index+1])
                    fliterList.append(card[index+2])
                index += 1
            bool = self.isAirplane(fliterList)
            if bool is True:
                # check the distinct of kickers
                kickers = list(set(card) - set(fliterList))
                numOfK = len(kickers)
                for i in range(0,numOfK):
                    # blackJoker and RedJoker cannot be the kicker
                    curGra = self.c_grades[kickers[i]]
                    if(curGra == 14 or curGra == 15):
                        bool = False
                        break
                    for j in range(i+1,numOfK):
                        # print(self.c_grades[kickers[i]])
                        if (curGra == self.c_grades[kickers[j]]):
                            bool = False
        return bool

    # the function is useful for both airSolo and airPair
    def airkikGra(self,card):
        card = self.sortWithPattern(card)
        size = len(card)
        fliterList = []
        index = 0
        while (index < size - 2):
            if (self.c_grades[card[index]] == self.c_grades[card[index + 1]] and \
                            self.c_grades[card[index + 1]] == self.c_grades[card[index + 2]]):
                fliterList.append(card[index])
                fliterList.append(card[index + 1])
                fliterList.append(card[index + 2])
            index += 1
        temp,gra = self.airGra(fliterList)
        return size,gra

    def isAirplaneWithPair(self, card):
        if (isinstance(card,str)):
            card = card.split()
        bool = False
        if (card is None):
            return bool
        size = len(card)
        if (size < 10 and size % 5 != 0):
            return bool
        else:
            card = self.sortWithPattern(card)
            fliterList = []
            index = 0
            while (index < size - 2):
                if (self.c_grades[card[index]] == self.c_grades[card[index + 1]] and \
                    self.c_grades[card[index + 1]] == self.c_grades[card[index + 2]]):
                    fliterList.append(card[index])
                    fliterList.append(card[index + 1])
                    fliterList.append(card[index + 2])
                index += 1
            bool = self.isAirplane(fliterList)
            if bool is True:
                # check the distinct of kickers
                kickers = list(set(card) - set(fliterList))
                numOfK = len(kickers)
                kickers = self.sortWithPattern(kickers)
                index = 0
                while (index < numOfK):
                    if (self.c_grades[kickers[index]] != self.c_grades[kickers[index + 1]]):
                        bool = False
                    if (index < numOfK - 2):
                        if (self.c_grades[kickers[index]] == self.c_grades[kickers[index + 2]]):
                            bool = False
                    index += 2
        return bool

    def isFourwithSolo(self,card):
        if (isinstance(card,str)):
            card = card.split()
        bool = False
        size = len(card)
        if (card is None or size != 6):
            return bool
        else:
            card = self.sortWithPattern(card)
            index = 0
            fliterList = []
            while (index < size - 3):
                if (self.c_grades[card[index]] == self.c_grades[card[index + 1]] and \
                    self.c_grades[card[index + 1]] == self.c_grades[card[index + 2]] and \
                    self.c_grades[card[index + 2]] == self.c_grades[card[index + 3]]):
                    fliterList.append(card[index])
                    fliterList.append(card[index + 1])
                    fliterList.append(card[index + 2])
                    fliterList.append(card[index + 3])
                index += 1
            bool = self.isBoom(fliterList)
            if bool is True:
                # check the distinct of kickers
                kickers = list(set(card) - set(fliterList))
                if self.c_grades[kickers[0]] == self.c_grades[kickers[1]]:
                    bool = False
        return bool

    def fourSoloGra(self,card):
        card = self.sortWithPattern(card)
        return self.c_grades[card[2]]

    def isFourwithPair(self,card):
        if (isinstance(card,str)):
            card = card.split()
        bool = False
        size = len(card)
        if (card is None or size != 8):
            return bool
        else:
            card = self.sortWithPattern(card)
            index = 0
            fliterList = []
            while (index < size - 3):
                if (self.c_grades[card[index]] == self.c_grades[card[index + 1]] and \
                    self.c_grades[card[index + 1]] == self.c_grades[card[index + 2]] and \
                    self.c_grades[card[index + 2]] == self.c_grades[card[index + 3]]):
                    fliterList.append(card[index])
                    fliterList.append(card[index + 1])
                    fliterList.append(card[index + 2])
                    fliterList.append(card[index + 3])
                index += 1
            bool = self.isBoom(fliterList)
            if bool is True:
                # check the distinct of kickers
                kickers = list(set(card) - set(fliterList))
                numOfK = len(kickers)
                kickers = self.sortWithPattern(kickers)
                index = 0
                while (index < numOfK):
                    if (self.c_grades[kickers[index]] != self.c_grades[kickers[index + 1]]):
                        bool = False
                    if (index < numOfK - 2):
                        if (self.c_grades[kickers[index]] == self.c_grades[kickers[index + 2]]):
                            bool = False
                    index += 2
        return bool

    def fourpairGra(self,card):
        card = self.sortWithPattern(card)
        return self.c_grades[card[2]]

    def judgeType(self,cards):
        flag = False
        for each in cards:
            for key in self.c_grades:
                if (each == key):
                    flag = True
        if (not flag):
            return 'error type'
        if(self.isSolo(cards)):
            return self.card_type[0]
        elif(self.isPair(cards)):
            return self.card_type[1]
        elif(self.isRocket(cards)):
            return self.card_type[2]
        elif(self.isTrio(cards)):
            return self.card_type[3]
        elif(self.isTrioWithSolo(cards)):
            return self.card_type[4]
        elif(self.isTrioWithPair(cards)):
            return self.card_type[5]
        elif(self.isPairSisters(cards)):
            return self.card_type[6]
        elif(self.isBoom(cards)):
            return self.card_type[7]
        elif(self.isChain(cards)):
            return self.card_type[8]
        elif(self.isAirplane(cards)):
            return self.card_type[9]
        elif(self.isAirplaneWithSolo(cards)):
            return self.card_type[10]
        elif(self.isAirplaneWithPair(cards)):
            return self.card_type[11]
        elif(self.isFourwithSolo(cards)):
            return self.card_type[12]
        elif(self.isFourwithPair(cards)):
            return self.card_type[13]
        else:
            return 'error type'

    def hasRocket(self,card):
        first_two = card[0:2]
        rocket = self.isRocket(first_two)
        return rocket

    def isOver(self):
        if(len(self.user[self.dizhu]) == 0):
            return True,user.point
        elif(len(self.user[(self.dizhu+1)%3]) == 0 or len(self.user[(self.dizhu+2)%3]) == 0):
            return True,-user.point
        else:
            return False,0

    def nextState(self,*args):
        if (len(args) == 2 and isinstance(args[0],list) and isinstance(args[1],int)):
            args[0][self.dizhu] -= args[1]
        if (len(args) == 3 and isinstance(args[0],list) and isinstance(args[1],int) and isinstance(args[2],int)):
            args[0][(self.dizhu+1)%3] -= args[1]
            args[0][(self.dizhu+2)%3] -= args[2]
        return args[0]

# originally, I would like to build a minimax tree but then I realize the situation will bemuch more
# complex than my expectation. Althought I could analyze how many methods to give out cards in one turn,
# I cannot predict wether the other players can beat them. If one of them can catch the cards, then I
# need to consider whether I can beat their cards. If not, then I lose the priority of giving out cards.
# Then, I stop here, waiting for some ideas.

    def getAvial(self):
        com,num = self.analysis(self.user[dizhu])
        step_one_num_list = []
        for each in com:
            step_one_num_list.append(len(each))
        currState = []
        for each in self.user:
            currState.append(len(each))
        nextState = []
        for each in step_one_num_list:
            nextState.append(self.nextState(currState,each))

    def evaGrade(self,cards):
        if(not isinstance(cards,list)):
            cards = cards.split()
        if(self.isSolo(cards)):
            return self.soloGra(cards)
        elif(self.isPair(cards)):
            return 2+self.pairGra(cards)
        elif(self.isRocket(cards)):
            return 29 # 14 + 15 -> max
        elif(self.isTrio(cards)):
            return 3+self.TrioGra(cards)
        elif(self.isTrioWithSolo(cards)):
            return 4+self.TrioSoloGra(cards)
        elif(self.isTrioWithPair(cards)):
            return 5+self.TrioPairGra(cards)
        elif(self.isPairSisters(cards)):
            len,gra = self.pairSisGra(cards)
            return len+gra
        elif(self.isBoom(cards)):
            return 12+self.BoomGra(cards)
        elif(self.isChain(cards)):
            len, gra = self.chainGra(cards)
            return len+gra
        elif(self.isAirplane(cards)):
            len, gra = self.airGra(cards)
            return len + gra
        elif(self.isAirplaneWithSolo(cards) or self.isAirplaneWithPair(cards)):
            len, gra = self.airkikGra(cards)
            return len + gra
        elif(self.isFourwithSolo(cards)):
            return 5+self.fourSoloGra(cards)
        elif(self.isFourwithPair(cards)):
            return 6+self.fourpairGra(cards)
        else:
            return 0

    def hasChain(self,cards,chain):
        if (isinstance(cards,str)):
            card = cards.split()
        card = copy.deepcopy(cards)
        count = [0]*12
        for i in range(len(card)-1,-1,-1): #card: #(0,len(card)):
            if (self.c_grades[card[i]] == 13 or self.c_grades[card[i]] == 14 or self.c_grades[card[i]] == 15):
                temp = card[i]
                card.remove(temp)
        for i in range(len(card) - 1, -1, -1):
            for grade in range(1,13):
                if self.c_grades[card[i]] == grade:
                    count[grade-1] += 1
        # if no sevens and no tens, then no chains
        end = []
        for i in range(0,12):
            if count[i] == 0:
                end.append(i)
        if (len(end) > 0):
            # print(end)
            endbegin = end[0]
            if (endbegin > 4):
                # print('Head Have CHAIN!')
                chain1 = []
                index1 = len(card) - 1
                for i in range(0, endbegin):
                    # print(index1)
                    # print(card[index1])
                    # print(count[i])
                    chain1.append(card[index1])
                    index1 -= 1
                    index1 -= (count[i] - 1)
                chain.append(chain1)
            endend = end[len(end) - 1]
            if (endend <= 6):
                # print('Trail Have CHAIN!')
                chain1 = []
                index1 = 0
                # print(count)
                for i in range(11,endend, -1):#12):
                    # print(index1)
                    # print(card[index1])
                    # print(count[i])
                    chain1.append(card[index1])
                    index1 += 1
                    index1 += (count[i] - 1)
                chain.append(chain1)
                # print('Have CHAIN!')
            for i in range(0, len(end) - 1):
                if end[i + 1] - end[i] > 5:
                    # print('Middle Have CHAIN!')
                    # print(count)
                    chain1 = []
                    index1 =0
                    for j in range(end[i+1],len(count)):
                        index1+= count[j]
                    # index1 += 1
                    for i in range(end[i+1]-1,end[i],-1):
                        # print(index1)
                        # print(card[index1])
                        # print(count[i])
                        chain1.append(card[index1])
                        index1 += 1
                        index1 += (count[i] - 1)
                    chain.append(chain1)
        else:
            chain1 = []
            index1 = len(card) - 1
            for i in range(0, 12):
                chain1.append(card[index1])
                index1 -= 1
                index1 -= (count[i] - 1)
            chain.append(chain1)

    def hasBoom(self,card,list1):
        if (isinstance(card,str)):
            card = card.split()
        size = len(card)
        index = 0
        while(index < size-3):
            sub = card[index:index+4]
            boom = self.isBoom(sub)
            if(boom):
                list1.append(sub)
                for i in range(0,4):
                    card.remove(card[index])
                size -= 4
                index -= 1
            index += 1

    def hasTrio(self,card,list2):
        if (isinstance(card,str)):
            card = card.split()
        size = len(card)
        index = 0
        while (index < size - 2):
            sub = card[index:index + 3]
            trio = self.isTrio(sub)
            if (trio):
                list2.append(sub)
                for i in range(0, 3):
                    card.remove(card[index])
                size -= 3
                index -= 1
            index += 1

    def hasPair(self,card,list4):
        if (isinstance(card,str)):
            card = card.split()
        size = len(card)
        index = 0
        while (index < size - 1):
            sub = card[index:index + 2]
            trio = self.isPair(sub)
            if (trio):
                list4.append(sub)
                for i in range(0, 2):
                    card.remove(card[index])
                size -= 2
                index -= 1
            index += 1

    def combinTrioKik(self,list2,list4):
        len2 = len(list2)
        len4 = len(list4)
        # combine kik to Trios or Airplanes
        if (len2 != 0 and len4 != 0):
            if(len4 > len2):
                index = 1
                for each in list2:
                    temp = list4[len4-index]
                    if(isinstance(temp,str)):
                        each.append(temp)
                    else:
                        each.append(temp[0])
                        each.append(temp[1])
                    index += 1
                    list4.remove(temp)
            else:
                index = 0
                for each in list4:
                    if(isinstance(each,str)):
                        list2[index].append(each)
                    else:
                        list2[index].append(each[0])
                        list2[index].append(each[1])
                    list4.remove(each)
                    index += 1

    def combinAirKik(self,list3,list5):
        # print(list3)
        # print(list5)
        pair = []
        solo = []
        for each in list5:
            if(isinstance(each,list)):
                pair.append(each)
            else:
                solo.append(each)
        pairNum = len(pair)
        soloNum = len(solo)
        if (pairNum%2 is not 0):
            pair.remove(pair[0])
            pairNum -= 1
        if (soloNum%2 is not 0):
            solo.remove(solo[0])
            soloNum -= 1
        len3 = len(list3)
        # combine kik to Trios or Airplanes
        if (len3 != 0 and pairNum != 0):
            if(pairNum > 2*len3):
                index = 1
                for each in list3:
                    temp1 = pair[pairNum-index]
                    temp2 = pair[pairNum-index-1]
                    each.append(temp1[0])
                    each.append(temp1[1])
                    each.append(temp2[0])
                    each.append(temp2[1])
                    index += 1
                    list5.remove(temp1)
                    list5.remove(temp2)
            else:
                index = 0
                i_p = 0
                # print(pair)
                while i_p < pairNum:
                    temp1 = pair[i_p]
                    temp2 = pair[i_p+1]
                    list3[index].append(temp1[0])
                    list3[index].append(temp1[1])
                    list3[index].append(temp2[0])
                    list3[index].append(temp2[1])
                    index += 1
                    i_p += 2
                    list5.remove(temp1)
                    list5.remove(temp2)
        rest = len3-pairNum/2
        if(rest> 0 and soloNum != 0):
            if(soloNum > rest):
                index = 1
                for each in list3:
                    if(len(each)==6):
                        temp1 = solo[pairNum-index]
                        temp2 = solo[pairNum-index-1]
                        each.append(temp1)
                        each.append(temp2)
                        index += 1
                        list5.remove(temp1)
                        list5.remove(temp2)
                    else:
                        index += 1
            else:
                index = 0
                i_s = 0
                while i_s < soloNum:
                    if(len(list3[index])==6):
                        temp1 = solo[i_s]
                        temp2 = solo[i_s+1]
                        list3[index].append(temp1)
                        list3[index].append(temp2)
                        index += 1
                        i_p += 2
                        list5.remove(temp1)
                        list5.remove(temp2)
                    else:
                        index += 1

    def analysis(self,card):
        # list1 -- for boom and Rocket
        # list2 -- for Trios
        # list3 -- for Airplanes
        # chain -- for chains
        # list4 -- for pairs and solo
        card = card.split()
        # card = self.sortWithPattern(card)
        numOfTurns = 0
        value = 0
        list1 = []
        list2 = []
        # checking for rocket
        rocket = self.hasRocket(card)
        if(rocket):
            list1.append([card[0],card[1]])
            card.remove(card[0])
            card.remove(card[0])

        # checking for booms
        self.hasBoom(card,list1)
        # print(list1)
        # checking for trios
        self.hasTrio(card,list2)
        # print(list1)
        # print(list2)
        # print(card)
        # here need to make up checking for airplane
        list3 = []
        numTrio = len(list2)
        if(numTrio>=2):
            remove = []
            for i in range(0,numTrio-1,2):
                oneair = []
                curr = list2[i]
                next = list2[i+1]
                # 2 cannot be in the airplane
                if(self.TrioGra(curr) != 13):
                    if(self.TrioGra(curr)-self.TrioGra(next)==1):
                        for each in curr:
                            oneair.append(each)
                        for each in next:
                            oneair.append(each)
                        remove.append(curr)
                        remove.append(next)
                        list3.append(oneair)
            for item in remove:
                list2.remove(item)
        # checking for chain
        chain = []
        self.hasChain(card,chain)
        # print(chain)
        # print(count)
        for item in chain:
            for each in item:
                card.remove(each)
        # print(chain)
        # print(card)
        # combine the Trio and the rest of the card into chain and pair if possible
        if (len(list2) != 0):
            combine = copy.deepcopy(card)
            for item in list2:
                for each in item:
                    combine.append(each)
            chain_recheck = []
            combine = self.sortWithPattern(combine)
            # print(combine)
            self.hasChain(combine, chain_recheck)
            if(len(chain_recheck) != 0):
                for item in list2:
                    for each in item:
                        card.append(each)
                for item in chain_recheck:
                    chain.append(item)
                    for each in item:
                        card.remove(each)
                list2 =[]
        list4 = []
        self.hasPair(card,list4)
        # check whether have pairSisters
        # len4 = len(list4)
        # pairSis = []
        # if(len4>=3):
        #     # print(list4)
        #     grade = []
        #     grade_map = {}
        #     for each in list4:
        #         temp = self.pairGra(each)
        #         grade.append(temp)
        #         grade_map[temp] = each
        #     index = 0
        #     while index<len4:
        #         eachlist = []
        #         for each in list4[index]:
        #             eachlist.append(each)
        #         # eachlist.append(list4[index][0])
        #         # eachlist.append(list4[index][1])
        #         for i in range(index+1,len4-1):
        #             currGra = self.pairGra(list4[i])
        #             # print(list4[i], currGra)
        #             postGra = self.pairGra(list4[i+1])
        #             # print(list4[i+1], postGra)
        #             if (currGra - postGra == -1):
        #                 if(currGra!=13 and postGra!=13):
        #                     for each in list4[i+1]:
        #                         eachlist.append(each)
        #                     # eachlist.append(list4[i+1][0])
        #                     # eachlist.append(list4[i+1][1])
        #         if (len(eachlist) > 2):
        #             pairSis.append(eachlist)
        #         index += 1

        #     removelist = []
        #     for each in pairSis:
        #         self.hasPair(each,removelist)
        #     for each in removelist:
        #         list4.remove(each)
        for each in card:
            list4.append(each)
        self.combinTrioKik(list2,list4)
        self.combinAirKik(list3,list4)
        combin = []
        len1 = len(list1)
        len2 = len(list2)
        len3 = len(list3)
        len4 = len(list4)
        if (len(chain) != 0):
            for each in chain:
                combin.append(each)
        if (len1 != 0):
            for each in list1:
                combin.append(each)
        if (len2 != 0):
            for each in list2:
                combin.append(each)
        if (len3 != 0):
            for each in list3:
                combin.append(each)
        if (len4 != 0):
            for each in list4:
                combin.append(each)
        numOfTurns = len(combin)
        # print(combin)
        # if(len4 > (2*len3 +len2)):
        #     numOfTurns -= (len2 + 2*len3)
        # else:
        #     numOfTurns -= len4
        return combin,numOfTurns

    def remove(self,userNum,outCards,pre,preType):
        status = True
        beat = False
        if (outCards == 'pass'):
            return True,None
        currCards = self.user[userNum].split()
        if(not isinstance(outCards,list)):
            outCards = outCards.split()
        if(pre is not None):
            if (not isinstance(pre, list)):
                preCards = pre.split()
            else:
                preCards = pre
        else:
            preCards = None
        if(outCards is not None):
            card_type = self.judgeType(outCards)
        else:
            status = False
            card_type = None
        if (card_type == 'error type'):
            print('Invalid cards type!')
            status = False
        if(preType is not None):
            if(card_type != preType):
                if(preType == 'rocket'):
                    print('Invalid cards type to compete previous player!')
                    status = False
                elif(card_type == 'rocket'):
                    beat = True
                elif(card_type == 'boom'):
                    beat = True
                else:
                    status = False
            if(status and not beat):
                index = self.card_type.index(card_type)
                currGrad = 0
                preGrad = 0
                if (index == 0):
                    currGrad = self.soloGra(outCards)
                    preGrad = self.soloGra(preCards)
                if (index == 1):
                    currGrad = self.pairGra(outCards)
                    preGrad = self.pairGra(preCards)
                if (index == 3):
                    currGrad = self.TrioGra(outCards)
                    preGrad = self.TrioGra(preCards)
                if (index == 4):
                    currGrad = self.TrioSoloGra(outCards)
                    preGrad = self.TrioSoloGra(preCards)
                if (index == 5):
                    currGrad = self.TrioPairGra(outCards)
                    preGrad = self.TrioPairGra(preCards)
                if (index == 6):
                    currGrad = self.pairSisGra(outCards)
                    preGrad = self.pairSisGra(preCards)
                if (index == 7):
                    currGrad = self.BoomGra(outCards)
                    preGrad = self.BoomGra(preCards)
                if (index == 8):
                    len1,currGrad = self.chainGra(outCards)
                    len2,preGrad = self.chainGra(preCards)
                    if (len1 != len2):
                        print('Invalid cards length to compete previous player!')
                        status = False
                if (index == 9):
                    len1,currGrad = self.airGra(outCards)
                    len2,preGrad = self.airGra(preCards)
                    if (len1 != len2):
                        print('Invalid cards length to compete previous player!')
                        status = False
                if (index == 10 or index == 11):
                    len1,currGrad = self.airkikGra(outCards)
                    len2,preGrad = self.airkikGra(preCards)
                    if (len1 != len2):
                        print('Invalid cards length to compete previous player!')
                        status = False
                if(index == 12):
                    currGrad = self.fourSoloGra(outCards)
                    preGrad = self.fourSoloGra(preCards)
                if(index == 13):
                    currGrad = self.fourpairGra(outCards)
                    preGrad = self.fourpairGra(preCards)
                if (status and currGrad<=preGrad):
                    print('Cannot compete to previous player!')
                    status = False
        if(status):
            for item in outCards:
                try:
                    currCards.remove(item)
                except ValueError:
                    print('Please give out the existed cards!!')
                    status = False
                    break
        if(status):
            self.user[userNum] = ' '.join([x for x in currCards if x])
        return status,card_type

def dizhuturns(userNum,preType,pre,prepreType,prepre,com):
    out = ''
    card_type = ''
    if (preType is None and pre is None and prepreType is None and prepre is None):
        out = lowLevelAI(com)
        status, type = user.remove(userNum, out, None, None)
        os.system('clear')
    else:
        if ((pre == 'pass' and prepre == 'pass')):  # or (preType == None and prepreType == None)):
            out = lowLevelAI(com)
            status, type = user.remove(userNum, out, None, None)
            while (not status):
                out = lowLevelAI(com)
                status, type = user.remove(userNum, out, None, None)
            os.system('clear')
        else:
            if(pre=='pass'):
                out = doHold(com,prepre,prepreType)
                if (out == 'pass'):
                    os.system('clear')
                    # print('Last turn giving out:')
                    # print(pre)
                    # print(preType)
                    return out, None
                else:
                    status, type = user.remove(userNum, out, prepre, prepreType)
                    os.system('clear')
            else:
                out = doHold(com,pre,preType)
                if (out == 'pass'):
                    os.system('clear')
                    # print('Last turn giving out:')
                    # print(pre)
                    # print(preType)
                    return out, None
                else:
                    status, type = user.remove(userNum, out, pre, preType)
                    os.system('clear')
    return out,type

def oneturns(userNum,preType,pre,prepreType,prepre):
    out = raw_input('Your turn to give out cards: ')
    while(not bool(out)):
        out = raw_input('Your turn to give out cards: ')
    card_type = ''
    if(out == 'pass'):
        if (preType is None and pre is None and prepreType is None and prepre is None):
            print('You cannot pass for the first turn!')
            out,card_type = oneturns(userNum,None,None,None,None)
        elif (pre=='pass' and prepre == 'pass'):
            print('You cannot pass at your priority!')
            out,card_type = oneturns(userNum,None,'pass',None,'pass')
        else:
            os.system('clear')
            return out,None
    else:
        if((pre=='pass' and prepre == 'pass')):# or (preType == None and prepreType == None)):
            status, card_type = user.remove(userNum, out, None, None)
            while (not status):
                out = raw_input('Your turn to give out cards: ')
                status, card_type = user.remove(userNum, out, None, None)
            os.system('clear')
        else:
            if(pre=='pass'):
                status, card_type = user.remove(userNum, out, prepre, prepreType)
                while (not status):
                    out = raw_input('Your turn to give out cards: ')
                    status, card_type = user.remove(userNum, out, prepre, prepreType)
                os.system('clear')
            else:
                status, card_type = user.remove(userNum, out, pre, preType)
                while (not status):
                    out = raw_input('Your turn to give out cards: ')
                    status, card_type = user.remove(userNum, out, pre, preType)
                os.system('clear')
    # print(out,type)
    return out,card_type

def printHint(com):
    print('Hints @~@')
    for each in com:
        if (isinstance(each, list)):
            print(' '.join(str(x) for x in each))
        else:
            print(each)

def lowLevelAI(com):
    gra_map = {}
    gra_list = []
    for each in com:
        temp = user.evaGrade(each)
        gra_list.append(temp)
        gra_map[temp] = each
    mini = min(gra_list)
    choosen = gra_map[mini]
    if (isinstance(choosen, list)):
        choosen = ' '.join(str(x) for x in choosen)
    return choosen

def doHold(com,pre,preType):
    hold = []
    # for each in com:
    #     if(isinstance(each,str)):
    #         each = each.split()
    # print(com)
    # print('pre',pre)
    # print('preType',preType)
    for each in com:
        if(isinstance(each,str)):
            each = each.split()
        print(each)
        card_type = user.judgeType(each)
        if (card_type== preType):
            hold.append(each)
        if (card_type=='rocket'):
            hold.append(each)
        if (card_type=='boom'):
            hold.append(each)
    if(len(hold)==0):
        return 'pass'
    else:
        remove = []
        if(not isinstance(pre,list)):
            preC = pre.split()
        for each in hold:
            card_type=user.judgeType(each)
            if (card_type == 'chain'):
                len1,currGrad = user.chainGra(each)
                len2,preGrad = user.chainGra(preC)
                if (len1 != len2):
                    remove.append(each)
            if (card_type == 'airplane'):
                len1,currGrad = user.airGra(each)
                len2,preGrad = user.airGra(preC)
                if (len1 != len2):
                    remove.append(each)
            if (card_type == 'airplane_solo' or card_type == 'airplane_pair'):
                len1,currGrad = user.airkikGra(each)
                len2,preGrad = user.airkikGra(preC)
                if (len1 != len2):
                    remove.append(each)
        for item in remove:
            hold.remove(item)
        preGrad = user.evaGrade(pre)
        # print('preGrad',preGrad)
        beat = {}
        beatkey = []
        for each in hold:
            currGrad = user.evaGrade(each)
            # print('curGrad',currGrad)
            # print('cur',each)
            if(currGrad>preGrad):
                beatkey.append(currGrad)
                beat[currGrad] = each
        if (len(beat) == 0):
            return 'pass'
        else:
            mini = min(beatkey)
            return beat[mini]

# colorMap = { 'HEADER' : '\033[95m','OKBLUE' :'\033[94m', 'OKGREEN' : '\033[92m', 'WARNING' : '\033[93m',\
#     'FAIL' : '\033[91m', 'ENDC' : '\033[0m', 'BOLD' : '\033[1m', 'UNDERLINE' : '\033[4m'}
# colorList = []
# for key in colorMap:
#     colorList.append(colorMap[key])
user=Doudizhu()
user.shuffleCards()
user.dealingCards()

user.toBeLandholder()
user.sort()
user.mapping()
dizhu = user.dizhu
# com,num = user.analysis('RedJoker BlackJoker hearts_A diamond_A spades_K hearts_K diamond_K hearts_J clubs_J diamond_J spades_10 clubs_10 diamond_10 hearts_9 diamond_9 diamond_8 spades_7 spades_5 clubs_4 spades_3')
# print(com,num)
if(dizhu == 0):
    print('Landholder:')
    print(user.user[0])
    com,num = user.analysis(user.user[0])
    printHint(com)
    # bg = 40
    # for each in com:
    #     format = ';'.join([str(0), str(32), str(bg)])
    #     bg += 2
    #     for item in each:
    #         print(format + item + '\x1b[0;34;42m')

if(dizhu == 1):
    print('Landholder:')
    print(user.user[1])
    # print('\x1b[6;30;41m' + user.user[1] + '\x1b[0m')
    com,num = user.analysis(user.user[1])
    printHint(com)

if(dizhu == 2):
    print('Landholder:')
    print(user.user[2])
    # print('\x1b[6;30;41m' + user.user[2] + '\x1b[0m')
    com,num = user.analysis(user.user[2])
    printHint(com)

out,type = dizhuturns(dizhu,None,None,None,None,com)
# print(out)
# print(''.join(['Type of ', type]))
prepre = None
prepreType = None
pre = out
preType = type
userNum = dizhu
while(True):
    userNum = (userNum+1)%3
    if(userNum==dizhu):
        print('prepre turn givens:', prepre)
        print('pre turn gives: ',pre)
        print('Landholder turn: ')
        print 'It is your turn, User #{0:1d}'.format(userNum)
        print(user.user[userNum])
        com, num = user.analysis(user.user[userNum])
        printHint(com)
        currOut, currType = dizhuturns(userNum, preType, pre, prepreType, prepre, com)
        if(currType == 'rocket' or currType=='boom'):
            print('Double the score!')
            user.point *= 2
            print(''.join(['Current score is: ',str(user.point)]))
        # print('Landholder gives out: ')
        # print(currOut)
        # if (currType is not None and currType is not 'error type'):
        #     print(''.join(['Type of ', currType]))
        if(len(user.user[userNum])==0):
            print('\x1b[6;30;41m' + 'Landholder win!!!' + '\x1b[0m')
            print(''.join(['Landholder: +',str(user.point)]))
            print(''.join(['Both Peasants: -', str(float(user.point/2))]))
            break
    else:
        print('prepre turn givens:', prepre)
        print('pre turn gives: ',pre)
        print 'dizhu is User#{0:1d}'.format(dizhu)
        print('The three cards assgined are ' + user.threeCard)
        print('Peasant turn: ')
        print 'It is your turn, User #{0:1d}'.format(userNum)
        print(user.user[userNum])
        com, num = user.analysis(user.user[userNum])
        printHint(com)
        currOut, currType = oneturns(userNum,preType,pre,prepreType,prepre)
        if(currType == 'rocket' or currType=='boom'):
            print('Double the score!')
            user.point *= 2
            print(''.join(['Current score is: ', str(user.point)]))
        # print('Peasant gives out: ')
        # print(currOut)
        # if(currType is not None and currType is not 'error type'):
        #     print(''.join(['Type of ', currType]))
        if (len(user.user[userNum]) == 0):
            print('\x1b[6;30;41m'+ 'Peasants win!!!' + '\x1b[0m')
            print(''.join(['Both Peasants: +', str(float(user.point/2))]))
            print(''.join(['Landholder: -', str(user.point)]))
            break
    prepre = pre
    prepreType = preType
    pre = currOut
    preType = currType

