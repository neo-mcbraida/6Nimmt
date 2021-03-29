import random
import numpy as np

import AIOpponent

class Board:
    def __init__(self):
        self.epSinceUpdate = 0
        self.Reset()

    def Mix(self):
        random.shuffle(self.cards)
        self.deck1.append(self.cards[0])
        self.possibleCards.remove(card)
        self.deck2.append(self.cards[1])
        self.deck3.append(self.cards[2])
        self.deck4.append(self.cards[3])
        del self.cards[:4]
        del self.possibleCards[:4]
        for i in range(6):
            self.players[i].Reset()
            self.players[i].cards = self.cards[:10]
            del self.cards[:10]

    def GetCards(self):
        #print(self.p1.selected)
        tempstate = self.GetState(self.p2)
        self.p2.AIOpSelect(tempstate)
        #print(self.p2.selected)
        tempstate = self.GetState(self.p3)
        self.p3.AIOpSelect(tempstate)
        #print(self.p3.selected)
        tempstate = self.GetState(self.p4)
        self.p4.AIOpSelect(tempstate)
        #print(self.p4.selected)
        tempstate = self.GetState(self.p5)
        self.p5.AIOpSelect(tempstate)
        #print(self.p5.selected)
        tempstate = self.GetState(self.p6)
        self.p6.AIOpSelect(tempstate)
        #print(self.p6.selected)

    def SortCards(self):
        self.players.sort(key=lambda x: x.selected)

    def CheckOpUpdate(self):
        if self.epSinceUpdate == 5000:
            AIOpponent.OpUpdateModel()
            self.epSinceUpdate = 0
        else:
            self.epSinceUpdate += 1

    def Turn(self):
        print(self.decks)
        print(self.p1.penaltyCards)
        print(self.p1.cards)
        self.p1.PlayerSelect()
        self.GetCards()
        self.SortCards()#rearranges self.players in order or card number
        self.PlaceCard()
        if len(self.p1.cards) == 0:
            self.PlayerGetPen()#all players calculate their penalty
            winner = self.GetWinner()#returns player with highest penalty
            #print(winner)
            self.StartGame()
        else:
            self.Turn()

    def GetState(self, player):
        temp1 = self.AddZeroes(self.deck1)
        self.AddNegOne(temp1)
        temp2 = self.AddZeroes(self.deck2)
        self.AddNegOne(temp2)
        temp3 = self.AddZeroes(self.deck3)
        self.AddNegOne(temp3)
        temp4 = self.AddZeroes(self.deck4)
        self.AddNegOne(temp4)
        tempplayer = self.AddZeroes(player.cards)
        state = [temp1, temp2, temp3, temp4, tempplayer]
        #print(state)
        return state

    def AddZeroes(self, array):
        temp = array.copy()
        num = 10 - len(temp)
        i = 0
        while i < num:
            temp.append(0)
            i += 1
        return temp

    def AddNegOne(self, array):
        if array[4] == 0:
            array[4] = -1

    def StartGame(self):
        #self.cards = self.pHolder
        self.Mix()
        #return self.GetState()
        self.Turn()

    def SelectDeck(self, card):
        difMin = 105
        difMinIndex = -1
        for i in range(0, 4):
            deck = self.decks[i]
            if deck[-1] < card:
                tempDifMin = card - deck[-1]
                if tempDifMin < difMin or difMinIndex == -1 :
                    difMinIndex = i
                    difMin = tempDifMin
        return difMinIndex

    def GivePenalty(self, player, deck):
        for card in deck[:-1]:
            player.penaltyCards.append(card)
            player.tempPickUp.append(card)
        del deck[:-1]

    def PlaceCard(self):
        for player in self.players:
            card = player.selected
            index = self.SelectDeck(card)
            deck = self.decks[index]
            self.AddToRow(deck, index, card, player)

    def PickUp(self, index, player, card):
        for c in self.decks[index]:
            player.penaltyCards.append(c)
            player.tempPickUp.append(c)

        self.decks[index] = []
        self.decks[index].append(card)
        self.possibleCards.remove(card)

    def AddToRow(self, deck, index, card, player):
        if index == -1:
            index = self.GetSmallestDeck(self.decks)
            self.PickUp(index, player, card)
        elif len(deck) == 5:
            deck.append(card)
            self.GivePenalty(player, deck)
            self.possibleCards.remove(card)
        else:
            deck.append(card)
            self.possibleCards.remove(card)

    def GetSmallestDeck(self, decks):#returns deck with smallest penalty
        lowestPen = 100
        deckIndex = 0
        for i in range (0, 4):
            deck = decks[i]
            deckPen = self.CalcTurnPen(deck)
            if lowestPen > deckPen:
                deckIndex = i
                lowestPen = deckPen
        return deckIndex

    def PlayerGetPen(self):
        for player in self.players:
            player.CalcTotalPen()

    def GetWinner(self):
        lowest = 200
        winners = []
        for player in self.players:
            if player.penalty < lowest:
                winners = []
                winners.append(player.name)
            elif player.penalty == lowest:
                winners.append(player.name)
        return winners

    def GetTurnReward(self):#may need adjusting based on how well deep learning works
        reward = 5
        penalty = self.p1.CalcTurnPen(self.p1.tempPickUp)
        if penalty != 0:
            reward = penalty * - 2
        return reward

    def CalcTurnPen(self, penaltyCards):
        penalty = 0
        for card in penaltyCards:
        # for card in penaltyCards:
            if card == 55:
                penalty += 7
            elif (card % 11) == 0:
                penalty += 5
            elif (card % 10) == 0:
                penalty += 3
            elif (card % 5) == 0:
                penalty += 2
            else:
                penalty += 1
        return penalty

    #Method to let Model train against random inputs
    def StepRand(self, cardInd):
        self.p1.AiSelect(cardInd)
        self.CheckOpUpdate()
        if self.p1.selected == 0:
            nextState = np.array(self.GetState(self.p1))
            reward = -80 #discourage agent choosing card that doesnt rlly exist
            done = False
            return nextState, reward, done
        else:
            #if len(self.p1.cards) == 0:
               # nextState = np.array(self.GetState())
               # self.PlayerGetPen()#all players calculate their penalty
                #winners = self.GetWinner()#returns player with highest penalt
               # reward = self.GetTurnReward(True)
               # return nextState, reward, True
            #else:
            self.GetCards()
            self.SortCards()
            self.PlaceCard()
            self.SetDeck()
            nextState = np.array(self.GetState(self.p1))
            reward = self.GetTurnReward()
            if len(self.p1.cards) == 0:
                #nextState = np.array(self.GetState())
                self.PlayerGetPen()#all players calculate their penalty
                #winners = self.GetWinner()#returns player with highest penalt
                #reward = self.GetTurnReward()
                return nextState, reward, True
            else:
                return nextState, reward, False

    #Method to let Model train against itself
    #def TurnSelf(self):

    def SetDeck(self):#Because I'm bad at coding
        self.deck1 = self.decks[0]
        self.deck2 = self.decks[1]
        self.deck3 = self.decks[2]
        self.deck4 = self.decks[3]

    def Reset(self):
        self.cards = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104]
        #self.cards = []
        self.possibleCards = cards.copy()
        self.played = []
        self.deck1 = []
        self.deck2 = []
        self.deck3 = []
        self.deck4 = []
        self.decks = [self.deck1, self.deck2, self.deck3, self.deck4]
        self.p1 = Hand('p1')
        self.p2 = Hand('p2')
        self.p3 = Hand('p3')
        self.p4 = Hand('p4')
        self.p5 = Hand('p5')
        self.p6 = Hand('p6')
        self.players = [self.p1, self.p2, self.p3, self.p4, self.p5, self.p6]
        self.Mix()
        state = np.array(self.GetState(self.p1))
        return state

    def AIPlay(self, player):
        card = player.SelectBest(self.possibleCards, self.decks)

class Hand:
    def __init__(self, _name):
        self.name = _name
        self.Reset()
    
    def Reset(self):
        self.tempPickUp = []
        self.cards = []
        self.penaltyCards = []
        self.penalty = 0
        self.selected = 0
        self.playerCards = []

    def RandomSelect(self):
        #print(self.cards)
        #n = random.randint(0, (len(self.cards) -1))#removed - 1
        #if len(self.cards) == 0:
           # x = 1
        self.selected = self.cards[0]
        del self.cards[0]

    def PlayerSelect(self):
        n = int(input("enter card you want to play")) - 1
        self.selected = self.cards[n]
        del self.cards[n]

    def PlayerPlay(self):
        deck = int(input("enter the numbered deck to place your card")) - 1
        return deck, self.selected

    def RandomPlay(self):
        return (random.randint(1, 4)), self.selected

    def CalcTotalPen(self):
        for card in self.penaltyCards:
            if card == 55:
                self.penalty += 7
            elif (card % 11) == 0:
                self.penalty += 5
            elif (card % 10) == 0:
                self.penalty += 3
            elif (card % 5) == 0:
                self.penalty += 2
            else:
                self.penalty += 1

    def CalcTurnPen(self, penaltyCards):
        penalty = 0
        for card in penaltyCards:
            if card == 55:
                penalty += 7
            elif (card % 11) == 0:
                penalty += 5
            elif (card % 10) == 0:
                penalty += 3
            elif (card % 5) == 0:
                penalty += 2
            else:
                penalty += 1
        penaltyCards = []
        return penalty

    def AiSelect(self, index):
        if index >= len(self.cards):
            self.selected = 0
            #print(self.selected)
        else:
            self.selected = self.cards[index]
            #print(self.selected)
            del self.cards[index]

    def AIOpSelect(self, state):
        card = 0
        while card == 0:
            index = AIOpponent.AIMove(state)
            if index < len(self.cards):
                card = self.cards[index]
        self.selected = card

    def GetDeckDif(self, decks, cards):
        deckDifs = [100, 100, 100, 100]
        cardDifs = [0, 0, 0, 0]
        for i in range (0, 4):
            for card in cards:
                dif = card - decks[i]
                if dif > 0 and dif < deckDifs[i]:
                    deckDifs[i] = dif
                    cardDifs[i] = card 
        return deckDifs

    def CardRange(self, difs, decks):
        numBetween = [0, 0, 0, 0]
        for i in range (0 ,4):
            dif = difs[i]
            card = decks[i][-1]
            u = 0
            while u < dif:
                card += 1
                u += 1
                if card in self.playerCards:
                    numBetween[i] += 1
        return numBetween

    def SelectBest(self, playercards, decks):
        self.playerCards = playercards.copy()
        for card in self.cards:
            self.playerCards.remove(card)
        difs = self.GetDeckDif(decks, self.cards)
        numBetween = self.CardRange(difs, decks)
        probs = CalcProbPerDeck(numBetween)
        penArray = self.CalcDeckPen(decks)


    def CalcProbPerDeck(self, numBetween):
        prob = [0, 0, 0, 0]
        for i in range(0, 4):
            _prob = numBetween[i] / len(self.playerCards)
            prob[i] = _prob
        return prob

    def CalcDeckPen(self, decks):
        penArray = []
        for deck in decks:
            pen = self.CalcTurnPen(deck)
            penArray.append(pen)
        return penArray

    #def CalcLowestProb(self, decks):
        
            
    #def GetLowestProb(self, probs):
        

    


    
        

env = Board()
#env.StartGame()
