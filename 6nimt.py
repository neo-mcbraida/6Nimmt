import random

class Board:
    def __init__(self):
        self.handNum = 0
       # self.cards = range (1, 104)
        self.pHolder = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104]
        self.cards = []
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
        
        
    def Mix(self):
        random.shuffle(self.cards)
        _cards = [[], [], [], [], [], [], [], [], [], []]
        self.deck1.append(self.cards[0])
        self.deck2.append(self.cards[1])
        self.deck3.append(self.cards[2])
        self.deck4.append(self.cards[3])
        del self.cards[:4]
        for i in range(6):
            self.players[i].cards = self.cards[:10]
            _cards[i] = self.cards[:10]
            del self.cards[:10]
        self.cards = _cards


    def GetCards(self):
        self.p1.PlayerSelect()
        self.p2.RandomSelect()
        self.p3.RandomSelect()
        self.p4.RandomSelect()
        self.p5.RandomSelect()
        self.p6.RandomSelect()
    
    def SortCards(self):
        self.players.sort(key=lambda x: x.selected)
        

    def Turn(self):
        print(self.decks)
        print(self.p1.penaltyCards)
        print(self.p1.cards)
        self.GetCards()
        self.SortCards()#rearranges self.players in order or card number
        self.PlaceCard()
        if len(self.p1.cards) == 0:
            self.PlayerGetPen()#all players calculate their penalty
            winner = self.GetWinner()#returns player with highest penalty
            print(winner)
            self.StartGame()
        else:
            self.Turn()

    def StartGame(self):
        self.cards = self.pHolder
        self.Mix()
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
        self.decks[index] = []
        self.decks[index].append(card)     

    def AddToRow(self, deck, index, card, player):
        if index == -1:
            index = self.GetSmallestDeck(self.decks)
            self.PickUp(index, player, card)
        elif len(deck) == 5:
            deck.append(card)
            self.GivePenalty(player, deck)
        else:
            deck.append(card)

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
                winners.append(player.name1)
            elif player.penalty == lowest:
                winners.append(player.name)
        return winners
        
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

class Hand:
    def __init__(self, _name):
        self.name = _name
        self.cards = []
        self.penaltyCards = []
        self.penalty = 0
        self.selected = 0


    def RandomSelect(self):
        n = random.randint(0, (len(self.cards)- 1))
        self.selected = self.cards[n]
        del self.cards[n]

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
    

b = Board()
b.StartGame()


        
