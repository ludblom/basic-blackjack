#!/usr/bin/env python3

import math
import random
import sys


class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def getColor(self):
        return self.color

    def getValue(self):
        return self.value


class Deck:
    __countCards = None

    def __init__(self, deck):
        self.deck = deck
        self.__countCards = 0

    def updateCountCards(self, count):
        self.__countCards += count

    def returnCountCards(self):
        return self.__countCards

    def getDeck(self):
        return self.deck

    def draw(self, num):
        drawnCards = []
        if(len(self.deck) != 0):
            for i in range(num):
                drawnCards.append(self.deck.pop())
        else:
            return None

        return drawnCards


class Player:
    def __init__(self, name):
        self.cards = []
        self.score = 0
        self.__name = name
        self.wins = 0

    def addWin(self):
        self.wins += 1

    def getWins(self):
        return self.wins

    def getName(self):
        return self.__name

    def getCards(self):
        return self.cards

    def addCard(self, card):
        self.cards += card

    def getScore(self):
        return self.score

    def updateScore(self, score):
        self.score += score

    def removeScore(self):
        self.score = 0

    def clearCards(self):
        self.cards = []
        self.score = 0


def printCards(player):
    cards = player.getCards()

    if(str(player.getName()) is "player"):
        print("********** Player **********")
    elif(str(player.getName()) is "dealer"):
        print("********** Dealer **********")

    for card in cards:
        print("%s %s" % (card.getColor(), card.getValue()))
    print("Score: " + str(player.getScore()))
    print("****************************")


def printDealersCards(player):
    cards = player.getCards()
    print("********** Dealer **********")
    print("%s %s" % (cards[0].getColor(), cards[0].getValue()))
    print("%s %s" % (chr(9611), chr(9611)))
    print("Score: " + str(player.getScore()))
    print("****************************")


def calculate(player):
    vals = {"A": 11,
            "J": 10,
            "Q": 10,
            "K": 10}

    player.removeScore()
    for card in player.getCards():
        if(vals.get(card.getValue()) is None):
            player.updateScore(int(card.getValue()))
        else:
            player.updateScore(vals.get(card.getValue()))

    if(player.getScore() > 21):
        for card in player.getCards():
            if(card.getValue() is "A"):
                player.updateScore(-10)
                if(int(player.getScore()) <= 21):
                    return


def calculateDealer(player):
    vals = {"A": 11,
            "J": 10,
            "Q": 10,
            "K": 10}

    card = player.getCards()
    if(vals.get(card[0].getValue()) is None):
        player.updateScore(int(card[0].getValue()))
    else:
        player.updateScore(vals.get(card[0].getValue()))


def calcCountCards(dealer, player, cards):
    playerCards = dealer.getCards() + player.getCards()
    for card in playerCards:
        if(card.getValue() is "A" or
           card.getValue() is "J" or
           card.getValue() is "Q" or
           card.getValue() is "K"):
            # Add -1
            deck.updateCountCards(-1)
        elif(int(card.getValue()) >= 2 and int(card.getValue()) <= 6):
            # Add 1
            deck.updateCountCards(1)
        elif(int(card.getValue()) >= 7 and int(card.getValue()) <= 9):
            # Add 0
            deck.updateCountCards(0)
        else:
            # Subtract one
            deck.updateCountCards(-1)


def createDeck(decks):
    colors = [chr(9824), chr(9829), chr(9827), chr(9830)]
    dressed = ["J", "Q", "K", "A"]

    fullDeck = []

    numeric = [Card(str(value), color)
               for value in range(2, 11)
               for color in colors]

    dressed = [Card(value, color)
               for value in dressed
               for color in colors]

    deck = numeric + dressed

    for mergeDecks in range(decks):
        fullDeck += deck

    return fullDeck


def shuffleDeckHelper(deck):
    newDeck = []
    for i in range(len(deck)):
        card = random.randint(0, math.floor(len(deck))-1)
        newDeck.append(deck.pop(card))
    return newDeck


def shuffleDeck(deck, numShuffles):
    for shuffles in range(numShuffles):
        deck = shuffleDeckHelper(deck)
    return Deck(deck)


def dealerDrawEndCards(dealer, player):
    calculate(dealer)
    printCards(dealer)
    if(player.getScore() > 21):
        return
    while(dealer.getScore() < 17 or
          dealer.getScore() < player.getScore()):
        dealer.addCard(deck.draw(1))
        calculate(dealer)
        printCards(dealer)


def whoWon(dealer, player, cards):
    dealerScore = dealer.getScore()
    playerScore = player.getScore()

    if(playerScore == dealerScore):
        print("\n\nDRAW!\n\n")
        calcCountCards(dealer, player, cards)
        play(cards, dealer, player)
    elif((dealerScore < playerScore or
          dealerScore > 21) and
         playerScore <= 21):
        print("\n\nPLAYER WIN!\n\n")
        calcCountCards(dealer, player, cards)
        player.addWin()
        play(cards, dealer, player)
    else:
        print("\n\nDEALER WIN!\n\n")
        calcCountCards(dealer, player, cards)
        dealer.addWin()
        play(cards, dealer, player)


def playerAndComputer(deck, dealer, player):
    if(len(deck.getDeck()) > 0):
        inp = input("(D)raw, (S)tay, (Q)uit: ")

        if(inp is "D" or inp is "d"):
            player.addCard(deck.draw(1))
            calculate(player)
            printCards(player)
            if(player.getScore() >= 21):
                # Done, let dealer draw
                dealerDrawEndCards(dealer, player)
                whoWon(dealer, player, deck)

        elif(inp is "S" or inp is "s"):
            # Stay and ley dealer draw
            dealerDrawEndCards(dealer, player)
            whoWon(dealer, player, deck)

        elif(inp is "Q" or inp is "q"):
            sys.exit()

    else:
        print("End of deck")
        sys.exit()


def play(deck, dealer, player):
    # TODO: Add conditions to show it
    print("Status: %d" % int(deck.returnCountCards()))
    print("Player wins: %d" % int(player.getWins()))
    print("Dealer wins: %d" % int(dealer.getWins()))

    if(len(deck.getDeck()) > 4):
        # Clean round
        dealer.clearCards()
        player.clearCards()

        # Draw cards
        dealer.addCard(deck.draw(2))
        player.addCard(deck.draw(2))

        # Print cards
        calculateDealer(dealer)
        printDealersCards(dealer)

        calculate(player)
        printCards(player)

        while(True):
            playerAndComputer(deck, dealer, player)

    else:
        print("End of deck.")
        sys.exit()


if __name__ == "__main__":
    dealer = Player("dealer")
    player = Player("player")

    try:
        decks = int(input("Number of decks [6]: ") or 6)
        shuffles = int(input("Number of shuffles [4]: ") or 4)

    except ValueError:
        print("Please, enter a number. Exiting")
        sys.exit()

    # Create a deck, shuffle them and add it to Deck class
    deck = shuffleDeck(createDeck(decks), shuffles)

    # Play the game
    play(deck, dealer, player)
